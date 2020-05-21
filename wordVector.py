#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  6 10:52:38 2018

@author: wenmi
"""

from nltk.tokenize import WordPunctTokenizer  
from nltk.stem.lancaster import LancasterStemmer 
import gensim 
import os
lancaster_stemmer = LancasterStemmer() 
global para1
global para2
para2=665
para1=0

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

def sum_produce(sum_name,simi2,text,sentence_vector1):
#    with open(filename,'w') as f: 
#        f.write("I am Meringue.\n")
#        f.write("I am now studying in NJTECH.\n")
    global para1
    global para2
    sentence_index=simi2[1][0]
    flag=1
    size=0
    i=0
    i_pre=0
    simi3=[]
    simi3.append(simi2[0])
    
    while (i<(len(simi2)-1)):
        i=i+1
        for j in range(len(simi3)):
            if (cosine_simi(sentence_vector1[simi2[i][0]],sentence_vector1[simi3[j][0]])>para1):
                flag=1
            else:
                flag=0
                break
        if flag==1:
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

text1=[]
for i in range(len(text)):
    words = WordPunctTokenizer().tokenize(text[i])
    text1.append(words)
#分词获得一个list

for ele in text1:
    for i in range(len(ele)):
        ele[i]=lancaster_stemmer.stem(ele[i])
#词干化处理

model0 = gensim.models.Word2Vec(text1)   
model0.save('word2vector_model')
model1 = gensim.models.Word2Vec.load('word2vector_model') 
#词向量训练，得到模型model1

sentence_vector=[]
for ele in text1:
    sum=0
    for i in range(len(ele)):
        try:
            c=model1[ele[i]]#可以直接从model里面读取每个词语的向量值
            sum+=c
        except KeyError:
            pass
    sentence_vector.append(sum)
sentence_vector1=[]
for i in range(len(sentence_vector)):
    sentence_vector1.append(list(sentence_vector[i]))
#从model里面读取每个词语的向量值，针对每个句子，简单加和得到句向量
#存放在sentence_vector1里面


sentence_vector_total=sentence_vector1[0].copy()
for j in range(len(sentence_vector1)):
    if (j!=0):
        for i in range(len(sentence_vector_total)):
            sentence_vector_total[i]+=sentence_vector1[j][i]
    else:
        pass
#整个文档看成一个句子的句向量，存在sentence_vector_total

simi=[]
for i in range(len(text)):
    simi.append(cosine_simi(sentence_vector1[i],sentence_vector_total))
simi1=[]
for i in range(len(simi)):
    simi1.append((i,simi[i]))
#计算短句和大长句的相似度
#并且将短句和对应的simi值相关联，存在一个tuple当中，一起放在一个list当中

simi2=sorted(simi1,key=lambda simi: simi[1],reverse=True)
#对simi进行降序排序

#simi3=[]
#for i in range(len(sentence_vector1)):
#    test=[]
#    for j in range(len(sentence_vector1)):
#        test.append(cosine_simi(sentence_vector1[i],sentence_vector1[j]))
#    simi3.append(test)

text_sum=[]
for i in range(len(text)):
    text_sum.append(' '.join(text[i].split('\n')))
#对原来的text进行简单的处理，去掉每个句子中多余的换行符号
para2=665
sum_name='sum3_1'
para1=0
sum_produce(sum_name,simi2,text_sum,sentence_vector1)

sum_name='sum3_2'
para1=0.99998
sum_produce(sum_name,simi2,text_sum,sentence_vector1)

sum_name='sum3_3'
para1=0.999985
sum_produce(sum_name,simi2,text_sum,sentence_vector1)

sum_name='sum3_4'
para1=0.99999
sum_produce(sum_name,simi2,text_sum,sentence_vector1)
#para1仍然是阈值



