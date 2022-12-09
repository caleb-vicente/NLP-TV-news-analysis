# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 09:41:07 2020

@author: cvicentm
"""

from modules.sql import dBAdapter
from modules.pre import create_corpus as c
from nltk import sent_tokenize

n_documents = 4

#----------------------------------------------------------------------------
print("Getting body subtitles from the database started ...")
dbAdapter= dBAdapter.Database()
dbAdapter.open()
dic_subtitles = dict(dbAdapter.selectDic_subtitles_limit(n_documents))
dbAdapter.close()
print("finalizada consulta")

string = sent_tokenize(list(dic_subtitles.values())[0])

from sumy.parsers.plaintext import PlaintextParser
#for tokenization
from sumy.nlp.tokenizers import Tokenizer

parser = PlaintextParser.from_string(list(dic_subtitles.values())[0], Tokenizer("spanish"))


from sumy.summarizers.lsa import LsaSummarizer
summarizer_2 = LsaSummarizer()
summary_2 =summarizer_2(parser.document,10)
summ_list=[]
for sentence in summary_2:
    summ_list.append(sentence._text)
summ_text = " ".join(summ_list)