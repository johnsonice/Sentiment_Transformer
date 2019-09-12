#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 15:39:22 2019

@author: chengyu
"""

## transform raw data to tsv

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os

def front_truncate(sentence,max_len=200):
    sen = sentence.split()
    l_sen = len(sen)
    if l_sen>max_len:
        sen = sen[-max_len:]
    
    sen = " ".join(sen)
    return sen
    
#%%

if __name__ == "__main__":
    #raw_data = "/home/chengyu/Dev/Sentiment_Transformer/data/authority_views/Authorities Views 20190703_Yoko_Chengyu_Harry_Comp.xlsx"
    #raw_data = "../data/authority_views/Authorities Views_training_v2.xlsx"
    for data_type in ['train','dev','test','test_buff']:
        #data_type = 'train'
        #data_type = 'authorities_views'
        raw_data = "../data/authority_views/{}.xlsx".format(data_type)
        
        df = pd.read_excel(raw_data)
        #%%
        label_column = 'label'
        text_column = 'paragraph'
        
        df = df[[text_column,label_column]]
        df[text_column] = df[text_column].str.replace('^[\d]+.\s','') ## clear begaining 
#        if 'buff' in data_type.lower():
#            df[text_column] = df[text_column].apply(front_truncate)
        #%%
        df['filter'] = df[label_column].map(lambda x: x in [-1,1,0,999])
        df= df[df['filter']][[text_column,label_column]]
        arr = df.index.to_numpy()
        if data_type == "train":
            out = np.random.permutation(arr) # random shuffle
            df = df.loc[out]
            
        ## turn labels to int
        df[label_column] = df[label_column].astype(int)
        #%%
        ## if you want to split train and test 
    #    n_train = int(len(df)*0.0)   ## change the ratio
    #    n_dev = int(len(df)*1.0)     ## change the ratio
    #    n_test = len(df) - n_train - n_dev
    #    #%%
    #    df_train = df[:n_train]
    #    df_dev = df[n_train:n_train+n_dev]
    #    df_test = df[-n_test:]
        #%%
        ## export 
        out_folder = "../data/authority_views"
        #df_train.to_csv(os.path.join(out_folder,'train.tsv'),index=False,sep='\t')
        df.to_csv(os.path.join(out_folder,'{}.tsv'.format(data_type)),index=False,sep='\t')
        #df_test.to_csv(os.path.join(out_folder,'test.tsv'),index=False,sep='\t')
    