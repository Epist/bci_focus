(function () {
    'use strict';
    angular.module('app')
        .service('livestreamService', ['$http', 'RESTService', 'NEUROSCALE_API_URL', LiveStreamService]);

    var service, rest, $http;

    var mqttConnection, ns_api, _onMessageArrived;

    function LiveStreamService(_$http_, restService, _NEUROSCALE_API_URL_) {
        service = this;
        rest = restService;
        $http = _$http_;
        ns_api = _NEUROSCALE_API_URL_;

    }


    LiveStreamService.prototype.createConnection = function (onMessageArrived) {

        if (!mqttConnection) {
            NeuroScale.ACCESS_KEY = 'e9c67fe8-90a6-4437-a84c-b9119ad001b5';
            NeuroScale.API_HOST = ns_api;

            console.log(NeuroScale.ACCESS_KEY, NeuroScale.API_HOST);

            _onMessageArrived = onMessageArrived;

            mqttConnection = NeuroScale.API.loadInstances(createConnection);
        }
    };



    var messageArrivedCallback = function (topic, jsonObject) {
        // this callback is called when a new packet arrives.
        // console.log('Got a packet!');
        // console.log(jsonObject);
        // console.log(jsonObject.streams[0].samples);
        // numberOfMessages = numberOfMessages + 1;


        // if (jsonObject.streams.length > 0) { // if the received sample contains any values.
        //   // read the first array value of the last sample of the first stream.
        //   relaxation = jsonObject.streams[0].samples[jsonObject.streams[0].samples.length - 1][0];
        //   console.log('Relaxation: ' + relaxation);
        //   document.getElementById('relaxationValue').innerHTML = '<p>Relaxation = ' + relaxation + '</p>' + '<p>Number of MQTT messages received = ' + numberOfMessages + '</p>';
        // }
    };

    function get_uuid() {
        function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
                .toString(16)
                .substring(1);
        }

        return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
            s4() + '-' + s4() + s4() + s4();
    }

    // get instance and create connection
    var createConnection = function () {
        console.log(NeuroScale.API.getInstances());
        var instance = NeuroScale.API.getLatestInstance();

        var messageArrivedCb = _onMessageArrived || messageArrivedCallback;

        // create mqttConnection
        var host = NeuroScale.API.getMQTTHost(instance);
        var port = 8000;
        var topic = "/" + NeuroScale.API.getMQTTTopic(instance) + '/out/default';
        var encoding = instance.encoding;
        return new NeuroScale.MQTT.Connection(host, port, "js_client_id_" + get_uuid(), topic, encoding, messageArrivedCb);
    };


})();