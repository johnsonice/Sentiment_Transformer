# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 14:36:11 2019

@author: chuang
"""


## transform inference data to tsv

import pandas as pd
import numpy as np
#from sklearn.model_selection import train_test_split
import os

#%%

if __name__ == "__main__":
    #raw_data = "/home/chengyu/Dev/Sentiment_Transformer/data/authority_views/Authorities Views 20190703_Yoko_Chengyu_Harry_Comp.xlsx"
    #raw_data = "../data/authority_views/Authorities Views_training_v2.xlsx"
    file_name = 'authorities_views'
    raw_data = "../data/authority_views/{}.xlsx".format(file_name)
    df = pd.read_excel(raw_data)
    #%%
    ## specify data column name
    text_column = 'text'
    ## generate a fake label column
    label_column = 'label'
    df[label_column] = 0
    
    df = df[[text_column,label_column]]
    df[text_column] = df[text_column].str.replace('^[\d]+.\s','') ## clear begaining 
    df[text_column] = df[text_column].str.replace('\t',' ') ## replace \t # otherwise it will bug 
    df[label_column] = df[label_column].astype(int)

    #%%
    ## export 
    out_folder = "../data/authority_views"
    df.to_csv(os.path.join(out_folder,'{}.tsv'.format(file_name)),index=False,sep='\t')

    