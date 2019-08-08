export CUDA_VISIBLE_DEVICES=0
python ./examples/run_glue.py \
    --model_type bert \
    --model_name_or_path bert-base-uncased \
    --task_name SST-2 \
    --do_train \
    --do_eval \
    --do_lower_case \
    --data_dir data/glue_data/SST-2 \
    --max_seq_length 128 \
    --per_gpu_eval_batch_size=8   \
    --per_gpu_train_batch_size=8   \
    --learning_rate 2e-5 \
    --num_train_epochs 3.0 \
    --output_dir data/model_weights/SST-2/