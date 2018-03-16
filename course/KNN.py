from sklearn import datasets
from math import sqrt
import numpy as np
import operator
from collections import Counter
import matplotlib.pyplot as plt

#KNN

#data samples
#classification data
iris=datasets.load_iris() 
x=iris['data']
target=iris['target']

#regression data
x=np.random.uniform(-4,4,200) 
x = np.sort(x)
target=np.sin(x)+np.random.normal(size=200,scale=0.4)
x = x.reshape(len(x),1)

#knn
def Knn(x,t_val,numneighbor,model):
  '''
  x : input data
  t_val : target data
  numneighbor : number of neighbor, lower numneighbor makes result local(소수의 가까운 애덜에 영향을 받음)
  model : regression or classification, depends on target data type
  
  '''
	target=t_val
	Euclideanx = []
	y_predict=[]
	for z in x:
		euclidex=[]
		for y in x:
			euclidex.append(sqrt(sum((z - y)**2)))
		k = [[x,y] for (x,y) in zip(x,euclidex)]
		kindex = { i:k[i][1] for i in range(len(k))}
		sorted_k = sorted(kindex.items(), key=operator.itemgetter(1), )
		neighbors = sorted_k[1:numneighbor+1]
		neighbors_y = [target[x[0]] for x in neighbors]
		counter= Counter(neighbors_y)

		if model=='classification':
			y_predict.append(counter.most_common()[0][0])
		elif model =='regression':
			y_predict.append(sum(neighbors_y)/len(neighbors_y))		
	return y_predict



#bagging for knn model

def bagging(x,y,bangbeob,model_parameter,n_estimate,max_features,numneighbor):
  '''
    x : input data
    y : target data
    bangbeob(이름바꿔야함) : knn
    model_parameter(model로 이름 변경해야함) : regression or classification, depends on target data type
    n_estimate : number of single model
    max_features : number of features for each single model
    numneighbor : number of neighbor for knn model
  '''
	if max_features <0 or max_features>1:	
		print('error')
	
  else:
		features = len(x)*max_features
		estimate_model_x=[]
		estimate_model_y=[]
		bagging_class ={i : [0 for i in set(y)] for i in range(len(x))}
		bagging_reg={i :0 for i in range(len(x))}
		sampleindexcounter={i :0 for i in range(len(x))}
		
    for i in range(n_estimate):
			sampleindex=(np.random.choice(len(x),features,replace=True))			
			samplex=[x[i] for i in sampleindex]
			sampley=[y[i] for i in sampleindex]
			estimate_model_x.append(samplex)
			baggingresult=bangbeob(samplex,sampley,numneighbor=numneighbor,model=model_parameter)
			estimate_model_y.append(baggingresult)
			
      for ind in range(len(sampleindex)):
				if model_parameter=="classification":
					bagging_class[sampleindex[ind]][baggingresult[ind]]+=1
				elif model_parameter=="regression":
					bagging_reg[sampleindex[ind]]+=baggingresult[ind]
					sampleindexcounter[sampleindex[ind]]+=1
		
    if model_parameter=="classification":		
			bagging_finish=[bagging_class[x] for x in bagging_class]
			bagging_predict=[x.index(max(x)) for x in bagging_finish]
			return bagging_predict, estimate_model_x, estimate_model_y
		
    elif model_parameter=="regression":
			try:
				bagging_finish=[bagging_reg[i]/sampleindexcounter[i] for i in range(len(x))]
			
      except ZeroDivisionError as e:
				e = 0 
			
      return bagging_finish,estimate_model_x,estimate_model_y

