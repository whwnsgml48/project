import tensorflow as tf
import numpy as np
import pandas as pd
from collections import Counter
from collections import defaultdict


def read_data(filename = '../data/sonata_love/sonata_love_hangul.csv'):
    data = pd.read_csv(filename, encoding='cp949')

    data['nouns'] = data['nouns'].str.replace(r'[,]', '')
    data['nouns'] = data['nouns'].str.replace("[", '')
    data['nouns'] = data['nouns'].str.replace("]", '')
    data['nouns'] = data['nouns'].str.replace("'", '')
    data['nouns'] = [data['nouns'][i].split() for i in range(len(data['nouns']))]
    sentences = data['nouns']
    sentences = [sentences[i] for i in range(len(sentences)) if len(sentences[i]) > 2]
    return sentences

sentences = read_data()
print(sentences)
print(len(sentences))

#reference word list
reference = [" ".join(sentences[i]) for i in range(len(sentences))]
reference = " ".join(reference).split()#전체단어를 합친 리스트
word_list = list(set(reference))#고유 단어의 집합
word_dict = {w: i for i, w in enumerate(word_list)}#숫자를 통해 계산하기 위해 단어별 index를 부여하고 이를 dict 형태로 저장함.
word_index = [word_dict[word] for word in reference]# 전체 단어에 대해 index를 부여함

#word2vec 모델에 input으로 사용할 skip-gram 모델을 만든다.
skip_grams = []
idx = 0

for i in range(len(sentences)):
    for k in range(len(sentences[i]) - 2):
        idx = idx + 1
        target = word_index[idx]
        context = [word_index[idx-1], word_index[idx+1]]
        for w in context:
            skip_grams.append([target, w])
    idx = idx + 2


def random_batch(data, size):
    random_inputs = []
    random_labels = []
    random_index = np.random.choice(range(len(data)), size, replace=False)

    for i in random_index:
        random_inputs.append(data[i][0])  # target
        random_labels.append([data[i][1]])  # context word

    return random_inputs, random_labels


#########
# 옵션 설정
######
# 학습을 반복할 횟수
training_epoch = 5000
# 학습률41
learning_rate = 0.01
# 한 번에 학습할 데이터의 크기
batch_size = 20
# 단어 벡터를 구성할 임베딩 차원의 크기
# 이 예제에서는 x, y 그래프로 표현하기 쉽게 2 개의 값만 출력하도록 합니다.
embedding_size = 100
# word2vec 모델을 학습시키기 위한 nce_loss 함수에서 사용하기 위한 샘플링 크기
# batch_size 보다 작아야 합니다.
num_sampled = 15
# 총 단어 갯수
voc_size = len(word_list)

#########
# 신경망 모델 구성
######
inputs = tf.placeholder(tf.int32, shape=[batch_size])
# tf.nn.nce_loss 를 사용하려면 출력값을 이렇게 [batch_size, 1] 구성해야합니다.
labels = tf.placeholder(tf.int32, shape=[batch_size, 1])

# word2vec 모델의 결과 값인 임베딩 벡터를 저장할 변수입니다.
# 총 단어 갯수와 임베딩 갯수를 크기로 하는 두 개의 차원을 갖습니다.
embeddings = tf.Variable(tf.random_uniform([voc_size, embedding_size], -1.0, 1.0))
# 임베딩 벡터의 차원에서 학습할 입력값에 대한 행들을 뽑아옵니다.
# 예) embeddings     inputs    selected
#    [[1, 2, 3]  -> [2, 3] -> [[2, 3, 4]
#     [2, 3, 4]                [3, 4, 5]]
#     [3, 4, 5]
#     [4, 5, 6]]
selected_embed = tf.nn.embedding_lookup(embeddings, inputs)

# nce_loss 함수에서 사용할 변수들을 정의합니다.
nce_weights = tf.Variable(tf.random_uniform([voc_size, embedding_size], -1.0, 1.0))
nce_biases = tf.Variable(tf.zeros([voc_size]))

# nce_loss 함수를 직접 구현하려면 매우 복잡하지만,
# 함수를 텐서플로우가 제공하므로 그냥 tf.nn.nce_loss 함수를 사용하기만 하면 됩니다.
loss = tf.reduce_mean(
            tf.nn.nce_loss(nce_weights, nce_biases, labels, selected_embed, num_sampled, voc_size))

train_op = tf.train.AdamOptimizer(learning_rate).minimize(loss)

with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)

    for step in range(1, training_epoch + 1):
        batch_inputs, batch_labels = random_batch(skip_grams, batch_size)

        _, loss_val = sess.run([train_op, loss],
                               feed_dict={inputs: batch_inputs,
                                          labels: batch_labels})

        if step % 10 == 0:
            print("loss at step ", step, ": ", loss_val)

        if loss_val < 0.5:
            print('loss at step ', step, ": ", loss_val)
            break


    # matplot 으로 출력하여 시각적으로 확인해보기 위해
    # 임베딩 벡터의 결과 값을 계산하여 저장합니다.
    # with 구문 안에서는 sess.run 대신 간단히 eval() 함수를 사용할 수 있습니다.
    trained_embeddings = embeddings.eval()

temp_nouns = reference
temp_count = Counter(temp_nouns)


result = defaultdict(lambda : [])

for i, label in enumerate(word_list):
    result['label'].append(label)
    result['freq'].append(temp_count[label])
    for k, t in enumerate(trained_embeddings[i]):
        result[str(k+1)].append(t)

result = pd.DataFrame(result)
print(result)
result.to_csv('../data/sonata_love_word2vec_result.csv')

