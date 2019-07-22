#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 22:37:12 2019

@author: chengyu
"""


import torch
from pytorch_transformers import *
from utils_glue import (compute_metrics, convert_examples_to_features,
                        output_modes, processors)

#%%
save_model_path ='../data//model_weights/AIV/'
model = model_class.from_pretrained(save_model_path)
tokenizer = tokenizer_class.from_pretrained(save_model_path)
#%%
device = torch.device("cuda" if torch.cuda.is_available() and not args.no_cuda else "cpu")
model.to(device)
#%%
task = 'AIV'
data_dir = '../data/authority_views/'
processor = processors[task.lower()]()
label_list = processor.get_labels()
examples = processor.get_dev_examples(data_dir)

features = convert_examples_to_features(examples, label_list, max_seq_length = 128, tokenizer=tokenizer, output_mode,
    cls_token_at_end=bool(args.model_type in ['xlnet']),            # xlnet has a cls token at the end
    cls_token=tokenizer.cls_token,
    sep_token=tokenizer.sep_token,
    cls_token_segment_id=2 if args.model_type in ['xlnet'] else 1,
    pad_on_left=bool(args.model_type in ['xlnet']),                 # pad on the left for xlnet
    pad_token_segment_id=4 if args.model_type in ['xlnet'] else 0)