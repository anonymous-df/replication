import os

from torchmetrics.text import EditDistance, BLEUScore, ROUGEScore

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["WANDB_DISABLED"]= "true"
import torch
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
import pickle

from sklearn.metrics import f1_score, roc_auc_score, accuracy_score, precision_score, recall_score, average_precision_score, balanced_accuracy_score
from transformers import RobertaForMaskedLM, RobertaConfig
from transformers import PreTrainedTokenizerFast
import numpy as np
import random
import evaluate
import gc
from GPUtil import showUtilization as gpu_usage
from numba import cuda
import logging
from torch import nn
from transformers import Trainer
from torchmetrics.text.rouge import ROUGEScore
from nltk.translate import meteor
from collections import Counter


#torch.cuda.set_device(1)
#print(device)
##free GPU cache
def free_gpu_cache():
    print("Initial GPU Usage")
    gpu_usage()
    gc.collect()
    torch.cuda.empty_cache()
    cuda.select_device(0)
    cuda.close()
    cuda.select_device(0)
    print("GPU Usage after emptying the cache")
    gpu_usage()

#ree_gpu_cache()

##set seed
def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
set_seed(123)

tokenizer = PreTrainedTokenizerFast.from_pretrained("tokenizer.json")
tokenizer.add_special_tokens({'bos_token': '<s>'})
tokenizer.add_special_tokens({'eos_token': '</s>'})
tokenizer.add_special_tokens({'unk_token': '<unk>'})
tokenizer.add_special_tokens({'mask_token': '<mask>'})
tokenizer.add_special_tokens({'pad_token': '<pad>'})

def testing(path):
    with open('line_results.pkl', 'rb') as f:
        test_dataset = pickle.load(f)

    #print(test_dataset[0])
    masks = 0
    perfect = 0
    edits = 0
    bleu = 0
    rouge = 0
    meteor_value = 0
    number = len(test_dataset)
    no = 0
    for data in test_dataset:
        no = no + 1
        print(no)
        #print(data)
        predictions = np.array(data['predictions'])
        labels = data['labels']

        masks = masks + len(labels)

        #if np.array_equal(predictions[:, 0], labels):
        if np.array_equal(predictions, labels):
            perfect = perfect + 1

        #preds = [tokenizer.decode(item) for item in predictions[:,0]]
        preds = [tokenizer.decode(item) for item in predictions]
        #print(preds)
        trues = [tokenizer.decode(item) for item in labels]
        #print(trues)
        length_preds = len(''.join(preds))
        length_trues = len(''.join(trues))
        if length_preds >= length_trues:
            length = length_preds
        else:
            length = length_trues
        ed_metric = EditDistance()
        edits = edits + float(ed_metric([' '.join(preds)],[' '.join(trues)])/length)
        #print(edits)

        bleu_metric = BLEUScore()
        bleu = bleu + bleu_metric([' '.join(preds)],[[' '.join(trues)]])

        rouge_metric = ROUGEScore()
        rouge = rouge + rouge_metric(' '.join(preds),' '.join(trues))['rougeL_fmeasure']

        meteor_value = meteor_value + meteor([preds], trues)

    metrics = {
        'perfect': perfect,
        'masks': masks,
        'BLEU': float(bleu / number),
        'ROUGE-L': float(rouge/number),
        'METEOR': float(meteor_value/number),
        'EM': float(perfect/number),
        'ED': float(edits/number)
    }
    print(metrics)


print('DockerFill')
testing('pretraining')
