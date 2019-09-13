export CUDA_VISIBLE_DEVICES=1
export ROOT_DIR=../src
cd $ROOT_DIR
#rm -rf eval
python inference.py \
--infer_file_name dev  \




