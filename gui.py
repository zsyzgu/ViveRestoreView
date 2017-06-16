import numpy as np
from Tkinter import Tk, Button, GROOVE
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkMessageBox
import os
import os.path
import codecs

class Data:
	filename = ''
	timestamp = []
	transform = []

rootdir = 'data'
files = 0
data_set = []

for parent, dirnames, filenames in os.walk(rootdir):
	for filename in filenames:
		print filename
		inp = codecs.open(os.path.join(parent, filename), 'r')
		lines = inp.readlines()
		inp.close()
		n = len(lines)
		timestamp = np.zeros(n)
		transform = np.zeros((n, 18))
		for i in range(n):
			tags = lines[i].split(' ')
			timestamp[i] = float(tags[0])
			transform[i] = map(float, tags[1 :])
		transform = np.transpose(transform)
		data = Data()
		data.filename = filename
		data.timestamp = timestamp
		data.transform = transform
		data_set.append(data)

'''
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
'''

def id_device(i):
	return i

def id_trans(i):
	return len(devices) + i

def id_data(i):
	return len(devices) + len(trans) + i

def id_opt(i):
	return len(devices) + len(trans) + len(data_set) + i

def draw():
	plt.figure(1, figsize = (6, 6))
	plt.clf()

	action_cnt = 0
	for i in range(len(data_set)):
		if (switchs[id_data(i)] == 1):
			action_cnt = action_cnt + 1
			data = data_set[i]
			device_cnt = 0
			for j in range(18):
				if (switchs[id_trans(j % len(trans))] == 1 and switchs[id_device(j / len(trans))] == 1):
					device_cnt = device_cnt + 1
					x = data.timestamp
					y = data.transform[j]

					if switchs[id_opt(0)]:
						y = y - sum(y) / len(y)
					if switchs[id_opt(1)]:
						y = (y - min(y)) / (max(y) - min(y))
					
					if action_cnt == 1:
						line_style = '-'
					elif action_cnt == 2:
						line_style = '--'
					elif action_cnt == 3:
						line_style = '-.'
					else:
						line_style = ':'
					
					if device_cnt == 1:
						color_style = 'b'
					elif device_cnt == 2:
						color_style = 'r'
					else:
						color_style = 'g'
					
					plt.plot(x, y, line_style + color_style)

	plt.show()

def click_button(i):
	switchs[i] = 1 - switchs[i]
	if switchs[i] == 1:
		buttons[i].config(bg = 'white')
	else:
		buttons[i].config(bg = 'gray')
	
	draw()

root = Tk()

devices = ['head', 'left_hand', 'right_hand']
trans = ['x', 'y', 'z', 'rx', 'ry', 'rz']
opts = ['origin', 'normalize']

buttons = []
switchs = np.zeros(len(devices) + len(trans) + len(data_set) + len(opts))

Button(root, text = 'device', state = 'disabled', bg = 'black', width = 30).pack()
for i in range(len(devices)):
	button = Button(root, text = devices[i], bg = 'gray', width = 30, command = lambda i = i : click_button(id_device(i)))
	button.pack()
	buttons.append(button)

Button(root, text = 'trans', state = 'disabled', bg = 'black', width = 30).pack()
for i in range(len(trans)):
	button = Button(root, text = trans[i], bg = 'gray', width = 30, command = lambda i = i : click_button(id_trans(i)))
	button.pack()
	buttons.append(button)

Button(root, text = 'action', state = 'disabled', bg = 'black', width = 30).pack()
for i in range(len(data_set)):
	button = Button(root, text = data_set[i].filename, bg = 'gray', width = 30, command = lambda i = i : click_button(id_data(i)))
	button.pack()
	buttons.append(button)

Button(root, text = 'opt', state = 'disabled', bg = 'black', width = 30).pack()
for i in range(len(opts)):
	button = Button(root, text = opts[i], bg = 'gray', width = 30, command = lambda i = i : click_button(id_opt(i)))
	button.pack()
	buttons.append(button)

root.mainloop()