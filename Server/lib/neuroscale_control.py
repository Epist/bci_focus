#! /usr/bin/env python

# This example program reads EEG data from a well-formed LSL data source of your
# choosing, sends it up to a Concentration pipeline on Neuroscale, gets the
# result back, and then emits the result back into LSL under a stream name of
# your choice (see settings below).

import time
import json
try:
    from urllib.parse import urlparse  # Python 3
except ImportError:
    from urlparse import urlparse  # Python 2

# see README.md on how to install these packages
import requests
import paho.mqtt.client as mqtt
import msgpack
import pylsl

def deploy():
    # first we need to define the Neuroscale API URL to use; if use are enrolled in
    # a beta program you may have received a custom endpoint instead of the
    # default provided below.
    api_url = 'https://api.neuroscale.io'

    # you also need to provide your own access token; for security
    # reasons it is best to keep this string out of your code commits and instead
    # read it from an environment variable or file (if you do not have a token,
    # check our online documentation on how to generate one from your
    # username/password combination)
    access_token = '10e088ab-1374-4ad1-9dd2-3a995bce39a0'


    # construct the HTTP header that will be used for authorization
    auth_header = {'Authorization': 'Bearer ' + access_token}

    # next we need to identify the pipeline that we want to launch on Neuroscale
    # in this example we will launch the "Concentration Index" pipeline,
    # which computes a concentration index (note that there are some alternative
    # variants of this pipeline available)
    pipeline_name = 'Concentration (Generic)'

    # optionally the instance id if you already have an instance running
    instance_id = ''

    # this is the local LSL stream that we will send up to the cloud
    input_stream = 'openbci_eeg_team5'

    # this is the local stream that we forward back to LSL
    output_stream = 'ConcentrationStream'

    # resolve an EEG stream on the LSL network
    print("looking for the input stream '%s'..." % input_stream)
    streams = pylsl.resolve_stream('name', input_stream)

    # create a new inlet and extract meta-data
    inlet = pylsl.StreamInlet(streams[0])
    info = inlet.info()
    sampling_rate = info.nominal_srate()
    modality = info.type()
    desc = info.desc()
    try:
        channel_labels = []
        ch = desc.child('channels').child('channel')
        while not ch.empty():
            channel_labels.append(ch.child_value('label') or '(no label)')
            ch = ch.next_sibling('channel')
        if len(set(channel_labels)) < len(channel_labels):
            raise RuntimeError("Channel labels are not unique!")
        if len(channel_labels) != info.channel_count():
            raise RuntimeError("Incorrect number of channel labels!")
    except Exception as e:
        print("Error parsing channel labels: %s; falling back to defaults" % e)
        # not all data sources provide proper channel labels, but Neuroscale
        # requires them, so we make some up
        channel_labels = ['Ch' + str(k) for k in range(info.channel_count())]

    # open LSL output stream (one channel, 10 Hz); note that the UID must be
    # unique on the local network
    outinfo = pylsl.StreamInfo(output_stream, 'EEG', 1,
                               10, 'float32', 'mystream-j98ewyu8g')
    outlet = pylsl.StreamOutlet(outinfo)

    # next we will look up the pipeline of interest by name from the list
    # of available pipelines
    r = requests.get(api_url + '/v1/pipelines', headers=auth_header)
    if r.status_code == 200:  # 200: ok
        body = r.json()
        pipelines = body['data']
        # now go through all pipelines and pick the one that has a matching name
        for p in pipelines:
            if p['name'] == pipeline_name:
                pipeline_id = p['id']
                break
        else:
            print("ERROR: Could not find a pipeline named '%s'" % pipeline_name)
            exit(1)
    else:
        print("ERROR: Could not query available pipelines (HTTP %s); check "
              "your API URL and credentials." % r.status_code)
        exit(1)

    # from the stream parameters we construct the pipeline meta-data, which are part
    # of the required launch options; we need to declare the list of streams that
    # the pipeline is expected to receive and to send back; here we want to send
    # an EEG stream and receive the concentration index stream;
    eeg_stream = {"name": "myeeg", "type": modality, "sampling_rate": sampling_rate,
                  "channels": [{"label": c} for c in channel_labels]}
    # we also define the output stream, which is a single channel
    conc_stream = {"name": "myeeg", "type": modality, "sampling_rate": sampling_rate,
                   "channels": [{"label": "concindex"}]}
    # pipelines communicate with their environment through i/o nodes, and to fully
    # specify the desired i/o behavior of the pipeline, we need to define those
    # nodes and their streams; in our case, the pipeline has only a single node on
    # the input and one on the output, and both of them are named "default"
    node_decl_in = {"name": "default", "streams": [eeg_stream]}
    node_decl_out = {"name": "default", "streams": [conc_stream]}
    # the complete meta-data is now just the list of input and ouput nodes
    metadata = {"nodes": {"in": [node_decl_in], "out": [node_decl_out]}}

    # this sample can send either JSON-encoded or msgpack-encoded messages; the
    # msgpack format is recommended for anything other than wire debugging
    json_fallback = False

    # assemble the final launch options for the pipeline; for further options have
    # a look at the API docs (for instance, you can toggle some server-side
    # features)
    params = {"pipeline": pipeline_id, "metadata": metadata,
              "encoding": 'json' if json_fallback else 'msgpack'}

    if not instance_id:
        # to launch our processing pipeline now we need to create a new "instance"
        # of the desired pipeline (a running piece of code)
        # IMPORTANT: note that, once the instance has been created, you are
        # consuming resources in the cloud until you destroy the instance again
        r = requests.post(api_url + '/v1/instances', headers=auth_header, json=params)
    else:
        # we already know the id of a running instance and we'd like to reconfigure
        # it with new parameters -- this is usually much faster and easier on the
        # backend
        r = requests.patch(api_url + '/v1/instances/' + instance_id,
                           headers={'Authorization': auth_header['Authorization'],
                                    'Content-Type': 'application/json'},
                           data=json.dumps(params))
    if r.status_code == 201 or r.status_code == 200:  # 201: created / 200: ok
        reader = read_endpoint = None
        # we need to extract the instance id from the response so we can shut it
        # down again later (note: it's instructive to print out the JSON response)
        body = r.json()
        instance_id = body['id']
        try:
            print('instance %s has been requested successfully' % instance_id)

            # wait until the instance has launched; this is generally useful since
            # any data you stream up while the instance is not yet running is lost
            print('waiting for instance to come up...')
            last_state = ''
            while last_state != 'running':
                # this API call will return a lot of generally useful instance state
                # one can also get back debug information by appending /debug to
                # the below URL
                r = requests.get(api_url + '/v1/instances/' + instance_id,
                                 headers=auth_header)
                state = r.json()["state"]
                if state != last_state:
                    print(state + "...")
                    last_state = state
                time.sleep(1)

            # now that we have an instance, we are ready to stream raw data up and
            # processed data back down

            # for this, we need to extract the read/write endpoints that are
            # provided by the instance and described in the response body
            def get_endpoint(x, mode='read'):
                url = [e['url'] for e in x['endpoints']['data'] if e['mode'] == mode]
                return urlparse(url[0])
            read_endpoint = get_endpoint(body, mode='read')
            write_endpoint = get_endpoint(body, mode='write')

            # as we are using the paho MQTT library we need to declare a few
            # callback functions handle subscription and message receiving; if you
            # are only sending data and not receiving you can omit these as they
            # only provide diagnostics
            def on_connect(client, userdata, flags, rc):
                print("%s connected with result code %s" % (userdata, rc))
                # a common idiom in paho is to subscribe upon connect, which allows
                # us to tolerate connection failure
                if userdata == 'reader':
                    # by appending '/#' to the mqtt topic you are reading from all
                    # output sub-topics of the pipeline, which can include
                    # additional debug and monitoring data; to save bandwidth, you
                    # can also connect to specific sub-topics by replacing # with
                    # the topic name, as done here
                    client.subscribe('/' + str(read_endpoint.path[1:]) + '/default')

            def on_message(client, userdata, msg):
                # this callback will be invoked whenever we get a message back
                # the payload must first be decoded using either JSON or msgpack
                # (depending on pipeline settings)
                payload = msg.payload
                data = json.loads(payload) if json_fallback else msgpack.loads(payload)
                # the message has a 'streams' field that is a list of one chunk per
                # stream for which data was received (note that a stream that
                # updates less frequently than others may not be included in every
                # message)
                streams = data[b'streams']
                if streams:
                    pass
                    # print('received message on topic %s: ' % msg.topic)
                else:
                    pass
                    # print('received empty message on topic %s: ' % msg.topic)
                for stream in streams:
                    # the name of the stream: many pipelines will pass the input
                    # names through unchanged
                    name = stream[b'name']
                    # this is a list of samples, each of which is a list of channels
                    samples = stream[b'samples']
                    # a list of time stamps, one per sample (same length as samples)
                    stamps = stream[b'timestamps']
                    if name == b'myeeg':
                        # push a single sample
                        outlet.push_sample(samples[0])
                    # print('  stream %s: %i samples' % (name, len(stamps)))

            def on_disconnect(client, userdata, *args):
                print("%s got disconnected." % userdata)
                if userdata == 'reader':
                    reader.connect(read_endpoint.hostname, read_endpoint.port)
                else:
                    writer.connect(write_endpoint.hostname, write_endpoint.port)

            # these callbacks are only added for completeness and for extra
            # diagnostics
            def on_subscribe( client, userdata, mid, granted_qos ):
                print("%s subscribed at quos level %s" % (userdata, granted_qos))

            def on_publish( client, userdata, mid ):
                pass
                # print("%s has published." % userdata)

            def on_unsubscribe(client, userdata, *args):
                pass
                # print("%s got unsubscribed." % userdata)

            # having defined the callbacks, we're ready to subscribe to the read
            # endpoint; if you make an application that only uploads data you can
            # skip this part. (the userdata parameter is only used by our own
            # callbacks and is not otherwise necessary; same applies to the
            # subsequent writer setup call)
            reader = mqtt.Client(userdata='reader')
            reader.on_connect = on_connect
            reader.on_subscribe = on_subscribe
            reader.on_message = on_message
            reader.on_disconnect = on_disconnect
            reader.on_unsubscribe = on_unsubscribe
            reader.connect(read_endpoint.hostname, read_endpoint.port)
            reader.loop_start()

            # we also hook up the write endpoint; again, if you are not streaming up
            # data you can omit this part
            writer = mqtt.Client(userdata='writer')
            writer.on_connect = on_connect
            writer.on_publish = on_publish
            writer.on_disconnect = on_disconnect
            writer.on_unsubscribe = on_unsubscribe
            writer.connect(write_endpoint.hostname, write_endpoint.port)
            writer.loop_start()

            # in the following infinite loop we're sending and receiving data
            print('now sending data...')
            while True:
                # read a new chunk from LSL
                samples, timestamps = inlet.pull_chunk()
                if timestamps:
                    # print("Got new chunk from LSL (len=%s)..." % len(timestamps))
    
                    # build eeg part of the message from it
                    eeg_chunk = {'name': 'myeeg', 'samples': samples,
                                 'timestamps': timestamps}

                    # now build the message that holds the chunk; generally, a message
                    # holds a list of one or more stream chunks in a field named
                    # streams
                    msg = {'streams': [eeg_chunk]}

                    # depending on the pipeline configuration, we need to encode either
                    # via JSON or msgpack
                    if json_fallback:
                        msg = json.dumps(msg)
                    else:
                        msg = bytearray(msgpack.dumps(msg))

                    # send the message and sleep for a bit
                    writer.publish('/' + str(write_endpoint.path[1:]), msg)

                # note that using a shorter sleep interval here will lead to more
                # messages per second being transmitted; there is an upper limit
                # to how many messages per second the backend will pick up,
                # and if you find that the output starts to lag behind by several
                # seconds, most likely your transmission interval is too short
                time.sleep(0.1)

        except Exception as ex:
            print("ERROR: %s" % ex)
        finally:
            # we unsubscribe explicitly to shut off the log messages
            if reader:
                reader.unsubscribe('/' + str(read_endpoint.path[1:]) + '/default')
                time.sleep(0.5)
            # Do not forget to terminate the instance after you are done using it
            # this is simply done using a delete request that involves the
            # corresponding instance; note: if you lost your instance id somehow,
            # or what to check what instances you have running, you can query your
            # instances via the call:
            # requests.get(api_url + '/v1/instances', headers=auth_header).json()
            # it's good practice to reuse (i.e., reconfigure instead of recreate)
            # existing instances if possible because it reduces pressure on the
            # neuroscale backend
            kill = ''
            while kill not in ['y', 'n']:
                try:
                    kill = raw_input('Kill the instance? (y/n):')  # Python 2.x
                except NameError:
                    kill = input('Kill the instance? (y/n):')  # Python 3.x
            if kill == 'y':
                r = requests.delete(api_url + '/v1/instances/' + instance_id,
                                    headers=auth_header)
                if r.status_code == 204:
                    print('instance %s was deleted successfully' % instance_id)
                else:
                    print('ERROR: instance %s was not deleted (HTTP %i)' %
                          (instance_id, r.status_code))
    else:
        print('ERROR: could not launch instance (HTTP %i)' % r.status_code)

