"""
Naive Bayes Model with Gaussian random variables
"""
import numpy as np

K = 10

def gaussian_learn(D):
	n = D.shape[1]
	X = D[:,:n-1]
	X0 = D[:,:n-1][D[:,n-1]==0]
	X1 = D[:,:n-1][D[:,n-1]==1]
	phi = len(X1)/float(len(D))
	mu,sigma = {},{}
	mu[0] = np.mean(X0, axis=0)
	mu[1] = np.mean(X1, axis=0)
	sigma[0] = fore_back_variance(X0,X)
	sigma[1] = fore_back_variance(X1,X)
	return phi,mu,sigma

def fore_back_variance(fX,bX):
	foreground = np.var(fX, axis=0)
	background = np.var(bX, axis=0)
	l = len(bX)/(len(bX)+2.0)
	return l * foreground + (1 - l) * background

def gaussian_pridect(X,phi,mu,sigma):
	return [gaussian_pridect_single(x,phi,mu,sigma) for x in X]

def gaussian_pridect_single(x,phi,mu,sigma):
	p0 = gaussian_prob(x,mu[0],sigma[0]) * (1-phi)
	p1 = gaussian_prob(x,mu[1],sigma[1]) * phi
	return 1 if p1 > p0 else 0

def gaussian_prob(x,mu,sigma):
	probs = [gaussian_prob_one(x[i],mu[i],sigma[i]) for i in range(len(x))]
	return np.prod(probs)

def gaussian_prob_one(x,mu,sigma):
	xx = np.exp(-0.5*((mu-mu)**2)/sigma)/np.sqrt(2*np.pi*sigma)
	return np.exp(-0.5*((x-mu)**2)/sigma)/np.sqrt(2*np.pi*sigma)

if __name__ == "__main__":
	print "============================================="
	print "loading spambase data..."
	spambase = np.loadtxt("../dataset/spambase/spambase.data", delimiter=",")
	np.random.shuffle(spambase)

	n = spambase.shape[1]
	train_errs = np.zeros(K)
	errs = np.zeros(K)

	k_folds = np.array_split(spambase,K)

	print "============================================="
	print "naive bayes classifier with %d folds cross-validation..." %K
	for i in range(K):
		print "iteration %d..." %i
		test = k_folds[i]
		train = np.vstack(np.delete(k_folds, i, axis=0))

		phi,mu,sigma = gaussian_learn(train) # mu is mean, sigma is variance
		y_test = gaussian_pridect(test[:,:n-1],phi,mu,sigma)
		errs[i] = np.mean((y_test-test[:,n-1])**2)
		y_train = gaussian_pridect(train[:,:n-1],phi,mu,sigma)
		train_errs[i] = np.mean((y_train-train[:,n-1])**2)
		print "train error: %f , test error: %f" %(train_errs[i], errs[i])
	print "the average train error rate is: %f" %np.mean(train_errs)
	print "the average test error rate is: %f" %np.mean(errs)
	print "============================================="