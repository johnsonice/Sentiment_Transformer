export CUDA_VISIBLE_DEVICES=0
export DATA=../../data/LM_finetune_Macro
python finetune_on_pregenerated.py \
--pregenerated_data $DATA/training/ \
--bert_model bert-base-uncased \
--do_lower_case \
--output_dir $DATA/finetuned_lm/ \
--epochs 3 \
--train_batch_size 8 \
--save_every_steps 2000 \
