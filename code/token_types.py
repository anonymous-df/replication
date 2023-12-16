from torchmetrics.text import EditDistance
import pickle
from transformers import PreTrainedTokenizerFast
import numpy as np
import random
import string

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

_SYMBOLS = string.punctuation
print(_SYMBOLS)
##set seed
def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    #torch.manual_seed(seed)
    #if torch.cuda.is_available():
    #    torch.cuda.manual_seed_all(seed)
set_seed(123)

tokenizer = PreTrainedTokenizerFast.from_pretrained("tokenizer.json")
tokenizer.add_special_tokens({'bos_token': '<s>'})
tokenizer.add_special_tokens({'eos_token': '</s>'})
tokenizer.add_special_tokens({'unk_token': '<unk>'})
tokenizer.add_special_tokens({'mask_token': '<mask>'})
tokenizer.add_special_tokens({'pad_token': '<pad>'})

def testing(path):
    with open('results_%s.pkl'%path,'rb') as f:
        test_dataset = pickle.load(f)
    number = len(test_dataset)
    results = []
    i_number = 0
    st_number = 0
    sb_number = 0
    nm_number = 0
    for data in test_dataset:
        #print(data)
        predictions = np.array(data['predictions'])
        labels = data['labels']

        for x in range(0, len(labels)):
            preds = []
            token = labels[x]
            if tokenizer.decode(token) in _INSTRUCTIONS:
                type = 'Identifier'
                i_number = i_number + 1
            elif tokenizer.decode(token) in _SYMBOLS:
                type = 'Symbol'
                sb_number = sb_number + 1
            elif tokenizer.decode(token).isnumeric():
                type = 'Numeric'
                nm_number = nm_number + 1
            else:
                type = 'String'
                st_number = st_number + 1
            for y in range(0, 5):
                if token == predictions[x, y]:
                    preds.append(1)
                else:
                    preds.append(0)
                    # print(predicted_token_id_5)
            results.append({'token':labels[x],'type':type,'preds':preds})

    print("Total:%s, Identifier:%s, String:%s, Symbol:%s, Number:%s"%(number,i_number,st_number,sb_number,nm_number))
    with open('results_%s_types.pkl'%path,'wb') as f:
        pickle.dump(results, f)


#    predictions = np.array(data['predictions'])
#    labels = data['labels']
def testing_types(path):
    with open('results_%s_types.pkl'%path,'rb') as f:
        dataset = pickle.load(f)
    i_num = 0
    p_num = 0
    s_num = 0
    n_num = 0
    i_acc_1 = 0
    i_acc_5 = 0
    i_mrr = 0
    p_acc_1 = 0
    p_acc_5 = 0
    p_mrr = 0
    s_acc_1 = 0
    s_acc_5 = 0
    s_mrr = 0
    n_acc_1 = 0
    n_acc_5 = 0
    n_mrr = 0
    for data in dataset:
        if data['type']=='Identifier':
            i_num = i_num + 1
            if data['preds'][0] == 1:
                i_acc_1 = i_acc_1 + 1
            for y in range(0, 5):
                if data['preds'][y] == 1:
                    i_acc_5 = i_acc_5 + 1
                    i_mrr = i_mrr + float(1 / (y + 1))
                    break
        elif data['type']=='Symbol':
            p_num = p_num + 1
            if data['preds'][0] == 1:
                p_acc_1 = p_acc_1 + 1
            for y in range(0, 5):
                if data['preds'][y] == 1:
                    p_acc_5 = p_acc_5 + 1
                    p_mrr = p_mrr + float(1 / (y + 1))
                    break
        elif data['type']=='String':
            s_num = s_num + 1
            if data['preds'][0] == 1:
                s_acc_1 = s_acc_1 + 1
            for y in range(0, 5):
                if data['preds'][y] == 1:
                    s_acc_5 = s_acc_5 + 1
                    s_mrr = s_mrr + float(1 / (y + 1))
                    break
        elif data['type']=='Numeric':
            n_num = n_num + 1
            if data['preds'][0] == 1:
                n_acc_1 = n_acc_1 + 1
            for y in range(0, 5):
                if data['preds'][y] == 1:
                    n_acc_5 = n_acc_5 + 1
                    n_mrr = n_mrr + float(1 / (y + 1))
                    break

    total = i_num + s_num + p_num + n_num
    result = {
    'Identifier': {'number': i_num, 'ratio':float(i_num/total), 'Acc-1':float(i_acc_1/i_num), 'Acc-5':float(i_acc_5/i_num), 'MRR':float(i_mrr/i_num)},
    'String': {'number': s_num, 'ratio':float(s_num/total), 'Acc-1':float(s_acc_1/s_num), 'Acc-5':float(s_acc_5/s_num), 'MRR':float(s_mrr/s_num)},
    'Numeric': {'number': n_num, 'ratio':float(n_num/total), 'Acc-1':float(n_acc_1/n_num), 'Acc-5':float(n_acc_5/n_num), 'MRR':float(n_mrr/n_num)},
    'Symbol': {'number': p_num, 'ratio': float(p_num / total), 'Acc-1': float(p_acc_1 / p_num), 'Acc-5': float(p_acc_5 / p_num), 'MRR': float(p_mrr / p_num)},
    }
    print('Identifier', result['Identifier'])
    print('String', result['String'])
    print('Numeric', result['Numeric'])
    print('Punctuation', result['Symbol'])



#print("No Pretraining:")
#testing("no-pretraining")