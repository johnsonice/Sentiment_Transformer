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

#%%

if __name__ == "__main__":
    #raw_data = "/home/chengyu/Dev/Sentiment_Transformer/data/authority_views/Authorities Views 20190703_Yoko_Chengyu_Harry_Comp.xlsx"
    #raw_data = "../data/authority_views/Authorities Views_training_v2.xlsx"
    raw_data = "../data/authority_views/Authorities Views_best_test.xlsx"
    
    df = pd.read_excel(raw_data)
    df = df[['paragraph','Yoko_new']]
    df['filter'] = df['Yoko_new'].map(lambda x: x in [-1,1,0,999])
    df= df[df['filter']][['paragraph','Yoko_new']]
    arr = df.index.to_numpy()
    out = np.random.permutation(arr) # random shuffle
    df = df.loc[out]
    #%%
    n_train = int(len(df)*0.0)   ## change the ratio
    n_dev = int(len(df)*1.0)     ## change the ratio
    n_test = len(df) - n_train - n_dev
    #%%
    df_train = df[:n_train]
    df_dev = df[n_train:n_train+n_dev]
    df_test = df[-n_test:]
    #%%
    ## export 
    out_folder = "../data/authority_views"
    
    #df_train.to_csv(os.path.join(out_folder,'train.tsv'),index=False,sep='\t')
    df_dev.to_csv(os.path.join(out_folder,'dev.tsv'),index=False,sep='\t')
    #df_test.to_csv(os.path.join(out_folder,'test.tsv'),index=False,sep='\t')
    