#!/usr/bin/python
'''
  openbci_control.py
  ---------------

  This is the main module for establishing an OpenBCI stream through the Lab Streaming Layer (LSL).

  Lab streaming layer is a networking system for real time streaming, recording, and analysis of time-series 
  data. LSL can be used to connect OpenBCI to applications that can record, analyze, and manipulate the data, 
  such as Matlab, NeuroPype, BCILAB, and others.


'''

import lib.neuroscale_control as ns
import lib.streamerlsl as streamerlsl
from multiprocessing import Process


class OpenBCIControl(Process):
    def __init__(self):
        super().__init__()
        self.paused = False

    def run(self):
        # ask alex about threading here
        pass

    ### PUBLIC FUNCTIONS
    def get_pause_state(self):
        return self.paused

    def start_streaming(self):
        '''
        Public function for starting the streaming pipeline (OpenBCI to LSL to NeuroPype)
        '''

        # ask alex about threading here
        self._create_lsl()
        self._start_lsl()
        self._send_to_ns()

    def pause_streaming(self):
        '''
        Public function for pausing the streaming pipeline (halting OpenBCI to LSL)
s       '''
        self.paused = True
        self._stop_lsl()

    def resume_streaming(self):
        '''
        Public function for resuming the OpenBCI+LSL stream
        '''
        self.paused = False
        self._start_lsl()

    def stop_streaming(self):
        '''
        Public function for killing the streaming pipeline (close LSL, end NeuroScale instance)
        '''
        self._stop_lsl()
        ## kill NS instance here
        ns.kill()
        self.terminate()

    ### PRIVATE FUNCTIONS
    def _create_lsl(self):
        self.lsl = streamerlsl.StreamerLSL(GUI=False)
        self.lsl.create_lsl()

    def _start_lsl(self):
        '''
        This method begins OpenBCI streaming into the LSL
        '''
        self.lsl.start_streaming()

    def _stop_lsl(self):
        '''
        This stops OpenBCI streaming to LSL
        '''
        self.lsl.stop_streaming()

    def _send_to_ns(self):
        '''
        This begins the NeuroScale deployment. NeuroScale will read from LSL
        '''
        ns.deploy()

