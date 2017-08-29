import pandas as pd
import os
import time


def data_load(file_path):
    temp = pd.read_csv(file_path, header=0, encoding='cp949')
    temp = temp.dropna(axis=0, how='any')
    temp['b_comment'] = temp['b_comment'].str.replace(' ', '_')
    temp['b_comment'] = temp['b_comment'].str.replace(r'\s', '')
    temp['b_comment'] = temp['b_comment'].str.replace('_', ' ')
    temp = temp.groupby(['article_id'])['b_comment'].apply(list).reset_index()

    temp['content'] = None
    iter = 0
    for x in temp['b_comment']:
        temp['content'][iter] = ' '.join(x)
        iter = iter + 1

    temp['date'] = None
    temp['id'] = None
    temp['title'] = None

    return temp

def search(dir):
    filenames = os.listdir(dir)
    data = pd.DataFrame()

    for filename in filenames:
        temp = data_load(os.path.join(dir, filename))
        data = data.append(temp)

    return temp

file_dir = 'C:/Users/JunHee/Desktop/code/data/comment'


s_time = time.time()
result = search(file_dir)
result = result[['article_id', 'c_title', 'c_id', 'c_content', 'c_date']]
result.to_csv('comment.csv', index = False)
print('종료 : ', time.time() - s_time)
