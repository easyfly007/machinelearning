from numpy import *
import operator

def createdataset():
	group = array([[1.0, 1.1], [1.0, 1.0],  [0.0, 0], [0, 0.1]] )
	labels = ['A', 'B', 'B', 'B']
	return group, labels

def classify0(inx, dataset, labels, k):
	datasetsize = dataset.shape[0]
	print(datasetsize)
	diffmat = tile(inx, (datasetsize, 1)) - dataset
	sqdiffmat = diffmat**2
	sqdistances = sqdiffmat.sum(axis = 1)
	distances = sqdistances**0.5
	sorteddistindices = distances.argsort()
	classcount = {}
	for i in range(k):
		voteilabel = labels[sorteddistindices[i]]
		classcount[voteilabel] = classcount.get(voteilabel, 0) + 1
	sortedclasscount = sorted(classcount.iteritems(), 
		key = operator.itemgetter(1), reverse = True)
	return sortedclasscount[0][0]

group, labels = createdataset()
a = classify0([0, 0], group, labels, 3)
print a

def file2matrix(filename):
	fr = open(filename)
	arrayolines = fr.readlines()
	numberoflines = len(arrayolines)
	returnmat = zeros((numberoflines, 3))
	classlabelvector = []
	index = 0
	for line in arrayolines:
		line = line.strip()
		listfromline = line.split('\t')
		returnmat[index, :] = listfromline[0:3]
		classlabelvector.append(int(listfromline[-1]))
		index +=1
	return returnmat, classlabelvector

def autonorm(dataset):
	minvals = dataset.min(0)
	maxvals = dataset.max(0)
	ranges = maxvals - minvals
	normdataset = zeros(shape(dataset))
	m = dataset.shape[0]
	normdataset = dataset - tile(minvals, (m, 1))
	normdataset = normdataset/tile(ranges, (m, 1))
	return normdataset, ranges, minvals


def datingclasstest():
	horatio = 0.1
	datingdatamat, datingdatalabels = file2matrix('datingTestSet2.txt')
	normmat, ranges, minvals = autonorm(datingdatamat)
	m = normmat.shape[0]
	numtestvecs = int(m*horatio)
	errorcount = 0.0
	for i in range(numtestvecs):
		classifierresult = classify0(normmat[i,:], normmat[numtestvecs:m, :],
			datingdatalabels[numtestvecs:m], 3)
		print "the classifier came back with: %d, the real answer is: %d" % (
			classifierresult, datingdatalabels[i])
		if classifierresult != datingdatalabels[i]:
			errorcount += 1.0
	print 'the total error rate is: %f' %(errorcount/float(numtestvecs))




def classifyperson():
	resultlist = ['not at all', 'in small doses', 'in large doses']
	percentats = float(raw_input('percentage of time spent playing video games? >'))
	ffmiles = float(raw_input('frequent flier miles earned per year? >'))
	icecream = float(raw_input('liters of ice cream consmed per year? >'))
	datingdatamat, datingdatalabels = file2matrix('datingTestSet2.txt')
	normmat, ranges, minvals = autonorm(datingdatamat)
	inarr = array([ffmiles, percentats, icecream])
	classifierresult = classify0((inarr - minvals)/ranges, normmat, datingdatalabels, 3)
	print 'you will probably like this person: ', resultlist[classifierresult -1]

if __name__ == "__main__":
	datingdatamat, datingdatalabels = file2matrix('datingTestSet2.txt')
	normmat, ranges, minvals = autonorm(datingdatamat)

	classifyperson()

	import matplotlib
	import matplotlib.pyplot as plt 
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.scatter(normmat[:,0], normmat[:, 1], 
		15.0*array(datingdatalabels), 15.0*array(datingdatalabels))
	# ax.scatter(datingdatamat[:,0], datingdatamat[:, 1], 
	# 	15.0*array(datingdatalabels), 15.0*array(datingdatalabels))
	plt.show()

	datingclasstest()