export CUDA_VISIBLE_DEVICES=0
export DATA=../../data/LM_finetune_Macro
python finetune_on_pregenerated.py \
--pregenerated_data $DATA/training/ \
--bert_model   $DATA/finetuned_lm/ \
--do_lower_case \
--output_dir $DATA/finetuned_lm/ \
--epochs 10 \
--train_batch_size 64 \
--save_every_steps 4000 \
--gradient_accumulation_steps 8 
 #bert-base-uncased \