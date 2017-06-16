import numpy as np
import matplotlib.pyplot as plt
import os
import os.path
import codecs
from Tkinter import *

root_dir = 'data'
file_cnt = 0

for parent, dir_names, file_names in os.walk(root_dir):
	for file_name in file_names:
		print file_name
		inp = codecs.open(os.path.join(parent, file_name), 'r')
		lines = inp.readlines()
		n = len(lines)
		data = np.zeros((n, 18))
		time_stamp = np.zeros(n)
		for i in range(n):
			tags = lines[i].split(' ')
			time_stamp[i] = float(tags[0])
			data[i] = map(float, tags[1 :])
		inp.close()
		data = np.transpose(data)

		plt.figure(file_cnt, figsize = (8, 6))
		file_cnt = file_cnt + 1

		plt.plot(time_stamp, data[0])
		plt.plot(time_stamp, data[1])
		plt.plot(time_stamp, data[2])
		plt.plot(time_stamp, data[6])
		plt.plot(time_stamp, data[7])
		plt.plot(time_stamp, data[8])
		plt.plot(time_stamp, data[12])
		plt.plot(time_stamp, data[13])
		plt.plot(time_stamp, data[14])

plt.show()
