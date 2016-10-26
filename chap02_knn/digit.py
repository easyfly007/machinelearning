from numpy import *
from dating import classify0
from os import listdir

def img2vector(filename):
	returnval = zeros((1, 1024))
	fr = open(filename)
	for i in range(32):
		linestr = fr.readline()
		for j in range(32):
			returnval[0, 32*i + j] = int(linestr[j])
	return returnval


def handwritingclasstest():
	hwlabels = []
	trainingfilelist = listdir('trainingDigits')
	m = len(trainingfilelist)
	trainingmat = zeros((m, 1024))
	for i in range(m):
		filenamestr = trainingfilelist[i]
		filestr = filenamestr.split('.')[0]
		classnumstr = int(filestr.split('_')[0])
		hwlabels.append(classnumstr)
		trainingmat[i, :] = img2vector('trainingDigits/%s' % filenamestr)
	testfilelist = listdir('testDigits')
	errorcount = 0.0
	mtest = len(testfilelist)
	for i in range(mtest):
		filenamestr = testfilelist[i]
		filestr = filenamestr.split('.')[0]
		classnumstr = int(filestr.split('_')[0])
		vectorundertest = img2vector('testDigits/%s' % filenamestr)
		classifierresult = classify0(vectorundertest, trainingmat,hwlabels, 3)
		print 'the classigier came back with: %d, the resl answer is: %d' %(
			classifierresult, classnumstr)
		if (classifierresult != classnumstr):
			errorcount += 1
	print '\n the total number of errors is: %d' %errorcount
	print '\n the total error rate is %f' %(errorcount/float(mtest))



if __name__ == "__main__":
	handwritingclasstest()



