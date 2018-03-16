# -*- coding: utf-8 -*-
"""
Spyder Editor


"""

import pandas as pd
from newspaper import Article


url = pd.read_csv(r'C:\Users\JJY\stock\NewsUrlall_cnn.csv')


articles = []
for date in url.columns:
    print(date)
    text =[]
    for post in url[date]:
        try:
            article = Article(post)
            article.download()
            article.parse()
            text.append(article.text)
            
        except:
            pass
    articles.append(text)
    #article.nlp()
    

        
        
Article_text = pd.DataFrame(articles)
Article_text = Article_text.T
Article_text.columns =[url.columns]
Article_text.to_csv('Articles_CNN.csv')



import nltk 
import pandas as pd
import numpy as np 
from nltk.stem.snowball import SnowballStemmer;from nltk import ngrams
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer; from sklearn import linear_model
from sklearn.cross_validation import KFold
from matplotlib import pyplot as plt;
from nltk.stem import WordNetLemmatizer
from nltk.corpus import sentiwordnet as swn
import re
#데이터 전처리

def isEnglish(s):
    try:
        s.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True
    
    
url = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"     
def textRe(s):
    s = re.sub(url, "",s)
    s = re.sub('\s\W',' ',s)
    s = re.sub('\W\s',' ',s)
    s = re.sub('\s+',' ',s)
    s = s.lower()
    return s

#비 영문 트윗, 디스크립션 제거    
data = pd.read_csv('Article_text')
target = pd.read_csv(r'C:\Users\jaeyoon\GoogleDrive\Stock\crawler\S&P500.csv')




#기사 텍스트 소문자 변환 및 처리
for x in data.columns:
    lowertext = [textRe(data[x][i]) for i in data[x].index]
    data[x] = lowertext
        
#stopwords 제거
from nltk.corpus import stopwords
stop = stopwords.words('english')
tokens=[]
##
for i in text.index:
    token = nltk.tokenize.word_tokenize(text[i])
    tokens.append(token)
tokens_stop=[]
for x in tokens:
    z = []
    for i in x:
        if i not in stop:
            z.append(i)
    tokens_stop.append(z)

# -------------- Remove stopwords complete ----------------------

import pysentiment as ps





stemmer=SnowballStemmer("english",ignore_stopwords=True)
stemming = [[stemmer.stem(y) for y in list1] for list1 in tokens_stop]
countvectorizer=CountVectorizer()

vectorizer= TfidfVectorizer()

doc=[]
for x  in stemming:
    result =  " ".join(x)
    doc.append(result)
tf=countvectorizer.fit_transform(doc)




#감정 사전 만들기 text
words=pd.DataFrame(tf.toarray())
score=data['gender']
final_lasso = linear_model.Lasso(alpha=0.0005)
final_lasso.fit(words, score)
fea_score=[[feature,coef] for feature, coef in zip(list(countvectorizer.get_feature_names()),list(final_lasso.coef_))]
fea_score=pd.DataFrame(np.array(fea_score))
fea_score.columns=['feature','sen_score']
fea_score['sen_score']=pd.to_numeric(fea_score['sen_score'])
fea_score=fea_score[(fea_score['sen_score']>0)|(fea_score['sen_score']<0)]
fea_score
dic_score_text=[]
for x in stemming:
    xscore=0
    for i in x:
        if i in list(fea_score['feature']):
            xscore+= list(fea_score['sen_score'])[list(fea_score['feature']).index(i)]    
    dic_score_text.append(xscore)
data['dic_text'] = dic_score_text
