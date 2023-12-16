#! pip install tokenizers

from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.processors import BertProcessing
from tokenizers import normalizers
from tokenizers.normalizers import NFD, StripAccents, Lowercase
from tokenizers import pre_tokenizers
from tokenizers.pre_tokenizers import Digits

# Load data from files
#paths = [str(x) for x in Path("F:/dockerfile-model/dockerfile_data_1/").glob("*.txt")]
import pymysql


def getSQLData(table_name):
    con = pymysql.connect(host='localhost', user='root', passwd='1234',db='xxx')
    cur = con.cursor()
    cur.execute("SELECT content_valid from %s;"%table_name)
    rows = cur.fetchall()
    return rows

text = []
table_names = ['dockerfile']
for table in table_names:
    rows = getSQLData(table)
    for row in rows:
        #print(row[0].replace('\n',' ').strip())
        text.append(row[0].replace('\n',' ').strip())

# Initialize a tokenizer
normalizer = normalizers.Sequence([
    NFD(),          # Unicode
    StripAccents()] # remove accents
)

tokenizer = Tokenizer(BPE(unk_token="<unk>"))

pre_tokenizer = pre_tokenizers.Sequence([
    Whitespace(),
    Digits(individual_digits=False)
])

tokenizer.pre_tokenizer = pre_tokenizer

tokenizer.normalizer = normalizer  # 
trainer = BpeTrainer(special_tokens=["<s>", "<pad>", "</s>", "<unk>", "<mask>"],vocab_size=50000, show_progress=True, min_frequency=2)
# Customize training
tokenizer.train_from_iterator(text, trainer)

#tokenizer.post_processor = BertProcessing(
#    ("</s>", tokenizer.token_to_id("</s>")),
#    ("<s>", tokenizer.token_to_id("<s>")),
#)

#tokenizer.enable_padding(pad_id=1, pad_token="<pad>")

tokenizer.save_model("tokenizer")

print(tokenizer.get_vocab_size())

