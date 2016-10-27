from math import log
import operator


def calcshannonentropy(dataset):
	numentries = len(dataset)
	labelcounts = {}
	for featvec in dataset:
		currentlabel = featvec[-1]
		if currentlabel not in labelcounts.keys():
			labelcounts[currentlabel] = 0
		labelcounts[currentlabel] += 1
	shannonentropy = 0.0
	for key in labelcounts:
		prob = float(labelcounts[key])/numentries
		shannonentropy -= prob * log(prob, 2)
	return shannonentropy

def createdataset():
	dataset = [[1, 1, 'yes'],
		[1, 1, 'yes'],
		[1, 0, 'no'],
		[0, 1, 'no'],
		[0, 1, 'no']]
	labels = ['no surfacing', 'flippers']
	return dataset, labels

# split the dataset, get a new subset, which the asix feature with value
# the new dataset excluded the axis feature
def splitdataset(dataset, axis, value):
	retdataset = []
	for featvec in dataset:
		if featvec[axis] == value:
			reducedfeatvec = featvec[:axis]
			reducedfeatvec.extend(featvec[axis+1:])
			retdataset.append(reducedfeatvec)
	return retdataset


def choosebestfeaturetosplit(dataset):
	numfeatures = len(dataset[0]) -1
	baseentropy = calcshannonentropy(dataset)
	bestinfogain = 0.0
	bestfeature = -1
	for i in range(numfeatures):
		featlist = [example[i] for example in dataset]
		uniquevals = set(featlist)
		newentropy = 0.0
		for value in uniquevals:
			subdataset = splitdataset(dataset, i, value)
			prob = len(subdataset) / float(len(dataset))
			newentropy += prob * calcshannonentropy(subdataset)
		infogain = baseentropy - newentropy
		if infogain > bestinfogain:
			bestinfogain = infogain
			bestfeature = i
	return bestfeature


def majoritycnt(classlist):
	classcount= {}
	for vote in classlist:
		if vote not in classcount.keys():
			classcount[vote] = 0
		classcount[vote] += 1
	sortedclasscount = sorted(classcount.iteritems(), key=operator.itemgetter(1), reverse = True)
	return sortedclasscount[0][0]

def createtree(dataset, labels):
	classlist = [example[-1] for example in dataset]
	if classlist.count(classlist[0] == len(classlist)):
		# all the class are the same
		return classlist[0]
	if len(dataset[0]) ==1:
		return majoritycnt(classlist)
	bestfeature = choosebestfeaturetosplit(dataset)
	bestfeaulabel = labels[bestfeature]
	mytree = {bestfeaulabel:{}}
	del(labels[bestfeature])
	featvalues = [example[bestfeature] for example in dataset]
	uniquevals = set(featvalues)
	for value in uniquevals:
		sublabels = labels[:]
		mytree[bestfeaulabel][value] = createtree(splitdataset(dataset, bestfeature, value), sublabels)
	return mytree


import matplotlib.pyplot as plt 
decisionnode = dict(boxstyle = 'aswtooth', fc = '0.8')
leafnode = dict(boxstyle = 'round4', fc= '0.8')
arrow_args = dict(arrowstyle = "<-")
def plotnode(nodetxt, centerpt, parentpt, nodetype):
	createplot.ax1.annotate(nodetxt, xy=parentpt, xycoords = 'axes fraction', xytext=centerpt, textcoords = 'axes fraction', va = 'center', ha = 'center', bbox = nodetype, arowprops = arrow_args)

def createplot():
	fig = plt.figure(1, facecolor = 'white')
	fig.clf()
	createPlot.ax1 = plt.subplot(111, frameon = False)
	plotnode(U'decision point', (0.5, 0.1), (0.1, 0.5), decisionnode)
	plotnode(U'leaf node', (0.8, 0.1), (0.3, 0.8), leafnode)
	plt.show()