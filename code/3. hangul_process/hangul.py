import pandas as pd
from konlpy.tag import Kkma
import numpy as np

kkma = Kkma()

data = pd.read_csv('../data/sonata_love/sonata_love.csv', encoding='cp949')
data['text'] = data['title'] + ' ' + data['content']
col_names = ['article_id', 'id', 'date', 'text']
data = data[col_names]

#article_id처리
data['article_id'] = data.article_id.str.split('=', expand = True)[1]

#불용어 처리
data['text'] = data['text'].str.replace(r'[,-;:~*.-/(/)/?!^+%]','')
data['text'] = data['text'].str.replace('"',' ')
data['text'] = data['text'].str.replace("'",' ')
data['text'] = data['text'].str.replace('ㅠ','')
data['text'] = data['text'].str.replace('ㅋ','')
data['text'] = data['text'].str.replace('ㄷ','')
data['text'] = data['text'].str.replace('ㅎ','')
data['text'] = data['text'].str.replace('ㅅ','')
data['text'] = data['text'].str.replace('ㅈ','')
data['text'] = data['text'].str.replace('ㄹ','')
data['text'] = data['text'].str.replace('ㅇ','')
data['text'] = data['text'].str.replace('ㅜ','')
data['text'] = data['text'].str.replace('ㅡ','')
data['text'] = data['text'].str.replace(' ','_')
data['text'] = data['text'].str.replace(r'\s','')
data['text'] = data['text'].str.replace('_',' ')
data['text'] = data['text'].str.upper()

data = data.dropna(axis=0, how='any')
data['nouns'] = np.NaN



def tokenize(doc):
    for i, text in doc['text'].iteritems():
        temp = kkma.pos(text)
        temp = [list(t) for t in zip(*temp)]
        temp = {'noun' : temp[0],
                'pos' : temp[1]}
        temp = pd.DataFrame(data = temp)

        result = [temp['noun'][i] + '/' + temp['pos'][i] for i in range(len(temp))]
        doc['nouns'][i] = result
        print(i, doc['nouns'][i])

tokenize(data)

data = data.dropna(axis=0, how='any')

data.to_csv('../data/sonata_love/sonata_love_hangul.csv')