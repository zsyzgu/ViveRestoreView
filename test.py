import data_process as dat
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.stattools import adfuller
import numpy as np
from scipy import stats
import math

fps = 100
action_interval = 5 * fps
action_period = 1 * fps

data_set = dat.get_data_set()

task_num = len(data_set)
action_num = len(data_set[0].actions)
trans_num = len(data_set[0].transform)

def caln_cor(data, act_id = -1):
	action_num = len(data.actions)
	trans_num = len(data.actions[0])
	
	if act_id == -1:
		mat = np.zeros((trans_num, action_num * action_period))
		for trans_id in range(trans_num):
			for act_id in range(action_num):
				mat[trans_id][act_id * action_period : (act_id + 1) * action_period] = data.actions[act_id][trans_id]
	else:
		mat = np.zeros((trans_num, action_period))
		for trans_id in range(trans_num):
			mat[trans_id] = data.actions[act_id][trans_id]
	
	cor = np.corrcoef(mat)
	return cor

result = np.zeros((task_num, trans_num * trans_num))
for task_id in range(task_num):
	result[task_id] = caln_cor(data_set[task_id]).reshape(trans_num * trans_num)

for task_id in range(task_num):
	correct = 0
	for act_id in range(action_num):
		test_cor = caln_cor(data_set[task_id], act_id).reshape(trans_num * trans_num)
		
		min_diff = 1e8
		predict = -1
		for i in range(task_num):
			diff = sum(abs(test_cor - result[i]))
			if diff < min_diff:
				min_diff = diff
				predict = i
		if predict == task_id:
			correct = correct + 1
	
	print task_id, float(correct) / action_num
