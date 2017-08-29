import pandas as pd
import os
import time


data = pd.DataFrame()

def search(dir):
    filenames = os.listdir(dir)
    data = pd.DataFrame()

    for filename in filenames:
        temp = pd.read_csv(os.path.join(dir, filename), header=0, encoding='cp949')
        data = data.append(temp)
    #data = data.dropna(axis=0, how='any')
    return data

file_name = 'C:/Users/JunHee/Desktop/code/data/sonata_love'

s_time = time.time()
result = search(file_name)
result = result[['article_id','title','id','content','date']]
result.to_csv('article.csv', index=False)
print('종료 : ', time.time()-s_time)