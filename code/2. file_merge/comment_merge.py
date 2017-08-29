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

    return data

file_name = '현대/쏘나타/LF쏘나타러브/질문답변'

s_time = time.time()
result = search('D:/'+file_name+'/comment')
result = result[['article_id','b_id','b_date','b_comment']]
result.to_csv('D:/'+file_name+'/comment.csv', index=False)
print('종료 : ', time.time()-s_time)