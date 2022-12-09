# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 20:18:07 2020

@author: cvicentm
"""
from tqdm import tqdm
import pandas as pd
import numpy as np
# mis importaciones
from modules.pre import create_corpus as c

def more_important_words_by_day(dic_subtitles,corpus,id2word,model,day):
    """model is tfidf model"""
    
    results=[]
    for doc in tqdm(model[corpus]):
        results.append([[id2word[num],freq] for num, freq in doc])
    
    sort_results=[]
    for result in tqdm(results):
        df_result = pd.DataFrame(result)
        sort_results.append(df_result.sort_values(1,ascending=False).values.tolist())
    
    #sort_vector= vector.sort_values(1,ascending=False) 
    #.sort(reverse=True) 
    dates = []
    for subtitle in tqdm(list(dic_subtitles.keys())):
        dates.append(c.get_date(subtitle))
    
    final_df=pd.DataFrame(list(dic_subtitles.keys()),dates).reset_index()
    select_index_from_day=list(final_df.loc[final_df['index'] == day].index)
    tfidf_day=[(list(dic_subtitles.keys())[idx],sort_results[idx]) for idx in select_index_from_day]
    
    list_word_day = []
    list_word_day = [word for document in tfidf_day for word,num in document[1]]
    list_word_day = list(dict.fromkeys(list_word_day))
    
    miw_day = np.zeros((len(list_word_day),len(tfidf_day)))
    
    for i in tqdm(range(len(tfidf_day))):
        df = pd.DataFrame(tfidf_day[i][1])
        for j in range(len(list_word_day)):
            try:
                if len(df.loc[df[0]==list_word_day[j]][1])!=0:
                    miw_day[j][i]=float(df.loc[df[0]==list_word_day[j]][1])
            except Exception as e:
                pass
    
    tfidf_result = pd.DataFrame(list_word_day)
    
    for i in range(np.shape(miw_day)[1]):
        tfidf_result.insert(i+1,tfidf_day[i][0],miw_day[:,i])
        
    tfidf_result['sum'] = tfidf_result.sum(axis=1)
    
    tfidf_result = tfidf_result.sort_values("sum",ascending=False)
    
    return tfidf_result

def remove_less_important_words(corpus_tfidf, percent):
    
    "this function remove all the words in a document which are not over the average level"
    
    corpus_tfidf_filtered = []
    for corp in corpus_tfidf:
        dic_corp = dict(corp) 
        avg = np.percentile(np.array(list(dic_corp.values())), percent)
        newDict = dict(filter(lambda elem: elem[1] > avg, dic_corp.items()))
        corp_new = list(newDict.items())
        corpus_tfidf_filtered.append(corp_new)
        
    return corpus_tfidf_filtered

def train_tfidf(corpus, rm = 0, per=50):
    from gensim.models import TfidfModel
    
    tfidf = TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    if rm == 0:
        return corpus_tfidf, tfidf
    else:
        corpus_tfidf_rm = remove_less_important_words(corpus_tfidf, per)
        return corpus_tfidf_rm, tfidf