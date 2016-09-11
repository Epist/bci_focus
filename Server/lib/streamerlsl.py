'''
  streamerlsl.py
  ---------------

  This is the module that handles the creation and function of LSL using OpenBCI data.

  If the GUI application is used, the GUI controls the parameters of the stream, and calls
  the functions of this class to create, run, and stop each stream instance.

  If the command line application is used, this module creates the LSL instances
  using default parameters, and then allows the user interaction with the stream via the CLI.


'''

import random
import threading
import time
from pylsl import StreamInfo, StreamOutlet

import lib.open_bci_v3 as bci


class StreamerLSL():
    def __init__(self, port=None):
        if port is None:
            self.initialize_board(autodetect=True)
        else:
            self.initialize_board(port=port)

    def initialize_board(self, autodetect=False, port=None, daisy=None):
        print("\n-------INSTANTIATING BOARD-------")
        self.board = bci.OpenBCIBoard()

    def send(self, sample):
        try:
            self.outlet_eeg.push_sample(sample.channel_data)
        except:
            print("Error! Check LSL settings")

    def create_lsl(self, default=True, stream1=None, stream2=None):
        random_id = random.randint(0, 255)
        # default parameters
        eeg_name = 'openbci_eeg'
        eeg_type = 'EEG'
        eeg_chan = 8
        eeg_hz = 250.0
        eeg_data = 'float32'
        eeg_id = 'openbci_eeg_id' + str(random_id)
        # create StreamInfo
        self.info_eeg = StreamInfo(eeg_name, eeg_type, eeg_chan, eeg_hz, eeg_data, eeg_id)

        chns = self.info_eeg.desc().append_child('channels')
        labels = ['Fp1', 'Fp2', 'C3', 'C4', 'T5', 'T6', 'O1', 'O2']
        for label in labels:
            ch = chns.append_child("channel")
            ch.append_child_value('label', label)
            ch.append_child_value('unit', 'microvolts')
            ch.append_child_value('type', 'EEG')

        # additional Meta Data
        self.info_eeg.desc().append_child_value('manufacturer', 'OpenBCI Inc.')

        # create StreamOutlet
        self.outlet_eeg = StreamOutlet(self.info_eeg)


        print("--------------------------------------\n" + \
          "LSL Configuration: \n" + \
          "  Stream 1: \n" + \
          "      Name: " + eeg_name + " \n" + \
          "      Type: " + eeg_type + " \n" + \
          "      Channel Count: " + str(eeg_chan) + "\n" + \
          "      Sampling Rate: " + str(eeg_hz) + "\n" + \
          "      Channel Format: " + eeg_data + " \n" + \
          "      Source Id: " + eeg_id + " \n" + \
          "Electrode Location Montage:\n" + \
          str(labels) + "\n" + \
          "---------------------------------------\n")


    def cleanUp():
        board.disconnect()
        print("Disconnecting...")
        atexit.register(cleanUp)


    def start_streaming(self):
        boardThread = threading.Thread(target=self.board.start_streaming, args=(self.send, -1))
        boardThread.daemon = True  # will stop on exit
        boardThread.start()


    def stop_streaming(self):
        self.board.stop()
        time.sleep(.1)
