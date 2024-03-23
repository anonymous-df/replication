import torch
import pickle

from transformers import RobertaForMaskedLM,PreTrainedTokenizerFast
import numpy as np
import random
import logging
from torch import nn
import time


##set seed
def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
set_seed(123)

_INSTRUCTIONS = ['FROM',
                 'MAINTAINER',
                 'RUN',
                 'CMD',
                 'LABEL',
                 'EXPOSE',
                 'ENV',
                 'ADD',
                 'COPY',
                 'ENTRYPOINT',
                 'VOLUME',
                 'USER',
                 'WORKDIR',
                 'ONBUILD',
                 'HEALTHCHECK',
                 'ARG',
                 'STOPSIGNAL',
                 'SHELL']
tokenizer = PreTrainedTokenizerFast.from_pretrained("tokenizer.json")

with open('finetuning_test_data_token.pkl','rb') as f:
    valid_dataset = pickle.load(f)


def testing(i,dataset):
    #print("checkpoint ",i)
    model = RobertaForMaskedLM.from_pretrained('codebert')

    em = 0
    em_5 = 0
    masks = 0
    mrrs = 0
    number = len(dataset)
    for data in dataset:
        #no = no +1
        #print(no)
        input = {'input_ids': data['input_ids']}
        labels = data['labels'][0]
        with torch.no_grad():
            output = model(**input).logits
        mask_token_index = (input['input_ids'] == 4)[0].nonzero(as_tuple=True)[0]

        masks = masks + len(mask_token_index)
        predicted_token_id = output[0, mask_token_index].argmax(axis=-1)
        #print(predicted_token_id)

        for j in range(0, len(mask_token_index)):
            if predicted_token_id[j] == labels[mask_token_index[j]]:
                em = em + 1

        a, idx1 = torch.sort(output[0, mask_token_index], descending=True)
        predicted_token_id_5 = idx1[:,:5]
        for x in range(0, len(mask_token_index)):
            for y in range(0, 5):
                if labels[mask_token_index[x]] == predicted_token_id_5[x,y]:
                    em_5 = em_5 + 1
                    mrrs = mrrs + float(1/(y+1))
                    break

    metrics = {
        'em': em,
        'masks': masks,
        'Acc-1': float(em/masks),
        'Acc-5': float(em_5/masks),
        'MRR': float(mrrs/masks),
    }
    print(_INSTRUCTIONS[i])
    print(metrics)

#print("CodeBert:")

print("Start Evaluation...")
start = time.perf_counter() 
print("Start Timestamp:", start)

for q in range(0,17):
    final_valid_data = []
    for i in range(0,len(valid_dataset)):
        #print(valid_dataset[i])
        for j in range(0, len(valid_dataset[0]['input_ids'])):
            x = tokenizer.convert_ids_to_tokens([valid_dataset[i]['input_ids'][j]])
            #print(x)
            if x[0] in _INSTRUCTIONS:     
                tag = x[0]
                #print(tag)
            elif x[0] == '<mask>':
                break
        if tag==_INSTRUCTIONS[q]:
            final_valid_data.append({'input_ids': torch.tensor([valid_dataset[i]['input_ids']]), 'labels': torch.tensor([valid_dataset[i]['labels']])})
    testing(q,final_valid_data)
