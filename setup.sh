conda create -n pytorch_transformer python==3.7 -y
source activate pytorch_transformer

conda install numpy pandas scipy scikit-learn xlrd spyder jupyter notebook -y
pip install pytorch-transformers
pip install tensorboardX