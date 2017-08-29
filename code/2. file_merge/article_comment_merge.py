import pandas as pd


article = pd.read_csv('C:/Users/JunHee/Desktop/code/data/sonata_love/article.csv', encoding='cp949')
comment = pd.read_csv('C:/Users/JunHee/Desktop/code/data/sonata_love/comment.csv', encoding='cp949')

df = pd.merge(article,comment, on = 'article_id', how='inner')
print(df.head())
df['content'] = df['content'] + ' ' + df['c_content']
df = df[['article_id', 'title', 'id','content','date']]
print(df.head())
df.to_csv('sonata_love.csv', index=False)