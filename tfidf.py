#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 21:06:12 2018

@author: wenmi
"""
#        if (cosine_simi(tf_idf_list[simi2[i_pre][0]],tf_idf_list[simi2[i][0]])>para1):
#                simi3.append(simi2[i])
#                i_pre=i
#        else:
#            pass
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import nltk.stem
import os
global para1
para1=0.005
english_stemmer = nltk.stem.SnowballStemmer('english')
class StemmedCountVectorizer(CountVectorizer):
        def build_analyzer(self):
            analyzer = super(StemmedCountVectorizer, self).build_analyzer()
            return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

vectorizer = StemmedCountVectorizer(stop_words='english')


def data_pro(str_name):
    f=open(str_name,'r')
    test=f.read()
    f.close()
    test2=test.split('>')
    import nltk
    from nltk.tokenize import sent_tokenize  
    test6 = sent_tokenize(test2[8])
    test6.pop(-1)
    return test6

def tf_idf(test):
    X = vectorizer.fit_transform(test)
    X_test=X.toarray()
    transformer = TfidfTransformer(smooth_idf=False)
    X_tfidf = transformer.fit_transform(X_test).toarray()
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

def sum_produce(sum_name,simi2,text,tf_idf_list):
    global para1
    sentence_index=simi2[1][0]
    size=0
    i=0
    i_pre=0
    simi3=[]
    simi3.append(simi2[0])
    while (i<(len(simi2)-1)):
        i=i+1
        for j in range(len(simi3)):
            if (cosine_simi(tf_idf_list[simi2[i][0]],tf_idf_list[simi3[j][0]])>para1):
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
        if size>665:
            with open(sum_name,'wt') as f:
                f.write('')
            for j in range(i):
                sentence_index=simi3[j][0]
                with open(sum_name,'a') as f:
                    f.write(text[sentence_index]+'\n')
            break

text_name='/Users/wenmi/Desktop/未命名文件夹/车光阳个人文件/大三学校课程/数据挖掘/期末大作业/d30033t/data/APW19981127.0244'
text1=data_pro(text_name)
text_name='/Users/wenmi/Desktop/未命名文件夹/车光阳个人文件/大三学校课程/数据挖掘/期末大作业/d30033t/data/APW19981203.0649'
text2=data_pro(text_name)
text_name='/Users/wenmi/Desktop/未命名文件夹/车光阳个人文件/大三学校课程/数据挖掘/期末大作业/d30033t/data/APW19981203.1240'
text3=data_pro(text_name)
text_name='/Users/wenmi/Desktop/未命名文件夹/车光阳个人文件/大三学校课程/数据挖掘/期末大作业/d30033t/data/APW19981228.0189'
text4=data_pro(text_name)
text_name='/Users/wenmi/Desktop/未命名文件夹/车光阳个人文件/大三学校课程/数据挖掘/期末大作业/d30033t/data/APW19981229.0467'
text5=data_pro(text_name)
text_name='/Users/wenmi/Desktop/未命名文件夹/车光阳个人文件/大三学校课程/数据挖掘/期末大作业/d30033t/data/APW19981230.0431'
text6=data_pro(text_name)
text_name='/Users/wenmi/Desktop/未命名文件夹/车光阳个人文件/大三学校课程/数据挖掘/期末大作业/d30033t/data/APW19981230.0473'
text7=data_pro(text_name)
text_name='/Users/wenmi/Desktop/未命名文件夹/车光阳个人文件/大三学校课程/数据挖掘/期末大作业/d30033t/data/APW19981231.0143'
text8=data_pro(text_name)
text_name='/Users/wenmi/Desktop/未命名文件夹/车光阳个人文件/大三学校课程/数据挖掘/期末大作业/d30033t/data/NYT19981119.0380'
text9=data_pro(text_name)
text_name='/Users/wenmi/Desktop/未命名文件夹/车光阳个人文件/大三学校课程/数据挖掘/期末大作业/d30033t/data/NYT19981223.0347'
text10=data_pro(text_name)

text=text1+text2+text3+text4+text5+text6+text7+text8+text9+text10
text_total=[' '.join(text)]

#以上代码提取了每一篇文档，分句后放在一个list里面，最后text把所有的句子存入一个list
#text_total把所有的句子变成一个长句子
#方便下面的处理


X = vectorizer.fit_transform(text)
X_test=X.toarray()
transformer = TfidfTransformer(smooth_idf=False)
X_tfidf = transformer.fit_transform(X_test).toarray()
tf_idf=X_tfidf
t=tf_idf
tf_idf_list=[]
for i in range(len(t)):
    tf_idf_list.append(list(t[i]))


Y = vectorizer.fit_transform(text_total)
Y_test=X.toarray()
transformer = TfidfTransformer(smooth_idf=False)
Y_tfidf = transformer.fit_transform(Y_test).toarray()
tf_idf_total=Y_tfidf
#计算tf_idf矩阵
tf_idf_total_list=list(tf_idf_total[0])
#将tf_idf的array转成list模式方便处理

simi=[]
for i in range(len(text)):
    simi.append(cosine_simi(tf_idf_list[i],tf_idf_total_list))
simi1=[]
for i in range(len(simi)):
    simi1.append((i,simi[i]))
#计算短句和长句的相似度
#并且将短句和对应的simi值相关联，存在一个tuple当中，一起放在一个list当中

simi2=sorted(simi1,key=lambda simi: simi[1],reverse=True)
#对simi进行降序排序

#simi3=[]
#for i in range(len(tf_idf_list)):
#    test=[]
#    for j in range(len(tf_idf_list)):
#        test.append(cosine_simi(tf_idf_list[i],tf_idf_list[j]))
#    simi3.append(test)
    

text_sum=[]
for i in range(len(text)):
    text_sum.append(' '.join(text[i].split('\n')))
#对原来的text进行简单的处理，去掉每个句子中多余的换行符号


sum_name='sum1_1'
para1=0
sum_produce(sum_name,simi2,text_sum,tf_idf_list)
sum_name='sum1_2'
para1=0.1
sum_produce(sum_name,simi2,text_sum,tf_idf_list)
sum_name='sum1_3'
para1=0.05
sum_produce(sum_name,simi2,text_sum,tf_idf_list)
sum_name='sum1_4'
para1=0.01
sum_produce(sum_name,simi2,text_sum,tf_idf_list)
#生成summary，根据不同的相似度阈值，生成了4个摘要，para1作为全局变量

with open('sum0','a') as f:
    f.write(text1[0])
    f.write(text2[0])
    f.write(text3[0])
    f.write(text4[0])
    f.write(text5[0])
    f.write(text6[0])
    f.write(text7[0])
    f.write(text8[0])
    f.write(text9[0])
    f.write(text10[0])
#baseline方法，把每个文档第一句拿出来，形成摘要
