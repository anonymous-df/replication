# Readme
This repository includes our data and code. We intend to enhance the explanation of this artifact if the paper is accepted.

## Environment Preparation

CPU: Intel(R) Xeon(R) Platinum 8255C CPU @2.50GHz with 24 core processors, and 86G RAM.

GPU: Two NVIDIA RTX 3090 GPUs with 24 GB memory

Packages: 
`transformers 4.34.1`
`tokenizers 0.14.1`
`torchmetrics 1.2.0`
`torch 2.1.0`
`scikit-learn 1.3.2`
`GPUtil 1.4.0`
`numpy 1.26.1`
`evaluate 0.4.1`
`numba 0.58.1`
`nltk 3.8.1`
`tqdm 4.66.1`
`typing 4.8.0`
`psycopg2 2.9.9`

## Code Files
`model.py`: code for model training. We implement our model with the popular deep learning development framework PyTorch and the python package transformers developed by HuggingFace. 

`hard_sharing.py`: hard parameter sharing class for model MTL pre-training.

`soft_sharing.py`: soft parameter sharing class for model MTL pre-training.

`testing_tc.py` and `testing_lc.py`: code for model testing. We use two evaluation metrics for the TC task, namely the Accuracy (Acc) of the top prediction and the
MRR for the top-5 recommendations. Five commonly used evaluation metrics are employed for the LC task: EM, ED, BLEU, ROUGE, and METEOR.

`instruction_types.py`: code for analysis of model performance when predicts different token types. 

`tokenizer.py`: code for tokenizer.  We use sub-word tokenization with the Byte-Pair Encoding (BPE) algorithm, as previous studies found that BPE can substantially reduce the vocabulary size
and alleviate the OOV problem.


## Data Files
The dataset contains 167,010 instances for pre-training,  89,072 for fine-tuning's training, 11,134 for validation, and 11,134 for testing. 

`train_data_tc_task`: Training, validation, and testing data for the TC task.

`train_data_lc_task`: Training, validation, and testing data for the LC task.

`tokenizer.json`: Our tokenizer file.
