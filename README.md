# Readme
Artifact package. This repository includes our data and code.

## Environment Preparation

CPU:  Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz with 12 core processors, and 32G RAM.

GPU: NVIDIA RTX 3090 GPU with 24 GB memory

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

`testing_tc.py` and `testing_lc.py`: code for model testing. We use two evaluation metrics for the TC task, namely the Accuracy (Acc) of the top prediction and the
MRR for the top-5 recommendations. Five commonly used evaluation metrics are employed for the LC task: EM, ED, BLEU, ROUGE, and METEOR.

`token_types.py`: code for analysis of model performance when predicts different token types. 

`tokenizer.py`: code for tokenizer.  We use sub-word tokenization with the Byte-Pair Encoding (BPE) algorithm, as previous studies found that BPE can substantially reduce the vocabulary size
and alleviate the OOV problem.

`statistics.R`: We enhance the automatic evaluation by conducting statistical tests. We employ the McNemar’s test (with Odds Ratios) and the Wilcoxon signed-rank test (with Cliff’s delta) on the metrics. Holm’s correction procedure is employed to account for multiple comparisons in
both statistical tests to adjust p-values.

## Data Files
The dataset contains 89,141 instances for training, 11,143 for validation, and 11,143 for testing. 

`train_data_tc_task`: Training, validation, and testing data for the TC task.

`train_data_lc_task`: Training, validation, and testing data for the LC task.


`human_scores`: We consider three evaluation criteria: Similarity (s), Naturalness (n), and Informativeness (i). The score values range from 1 to 4, with a higher score indicating a higher quality of the predicted lines. The score of s1 and s2 means student 1 and student 2.
