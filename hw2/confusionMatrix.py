import numpy as np

def confusionMatrix(predicted,labels):
	total = len(labels)
	tp,fp,tn,fn = 0,0,0,0
	for i in range(total):
		if predicted[i] == 1:
			if labels[i] == 1:
				tp += 1
			else:
				fp += 1
		else:
			if labels[i] == 1:
				fn += 1
			else:
				tn += 1
	tpr = tp/float(tp+fn)
	fpr = fp/float(fp+tn)
	tnr = tn/float(tn+fp)
	fnr = fn/float(fn+tp)
	return np.array([tpr,fpr,tnr,fnr])
