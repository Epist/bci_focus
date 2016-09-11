from pylsl import StreamInlet, resolve_stream
import threading
import time
import matplotlib.pyplot as plt
import numpy as np


class Data_Buffer:
    def __init__(self):
		self.data_list = [] #this is the list that will hold the data
		self.time_list = [] #this will hold the adjusted timestamps

	def _collect_data(self):
		'''
		This collects data from LSL outlet from NeuroScale for the concentration index output.
		'''
		start_time = time.time()
		current_time = start_time

		while (True):
			#print(current_time)
			#print(start_time)
			#current_time = time.time() - start_time
			conc_index, timestamp = self.inlet.pull_sample()
			self.data_list.append(conc_index)
			self.time_list.append(timestamp)




	def start_lsl_listener(self):
		'''
		This starts looking for the LSL outlet from NeuroScale. Once found, collect_data is launched.
		:return:
		'''
		print("looking for an EEG stream...")
		streams = resolve_stream('name', 'ConcentrationStream')
		self.inlet = StreamInlet(streams[0])
		lsl_thread = threading.Thread(target=self._collect_data())
		lsl_thread.daemon = True
		lsl_thread.run()

	def _detect_distraction(self):

		pass

	def _emit_distraction_signal(self):
		pass



	def _calculate_mean_conc(self):
		return np.mean(np.asarray(self.data_list))

	def _calculate_conc_timeseries(self):
		#this function returns the time series data of the concentration index, smoothed (1 value per second)
		smoothed = np.zeros(len(self.data_list)/10)
		second_sum = 0
		for i in range(len(self.data_list)):
			while i % 10 != 0 or i == 0:
				second_sum+=self.data_list[i]
			smoothed[i/10 - 1].append(second_sum/10)
			second_sum = self.data_list[i]
		return smoothed

	def _calculate_longest_focus_period(self):
		#this function returns the longest consecutive period of concentration
		threshold = 0.5 # concentration index > 0.5 -> concentrated for now
		cutoff = (np.sign(np.asarray(self.data_list) - threshold) + 1.0)/2.0

		return
