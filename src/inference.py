#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 22:37:12 2019

@author: chengyu
"""


import torch
import argparse
from pytorch_transformers import *
from utils_glue import (compute_metrics, convert_examples_to_features,
                        output_modes, processors)
from torch.utils.data import (DataLoader, RandomSampler, SequentialSampler,
                              TensorDataset)
from run_glue import load_and_cache_examples
import numpy as np
from args_util import parse_args,MODEL_CLASSES
import torch.nn.functional as F
from tqdm import tqdm, trange
import pandas as pd
import os 
#%%

def load_custom_examples(args, task, tokenizer, custom_file_path= '../data/authority_views/dev.tsv'):
    
    if not isinstance(custom_file_path,str) or not '.tsv' in custom_file_path:
        raise Exception('-----please provide path for proper tsv file with title column.-----')
    
    processor = processors[task]()
    output_mode = output_modes[task]
    # Load data features from cache or dataset file

    label_list = processor.get_labels()
    examples = processor.get_custom_examples(custom_file_path)
    features = convert_examples_to_features(examples, label_list, args.max_seq_length, tokenizer, output_mode,
        cls_token_at_end=bool(args.model_type in ['xlnet']),            # xlnet has a cls token at the end
        cls_token=tokenizer.cls_token,
        sep_token=tokenizer.sep_token,
        cls_token_segment_id=2 if args.model_type in ['xlnet'] else 1,
        pad_on_left=bool(args.model_type in ['xlnet']),                 # pad on the left for xlnet
        pad_token_segment_id=4 if args.model_type in ['xlnet'] else 0)

    # Convert to Tensors and build dataset
    all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
    all_input_mask = torch.tensor([f.input_mask for f in features], dtype=torch.long)
    all_segment_ids = torch.tensor([f.segment_ids for f in features], dtype=torch.long)
    if output_mode == "classification":
        all_label_ids = torch.tensor([f.label_id for f in features], dtype=torch.long)
    elif output_mode == "regression":
        all_label_ids = torch.tensor([f.label_id for f in features], dtype=torch.float)

    dataset = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_label_ids)
    return dataset,examples

#%%
if __name__ == "__main__":
    ## load all args 
    args = parse_args()
    task = 'AIV'
    mode = 'test'# or inference
    eval_task = task.lower()
    data_dir = '../data/authority_views/'
    ##########################################################
    # specify file names
    if mode == 'inference':
        test_file_path = os.path.join(data_dir,'authorities_views.tsv')
        res_file_path = os.path.join(data_dir,'authorities_views.csv')
    else:
        test_file_path = os.path.join(data_dir,'test_buff.tsv')
        res_file_path = os.path.join(data_dir,'test_buff.csv')
    ##########################################################
    output_mode = output_modes[task.lower()]
    batch_size = 8
    ## set model cuda setting
    device = torch.device("cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu")
    args.device = device
    
    #%%
    ## load model 
    save_model_path = args.output_dir  ## where model is saved
    config_class, model_class, tokenizer_class = MODEL_CLASSES[args.model_type]
    model = model_class.from_pretrained(save_model_path)
    tokenizer = tokenizer_class.from_pretrained(save_model_path)
    model.to(device)
    #%%
    processor = processors[args.task_name.lower()]()
    label_list = processor.get_labels()
    label_map = {label : i for i, label in enumerate(label_list)}
    id2label_map = {i : label for i, label in enumerate(label_list)}
    
    #%%
#   load_and_cache_examples
    eval_dataset,examples = load_custom_examples(args, eval_task, tokenizer, custom_file_path=test_file_path)
    args.eval_batch_size = args.per_gpu_eval_batch_size
    # Note that DistributedSampler samples randomly
    eval_sampler = SequentialSampler(eval_dataset)
    #eval_dataloader = DataLoader(eval_dataset, sampler=eval_sampler, batch_size=args.eval_batch_size)
    eval_dataloader = DataLoader(eval_dataset, sampler=eval_sampler, batch_size=batch_size)
    
    
    #%%
    ## initiate results as None
    preds_logits = None
    ## set model to eval # to that dropout batch normalization does not apply
    model.eval()
    for batch in tqdm(eval_dataloader, desc="Evaluating"):
        
        batch = tuple(t.to(args.device) for t in batch)
        inputs = {'input_ids':      batch[0],
                  'attention_mask': batch[1],
                  'token_type_ids': batch[2] if args.model_type in ['bert', 'xlnet'] else None,  # XLM don't use segment_ids
                  'labels':         batch[3]}
        with torch.no_grad():
            outputs = model(**inputs)
            tmp_eval_loss, logits = outputs[:2]
            probs = F.softmax(logits,dim=1)
            values, max_id = torch.max(logits, dim=1)
            
        if preds_logits is None:
            preds_logits = logits.detach().cpu().numpy()
            preds_probs = probs.detach().cpu().numpy()
            pred_label_ids = max_id.detach().cpu().numpy()
            out_label_ids = inputs['labels'].detach().cpu().numpy()
        else:
            preds_logits = np.append(preds_logits,logits.detach().cpu().numpy(), axis=0)
            preds_probs = np.append(preds_probs,probs.detach().cpu().numpy(),axis=0)
            pred_label_ids = np.append(pred_label_ids,max_id.detach().cpu().numpy(),axis=0)
            out_label_ids = np.append(out_label_ids,inputs['labels'].detach().cpu().numpy(), axis=0)
    
    ## clear model in memory
    del model,eval_dataloader
    
    #%%
    ## organize output formate 
    p0,p1,p2,p3 = map(list, zip(*preds_probs))
    
    #%%
    true_ids = [id2label_map[i] for i in out_label_ids]
    pred_ids = [id2label_map[i] for i in pred_label_ids]
    org_text = [e.text_a for e in examples]
    output_data = zip(org_text,true_ids,p0,p1,p2,p3,pred_ids)
    df = pd.DataFrame(output_data,columns=['text','true_labels',
                                           id2label_map[0],
                                           id2label_map[1],
                                           id2label_map[2],
                                           id2label_map[3],
                                           'pred_ids'])
    df.to_csv(res_file_path,encoding='utf8')
    check = df['true_labels'] == df['pred_ids']
    accuracy = sum(check)/len(check)
    print("accuracy: {:.2%}".format(accuracy))