def kill():
    api_url = 'https://api.neuroscale.io'

    # you also need to provide your own access token; for security
    # reasons it is best to keep this string out of your code commits and instead
    # read it from an environment variable or file (if you do not have a token,
    # check our online documentation on how to generate one from your
    # username/password combination)
    access_token = '10e088ab-1374-4ad1-9dd2-3a995bce39a0'

    # construct the HTTP header that will be used for authorization
    auth_header = {'Authorization': 'Bearer ' + access_token}

    # get current set of instances...
    killed, notkilled = 0, 0
    r = requests.get(api_url + '/v1/instances', headers=auth_header)
    if r.status_code == 200:  # HTTP 200: ok
        # kill each of them
        for inst in r.json()['data']:
            instance_id = inst['id']
            r = requests.delete(api_url + '/v1/instances/' + instance_id,
                                headers={'Authorization': 'Bearer ' + access_token})
            if r.status_code == 204:
                print('instance %s was deleted successfully' % instance_id)
                killed += 1
            else:
                print('ERROR: instance %s was not deleted (HTTP %i)' %
                      (instance_id, r.status_code))
                notkilled += 1
        if notkilled == 0:
            print("Completed successfully (%i instances killed)." % killed)
        else:
            print("Completed with errors (%i killed, %i survived)." % (killed, notkilled))
    else:
        print('ERROR: could not list instances (HTTP %i)' % r.status_code)