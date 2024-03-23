import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["WANDB_DISABLED"]= "true"
import torch
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
import pickle

from sklearn.metrics import f1_score, roc_auc_score, accuracy_score, precision_score, recall_score, average_precision_score, balanced_accuracy_score
from transformers import RobertaForMaskedLM, BertForMaskedLM, Trainer, TrainingArguments
from modeling_codesage import CodeSageForMaskedLM
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


torch.cuda.set_device(1)
print(device)
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

free_gpu_cache()

##set seed
def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
set_seed(123)

##set tokenizer
tokenizer = PreTrainedTokenizerFast(tokenizer_file="tokenizer.json")
tokenizer.add_special_tokens({'bos_token': '<s>'})
tokenizer.add_special_tokens({'eos_token': '</s>'})
tokenizer.add_special_tokens({'unk_token': '<unk>'})
tokenizer.add_special_tokens({'mask_token': '<mask>'})
tokenizer.add_special_tokens({'pad_token': '<pad>'})


#
# config = RobertaConfig(
#     attention_probs_dropout_prob=0.1,
#     bos_token_id=0,
#     eos_token_id=2,
#     hidden_act="gelu",
#     hidden_dropout_prob= 0.1,
#     hidden_size=768,
#     initializer_range=0.02,
#     intermediate_size=3072,
#     layer_norm_eps=1e-12,
#     max_position_embeddings=514,
#     model_type="roberta",
#     num_attention_heads=12,
#     num_hidden_layers=12,
#     pad_token_id=1,
#     type_vocab_size=1,
#     vocab_size=5000,
#     )
# ##set model config
#model = RobertaForMaskedLM(config)
model = RobertaForMaskedLM.from_pretrained("pretraining/checkpoint")
model.to(device)
print(model.num_parameters())
print(model.config)


#load training and validation dataset
with open('train_data_tc_task.pkl','rb') as f:
    train_dataset = pickle.load(f)
with open('valid_data_tc_task.pkl','rb') as f:
    valid_dataset = pickle.load(f)
final_train_data = []
#final_valid_data = []
#print(train_dataset[0]['input_ids'])
for i in range(0,len(train_dataset)):
    final_train_data.append({'input_ids': torch.tensor(train_dataset[i]['input_ids'][0]), 'labels': torch.tensor(train_dataset[i]['labels'][0])})
for i in range(0,len(valid_dataset)):
    final_valid_data.append({'input_ids': torch.tensor(valid_dataset[i]['input_ids'][0]), 'labels': torch.tensor(valid_dataset[i]['labels'][0])})

print(len(final_train_data[0]['input_ids'][0]))


def preprocess_logits_for_metrics(logits, labels):
    if isinstance(logits, tuple):
        # Depending on the model and config, logits may contain extra tensors,
        # like past_key_values, but logits always come first
        logits = logits[0]
    return logits




training_args = TrainingArguments(
    output_dir="/model/",
    evaluation_strategy="no",
    logging_strategy="steps",
    save_strategy="steps",
    learning_rate=5e-5,
    per_device_train_batch_size=8,
    seed=123,
    save_steps=10000,
    logging_steps=1000,
    max_steps=100000,
    optim="adamw_torch",
    fp16=True,
    report_to = 'none'
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=final_train_data,
)

trainer.train()

##validation
def validation(i,path):
    #print("checkpoint ",i)
    model = RobertaForMaskedLM.from_pretrained('pretraining/checkpoint')
    model.to(device)
    #print(model.num_parameters())

    results = []
    no = 0
    for data in final_valid_data:
        no = no +1
        print(no)
        input = {'input_ids': data['input_ids'].cuda()}
        labels = data['labels'][0].cuda()
        with torch.no_grad():
            output = model(**input).logits
        mask_token_index = (input['input_ids'] == tokenizer.mask_token_id)[0].nonzero(as_tuple=True)[0]

        #print(output)
        a, idx1 = torch.sort(output[0, mask_token_index], descending=True)
        #print(a)
        #print(list(np.round(torch.softmax(a,dim=1).cpu().numpy(),5)))
        a = torch.softmax(a,dim=1).cpu().numpy()
        predicted_token_id_5 = idx1[:,:5]
        predicted_token_ratio_5 = a[:,:5]
        ratios = []
        for items in predicted_token_ratio_5:
            temp = []
            for item in items:
                temp.append(round(item,5))
            ratios.append(temp)
        #print(ratios)

        results.append({'id': no, 'input': data['input_ids'].cpu().numpy(), 'labels': labels[mask_token_index].cpu().numpy(), 'predictions': predicted_token_id_5.cpu().numpy(), 'ratios': ratios})
        #print(results)
    with open('results.pkl', 'wb') as f:
        pickle.dump(results, f)


print("Roberta:")
testing(20,"pretraining")
