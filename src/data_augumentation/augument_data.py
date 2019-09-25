#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 21:59:31 2019

@author: chengyu
"""
import argparse
from backtranslation_util import Back_translator
import pandas as pd
#%%
def parse_args():

    parser = argparse.ArgumentParser()
    ## Required parameters
    parser.add_argument("--data_dir", default='../../data/authority_views/train.xlsx', type=str, required=False,
                        help="The input data dir.")
    parser.add_argument("--mode", default='google', type=str, required=False,
                        help="Whcih translation client you want to use")
    parser.add_argument("--task", default='backtranslate', type=str, required=False,
                        help="backtranslate or test")
    parser.add_argument("--output_dir", default="../../data/authority_views/train_aug.xlsx", type=str, required=False,
                        help="The output directory where the data will be saved.")
    parser.add_argument("--repet_n", default=5, type=int, required=False,
                        help="number of time you want to repet")
    
    args = parser.parse_args()
    
    return args

def unit_test():
    
    BT = Back_translator(mode=args.mode)
    test = '''Policy support, strengthening external demand,  \
            and supply-side reforms have helped maintain strong growth which, \
            along with tighter enforcement of capital flow management measures, \
            has also reduced exchange rate pressure. Regulators have recently focused \
            on addressing financial sector risks, resulting in tightening financial conditions. \
            The five-yearly Communist Party Congress is scheduled for the fall.'''
    print(test)

    res = BT.back_translate(test,rep_n = 10,unique=True)
    print(res)

if __name__ =="__main__":
    args = parse_args()
    if args.task == 'test':
        unit_test()
    else:
        df = pd.read_excel(args.data_dir)
        #pars = df['paragraph'].values.tolist()
        BT = Back_translator(mode=args.mode)
        #df = df[:5]
        
        data = df[['paragraph','label']].values.tolist()
        res_overall = []
        for idx,vals  in enumerate(data):
            print(idx)
            para,label = vals
            temp_aug_data = BT.back_translate(para,rep_n =args.repet_n,unique=False)
            temp_ps = [para]*len(temp_aug_data)
            temp_ls = [label]*len(temp_aug_data)
            res_overall.extend(list(zip(temp_ps,temp_aug_data,temp_ls)))
            #df['aug_paras']= df['paragraph'].apply(BT.back_translate,args=(5,False))
        
        res_df = pd.DataFrame(res_overall,columns = ['org_paragraph','paragraph','label'])
        #res_df['label'] = res_df['label'].astype(int)

        res_df.to_excel(args.output_dir)
    
