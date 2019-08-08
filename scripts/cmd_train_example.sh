export CUDA_VISIBLE_DEVICES=0
export ROOT_DIR=../src
cd $ROOT_DIR
export DATA_DIR=../data/authority_views
#rm -rf eval
python run_glue.py \
--model_type bert \
--model_name_or_path bert-base-uncased \
--task_name AIV \
--do_train \
--do_eval \
--data_dir $DATA_DIR/  \
--output_dir ../data/model_weights/AIV/ \
--save_steps 50 \
--num_train_epochs 8.0 \
--do_lower_case \
--learning_rate 3e-5 \
--max_seq_length=256 \
--evaluate_during_training \
--eval_all_checkpoints

#--per_gpu_eval_batch_size=8   \
#--per_gpu_train_batch_size=8   \



