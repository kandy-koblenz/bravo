
# coding: utf-8

import pandas as pd
import numpy as np
import sys
from collections import  Counter
import math
import time

#import bravo_assignment8_q1_1 as q1

store=pd.HDFStore("store2.h5")
#print(text_df.shape)
corpus_size = 100
text_df = store['df1']
out_link_df=store['df2']


#text_df = text_df.iloc[0:corpus_size]
#print(text_df.head)
#out_link_df = out_link_df.iloc[0:corpus_size]

## random 100 and 100long articles
# following code creates a word set for each and every article
text_df['wordset']=text_df.text.map(lambda x: set(x.lower().split()))






#out_link_df_longest_article;



def calcJaccardSimilarity(wordset1, wordset2):
    wordset1=set(wordset1)
    wordset2=set(wordset2)
    inter=wordset1.intersection(wordset2)
    union=wordset1.union(wordset2)
    jc=(len(inter)/len(union))
    return jc
    

text_df['termfrequency']=text_df.text.map(lambda x: Counter(x.lower().split()).items())






# it goes through each article's wordset and find the document freq
def temp_docfreq_function(rows):
    dictofwords = {}
    
    for row in rows:
        #print(row)
        for word in row:
            if word in dictofwords:
                num=dictofwords[word]+1
            else:
                num=1
            dictofwords[word]=num

    return dictofwords

docFreqDict=temp_docfreq_function(text_df['wordset'])

d=len(text_df['name']) # row size

def temp_tfidf_function(wordHist):
    ##tf-idf= tf of word * (number of documents/df(word))
    numofdocs=d
    dictofwords = {}
    for word in wordHist:
        #word[0] - is the word (key)
        #word[1] - is the term freq value
        if word[0] in docFreqDict:
            #print(word)           
        
            df=docFreqDict[word[0]] # get the document frequency of that word
            idf=math.log((numofdocs/df),10) # calculate the idf
            tfidf=idf*word[1]  # calculate the tf-idf= tf(word)*idf(word)
            dictofwords[word[0]]=tfidf
                   
    return dictofwords

## creating a coulum tfidf for each word in an article
text_df['tfidf']=text_df.termfrequency.map(temp_tfidf_function)

def calculateCosineSimilarity(dict1, dict2):
    dotprod=0
    for k1 in dict1:
        if k1 in dict2.keys():
            dotprod=dotprod+(dict1[k1]*dict2[k1])
    
    dict1dot=0
    dict2dot=0
    
    for key1 in dict1:
        dict1dot=dict1dot+(dict1[key1]*dict1[key1])

    for key2 in dict2:
        dict2dot=dict2dot+(dict2[key2]*dict2[key2])
        
    if(dict1dot == 0 or dict2dot == 0):
        cosinesimilarity = 1
    else :
        cosinesimilarity=dotprod/((math.sqrt(dict1dot))*(math.sqrt(dict2dot)))    
    
    return (1 - cosinesimilarity) # we wanted to reverse it to compare it with jaccard coefficient
    
#print('---------------------------------------------------------------------')

#print(text_df['name'])
#print(out_link_df['name'])

germanJackardListRank = []
germanCosineSimilarityListRank = []
germanJackardListRank_links = []
germanRow = text_df[text_df['name']=='German']
germanRow_link = out_link_df[out_link_df['name']=='German']
j = 0



text_df_rand = pd.DataFrame(columns=text_df.columns)
out_link_df_rand = pd.DataFrame(columns=out_link_df.columns)

text_df['articleLength']=text_df.text.map(lambda x: len(x))
out_link_df['articleLength']=out_link_df.out_links.map(lambda x: len(x))
text_df_longest_article=text_df.sort_values(by='articleLength',ascending=[False])
out_link_df_longest_article=out_link_df.sort_values(by='articleLength',ascending=[False])


for i in range(0,100):
    idx = np.random.randint(0, text_df.shape[0])
    text_df_rand.loc[i] = text_df.loc[idx]
    out_link_df_rand.loc[i] =out_link_df.iloc[idx]


rows_count = text_df_rand.shape[0]

longestgermanJackardListRank = []
longestgermanCosineSimilarityListRank = []
longestgermanJackardListRank_links = []

rows_count=100

## for random artciles
while (j < rows_count):
    row = text_df_rand.iloc[j]
    out_link_row = out_link_df_rand.iloc[j]
    long_row=text_df_longest_article.iloc[j]
    long_out_link_row=out_link_df_longest_article.iloc[j]
  
    start_time = time.time()
    germanCosineSimilarityListRank.append(calculateCosineSimilarity(row['tfidf'], germanRow['tfidf'].iloc[0]))
    longestgermanCosineSimilarityListRank.append(calculateCosineSimilarity(long_row['tfidf'], germanRow['tfidf'].iloc[0]))
    end_time = time.time()
    germanJackardListRank.append(calcJaccardSimilarity(row['wordset'], germanRow['wordset'].iloc[0]))
    longestgermanJackardListRank.append(calcJaccardSimilarity(long_row['wordset'], germanRow['wordset'].iloc[0]))

    germanJackardListRank_links.append(calcJaccardSimilarity(out_link_row['out_links'], germanRow_link['out_links'].iloc[0]))
    longestgermanJackardListRank_links.append(calcJaccardSimilarity(long_out_link_row['out_links'], germanRow_link['out_links'].iloc[0]))

    j = j + 1
    #break




#rows_count = text_df_rand.shape[0]


   

print('time taken - ',(end_time - start_time))
    
#print(germanCosineSimilarityListRank)
#print(germanJackardListRank)

def kendalls_tau(list1, list2):
    score = 0
    con_pair = 0
    non_con_pair = 0
    
    length = len(list1)
    
    if(length > len(list2)) :
        length = len(list2)
    
    i = 0
    while(i < length) :
        j = i + 1
        while(j < length) :
            if(((list1[i] - list1[j]) * (list2[i] - list2[j])) >= 0):
                con_pair = con_pair + 1
            else:
                non_con_pair = non_con_pair + 1
            j = j + 1 
        i += 1
    
    score = (con_pair - non_con_pair) / (con_pair + non_con_pair)
    return score
print('*** for 100 random articles***')    
print('kendalls Tau score for text based cosine and jaccard similarity - ', kendalls_tau(germanCosineSimilarityListRank, germanJackardListRank))
print('kendalls Tau score for text based cosine and link based jaccard similarity - ', kendalls_tau(germanCosineSimilarityListRank, germanJackardListRank_links))
print('kendalls Tau score for text based jaccard and link based jaccard similarity - ', kendalls_tau(germanJackardListRank, germanJackardListRank_links))

print('*** for 100 longest articles***')

print('kendalls Tau score for text based cosine and jaccard similarity - ', kendalls_tau(longestgermanCosineSimilarityListRank, longestgermanJackardListRank))
print('kendalls Tau score for text based cosine and link based jaccard similarity - ', kendalls_tau(longestgermanCosineSimilarityListRank, longestgermanJackardListRank_links))
print('kendalls Tau score for text based jaccard and link based jaccard similarity - ', kendalls_tau(longestgermanCosineSimilarityListRank, longestgermanJackardListRank_links))


'''
for row in text_iterate:
    #print(row[0])
    #print(row[1].tfidf)
    print(type(germanRow['tfidf']))
    print(type(row[1]['tfidf']))
    germanListRank.append(calculateCosineSimilarity(germanRow['tfidf'], row[1]['tfidf']))
    #print(type(row))
    break
'''

