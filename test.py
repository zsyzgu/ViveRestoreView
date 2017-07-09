import data_process as dat
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.stattools import adfuller
import numpy as np
from scipy import stats
import math
from sklearn import neighbors
from sklearn import tree
from sklearn import svm
from sklearn.cross_validation import train_test_split
from sklearn.decomposition import PCA

fps = 100
action_interval = 3 * fps
action_period = 1 * fps
action_seg = 10

data_set = dat.get_data_set()

task_num = len(data_set)
trans_num = len(data_set[0].transform)

def caln_feature(data, act_id):
	mat = np.zeros((trans_num, action_period))
	for trans_id in range(trans_num):
		mat[trans_id] = data.actions[act_id][trans_id]
	
	feature = []
	
	seg_len = action_period / action_seg
	for seg in range(action_seg):
		x = []
		y = []
		z = []
		for i in range(6):
			x.append(sum(mat[i * 3 + 0][seg * seg_len : (seg + 1) * seg_len]))
			y.append(sum(mat[i * 3 + 1][seg * seg_len : (seg + 1) * seg_len]))
			z.append(sum(mat[i * 3 + 2][seg * seg_len : (seg + 1) * seg_len]))
	
		for i in range(6):
			for j in range(i + 1):
				feature.append(x[i] * x[j] + z[i] * z[j])
				feature.append(y[i] * y[j])
	
	feature = feature / sum(map(abs, feature))
	return feature

x = []
y = []
for task_id in range(task_num):
	action_num = len(data_set[task_id].actions)
	for act_id in range(action_num):
		x.append(caln_feature(data_set[task_id], act_id))
		y.append(task_id)	

pca = PCA(n_components = action_seg * 5)
pca.fit(x)
x = pca.transform(x)


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)
clf = neighbors.KNeighborsClassifier(algorithm = 'kd_tree')
#clf = svm.LinearSVC()
#clf = tree.DecisionTreeClassifier()
clf.fit(x_train, y_train)
predict = clf.predict(x_test)  
for i in range(len(y_test)):
	if y_test[i] != predict[i]:
		print y_test[i], predict[i]
print np.mean(predict == y_test)
