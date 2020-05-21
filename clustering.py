#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 15:25:40 2018

@author: wenmi
"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import nltk.stem
import os
global para1
global para2
global size
global k_size
k_size=5

def sum_produce(sum_name,simi2,text):
    global para1
    global para2
    sentence_index=simi2[1][0]
    size=0
    i=0
    i_pre=0
    simi3=[]
    simi3.append(simi2[0])
    while (i<(len(simi2)-1)):
        i=i+1
        if (simi2[i_pre][1]-simi2[i][1]>para1):
                simi3.append(simi2[i])
                i_pre=i
        else:
            pass
    for i in range(len(simi3)):
        sentence_index=simi3[i][0]
            
        with open(sum_name,'a') as f:
            f.write(text[sentence_index]+'\n')
        size = os.path.getsize('/Users/wenmi/Desktop/未命名文件夹/车光阳个人文件/大三学校课程/数据挖掘/期末大作业/d30033t/data/'+sum_name)
        if size>para2:
            with open(sum_name,'wt') as f:
                f.write('')
            for j in range(i):
                sentence_index=simi3[j][0]
                with open(sum_name,'a') as f:
                    f.write(text[sentence_index]+'\n')
            break

def tf_idf(test):
    X = vectorizer.fit_transform(test)
    X_test=X.toarray()
    

    transformer = TfidfTransformer(smooth_idf=False)
    X_tfidf = transformer.fit_transform(X_test).toarray()
    #y=[X_test,X_tfidf]
    return X_tfidf

def cosine_simi(v1, v2):
    dot_product = 0.00000000
    normA = 0.00000000
    normB = 0.00000000
    for i in range(len(v1)):
        dot_product+=(v1[i])*(v2[i])
        normA+=pow(v1[i],2)
        normB+=pow(v2[i],2)
    y1=round(dot_product / ((pow(normA,0.5))*(pow(normB,0.5))),8)
    return y1

from random import randint
import xlwt



data_org=tf_idf_list.copy()



size=len(data_org)
def distance(a,b,q):
    length=len(a)
    d=0
    d_sum=0
    
    for i in range(length):
        d_sum=d_sum+(a[i]-b[i])**q
    
    d=pow(d_sum,1/q)
    return d
data_distance=[[-1]]*len(data_org)
for i in range(len(data_org)):
    for j in range(len(data_org)):
        if data_distance[i][0]<0:
            data_distance[i][0]=distance(data_org[i],data_org[j],2)
        else:
            data_distance[i].append(distance(data_org[i],data_org[j],2))
            
data_zhongjian=data_distance[0]

for i in range(len(data_org)):
    data_distance[i]=data_zhongjian[i*len(data_org):(i+1)*len(data_org)]
print('data addressed')
data_record=[]
for i in range(len(data_org)):
    data_record.append({"last":-1,"next":-1,"flag":0})

def belong(a,x,data_distance):#x是中心点列表，a是待划分的点
    t=10000
    point=-1
    for i in range(len(x)):
        if data_distance[a][x[i]]<t:
            t=data_distance[a][x[i]]
            point=x[i]
    return point

def cost(a,b,x,data_distance,data_record):
    sum=0
    y=x.copy()
    for i in range(k_size):
        if y[i]==a:
            y[i]=b
    for i in range(len(data_distance)):
        sum=sum+(data_distance[i][belong(i,y,data_distance)]-data_distance[i][data_record[i]['next']])
    return sum

def record_update(x,data_record,data_distance):
    for i in range(size):
        data_record[i]['last']=data_record[i]['next']
        data_record[i]['next']=belong(i,x,data_distance)
        if i in x:
            data_record[i]['flag']=0
        else:
            data_record[i]['flag']=1
            
            
        

x=[]
for i in range (k_size):
    x.append(randint(0,size))

record_update(x,data_record,data_distance)

y=x.copy()

cost_next=-1000
cost_last=1000
cost_change=cost_last-cost_next
times=0
point_last=-1
point_replace=-1
min=10000000000000
while (times<10):
    
    times+=1
    min=10000000000000
    for i in range(k_size):
        for j in range(size):
            if data_record[j]['flag']==1:
                if cost(x[i],j,x,data_distance,data_record)<min:
                    point_replace=j
                    point_last=x[i]
                    min=cost(x[i],j,x,data_distance,data_record)
    
    cost_next=min
    cost_change=cost_next-cost_last
    cost_last=min
    
    for i in range(k_size):
        if x[i]==point_last:
            x[i]=point_replace
            
    record_update(x,data_record,data_distance)
    print(times,'iterations',' ','cost_change is ',cost_change)
print('最终的簇中心点为')
for i in range(k_size):
    print (x[i],' ')
for i in range(len(data_record)):
    data_record[i]['flag']=i
#以上根据处理得到的数据,每个句子的tf_idf，进行聚类k-mediods算法
#最后的结果是x保存着3个簇中心的index,以及data_record，保存着每个短句的所属类



sentence_clustering_index=[]
sentence_clustering_contents=[]
sentence_clustering_tf_idf_total=[]
for i in range(k_size):
    test=[]
    contents=[]
    for j in range(size):
        if data_record[j]['next']==x[i]:
            test.append(data_record[j]['flag'])
            contents.append(text[data_record[j]['flag']])
    sentence_clustering_index.append(test)
    contents=' '.join(contents)
    sentence_clustering_contents.append(contents)
    
for i in range(k_size):
    sentence_clustering_tf_idf=tf_idf(sentence_clustering_contents)
    test=[]
    for j in range(len(sentence_clustering_tf_idf)):
        test.append(list(sentence_clustering_tf_idf[j]))
    sentence_clustering_tf_idf_total=test
#将属于每个类的短句的index取出来，存在sentence_clustering_index
#每一类的文本内容存在contents里面
#每一簇看成一个小长句，得到的tf_idf存在sentence_clustering_tf_idf_total

simi1=[]
for i in range(k_size):
    test=[]
    for j in range(len(sentence_clustering_index[i])):
        test.append((sentence_clustering_index[i][j],cosine_simi(tf_idf_list[sentence_clustering_index[i][j]],sentence_clustering_tf_idf_total[i])))
    test1=sorted(test,key=lambda simi: simi[1],reverse=True)
    simi1.append(test1)
#首先获得每个簇和内部的句子的相似度矩阵并且排序，结果放在simi1当中

simi2=[]
for i in range(k_size):
    simi2.append((i,cosine_simi(tf_idf_total_list,sentence_clustering_tf_idf_total[i])))
simi3=sorted(simi2,key=lambda simi: simi[1],reverse=True)
#获得每个簇整个长句子的相似度矩阵并且排序，结果放在simi3当中


sum_index=[]
flag=1
k=10
while(k):
    k=k-1
    for i in range(k_size):
        if (len(simi1[simi3[i][0]])>0):
            sum_index.append(simi1[simi3[i][0]].pop(0))
        else:
            pass
        
    for i in range(k_size):
        flag+=len(simi1[i])
#按照对应方法取出需要的句子的index 存在sum_index中

text_sum=[]
for i in range(len(text)):
    text_sum.append(' '.join(text[i].split('\n')))
#对原来的text进行简单的处理，去掉每个句子中多余的换行符号

sum_name='sum2'
para1=0
para2=665
sum_produce(sum_name,sum_index,text_sum)

