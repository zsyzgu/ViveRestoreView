import numpy as np
import os
import os.path
import codecs
import pandas as pd
import matplotlib.pyplot as plt

fps = 100
action_interval = 3 * fps
action_period = 1 * fps

class Data:
	filename = ''
	timestamp = []
	transform = []
	actions = []

def resample(ori_x, ori_y, fps):
	if len(ori_x) == 0 or len(ori_x) != len(ori_y):
		return ori_x, ori_y
	
	x = [ori_x[0]]
	y = [ori_y[0]]
	interval = 1.0 / fps
	t = interval

	for i in range(1, len(ori_x)):
		while t <= ori_x[i]:
			x.append(t)
			y.append((ori_y[i] * (t - ori_x[i - 1]) + ori_y[i - 1] * (ori_x[i] - t)) / (ori_x[i] - ori_x[i - 1]))
			t = t + interval
	
	return x, y

def get_data_set():
	rootdir = 'data'
	data_set = []

	for parent, dirnames, filenames in os.walk(rootdir):
		for filename in filenames:
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
				
			timestamp, transform = resample(timestamp, transform, fps)
			transform = np.transpose(transform)
			
			trans_num = len(transform)
			n = len(timestamp)
			z = np.zeros(n)
			for trans_id in range(trans_num):
				y = transform[trans_id] - pd.ewma(transform[trans_id], halflife = action_period)
				z = z + [y[i] * y[i] for i in range(n)]
			
			actions = []
			action_num = int((len(timestamp) - action_period / 2) / action_interval)
			for act_id in range(action_num):
				action = np.zeros((trans_num, action_period))
				mid = action_interval * (act_id + 1)
				t = -1
				for i in range(0, action_period):
					if (z[mid + i] == max(z[mid + i - 5 : mid + i + 5])):
						t = mid + i
						break
					if (z[mid - i] == max(z[mid - i - 5 : mid - i + 5])):
						t = mid - i
						break
				if t != -1:
					for trans_id in range(trans_num):
						action[trans_id] = transform[trans_id][int(t - action_period / 2) : int(t + action_period / 2)]
						action[trans_id] = action[trans_id] - sum(action[trans_id]) / action_period
					actions.append(action)
			
			data = Data()
			data.filename = filename
			data.timestamp = timestamp
			data.transform = transform
			data.actions = actions
			data_set.append(data)
	
	return data_set

