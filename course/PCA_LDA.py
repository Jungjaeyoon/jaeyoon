import numpy as np
from numpy import linalg as LA
from sklearn import datasets
from sklearn import decomposition
from sklearn.lda import LDA
import matplotlib.pyplot as plt


#PCA, LDA codes using numpy

#class LDA
class LDa:
    def __init__(self,x,y):
        self.x= x
        self.y= y
        self.class_means= [np.mean(x[y==z],axis=0) for z in set(y)]
        self.mean = np.mean(x,axis=0)
        self.n_feature = len(x[0])
        
        n=self.n_feature
        scatter_matrix = np.zeros((n,n))
        for target,mv in zip(list(set(self.y)), self.class_means):
            sc = np.zeros((n,n))
            for row in self.x[self.y == target]:
                row, mv = row.reshape(n,1), mv.reshape(n,1) 
                sc += np.dot((row-mv),(row-mv).T) 
            scatter_matrix += sc 
            
        between_class_scatter = np.zeros((n,n))
        for i,class_mean in zip(range(len(self.class_means)),self.class_means):
            N = self.x[self.y==i,:].shape[0]
            mean =self.mean.reshape(n,1)
            class_mean = class_mean.reshape(n,1)
            between_class_scatter += N * np.dot((class_mean - mean),((class_mean - mean).T))

        evl, evec = LA.eig(np.dot(LA.inv(scatter_matrix_w),(between_class_scatter)))
        self.evl= evl
        
        
    def transform(self,n_components):
        lda = np.dot(self.x,evec)  
        return lda[:,0:n_components]

    def explained_variance_ratio(self):
        return [x/sum(self.evl) for x in self.evl ]
 
    


#class PCA   
class PCa:
	def __init__(self,data):
		self.basedata = data
		self.mean0data = data - data.mean(axis=0)
		self.covx = np.cov(self.mean0data.T)

	def explained_variance_ratio(self):
		evl, evec = LA.eig(self.covx)
		return [x/sum(evl) for x in evl ]

	def explained_variance(self):
		evl, evec = LA.eig(self.covx)
		return evl

	def transform(self,n_components):
		if n_components > len(self.basedata[0]) or n_components < 0:
			return 'error'
		evl, evec = LA.eig(self.covx)
		x_pca = np.dot(self.mean0data,evec)
		return x_pca[:,0:n_components]






a=PCa(x)
x_pcaH=a.transform(n_components= 4)
print("-----------------------------------------")
print("explained_variance - of homework PCA")
print(a.explained_variance())
print("-----------------------------------------")
print("explained_variance_ratio - of homework PCA")
print(a.explained_variance_ratio())

#package PCA
pca = decomposition.PCA(n_components=4)
pca.fit(x)
x_pcaP=pca.transform(x)
print("-----------------------------------------")
print("explained_variance - of package PCA")
print(pca.explained_variance_)
print("-----------------------------------------")
print("explained_variance_ratio - of package PCA")
print(pca.explained_variance_ratio_)
print("-----------------------------------------")

#homework LDA

b = LDa(x,y)
x_ldaH = b.transform(n_components = 4)
print("explained_variance_ratio - of homework LDA")
print(b.explained_variance_ratio())
print("-----------------------------------------")


#package LDA
lda = LDA(n_components=4,store_covariance=True)
lda.fit(x,y)
x_ldaP =lda.transform(x)



plt.scatter(x_pcaH[:,0],x_pcaH[:,1],c=y)
plt.show()


plt.scatter(x_pcaP[:,0],x_pcaP[:,1],c=y)
plt.show()






plt.scatter(x_ldaH[:,0],x_ldaH[:,1],c=y)
plt.show()


plt.scatter(x_ldaP[:,0],x_ldaP[:,1],c=y)
plt.show()
