from pylsl import StreamInlet, resolve_stream
import threading
import time
import matplotlib.pyplot as plt
import numpy as np


class Data_Buffer():
	def __init__():
		self.data_list = [] #this is the list that will hold the data

	def _collect_data():
		'''
		This collects data from LSL outlet from NeuroScale for the concentration index output.
		'''
		start_time = time.time()
		current_time = start_time

		while (True):
			print(current_time)
			print(start_time)
			current_time = time.time()
			conc_index, timestamp = self.inlet.pull_sample()
			self.data_list.append(conc_index)
		# self.display(data_list)




	def start_lsl_listener():
		'''
		This starts looking for the LSL outlet from NeuroScale. Once found, collect_data is launched.
		:return:
		'''
		print("looking for an EEG stream...")
		streams = resolve_stream('name', 'ConcentrationStream')
		self.inlet = StreamInlet(streams[0])
		lsl_thread = threading.Thread(target=receive_data)
		lsl_thread.daemon = True
		lsl_thread.run()
	 
	def _display_data():
		x = np.arange(0,len(self.data_list))
		y = self.data_list
		plt.plot(x,y)
		plt.show()


	###############################
	# Analysis Functions
	###############################

	# REAL TIME
	def _detect_distraction(self):
        pass

    def _emit_distraction_signal(self):
        pass



	# POST-SESSION
	def _calculate_mean_conc(self):
		return np.mean(self.data_list)

	def _calculate_conc_timeseries(self):
		#this function returns the time series data of the concentration index, smoothed (1 value per second)
		smoothed = np.zeros(len(self.data_list)/10)
		second_sum = 0
		for i in range(len(data_list)):
			while i % 10 != 0 or i == 0:
				second_sum+=data_list[i]
			smoothed[i/10 - 1].append(second_sum/10)
			second_sum = data_list[i]
		return smoothed

	def _calculate_longest_focus_period(self):
        pass
