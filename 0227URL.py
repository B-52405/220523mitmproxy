import tensorflow as tf
import random
import re

# 本地数据集
FILE_NAMES = [
    "Benign_list_big_final.csv",
    "spam_dataset.csv",
    "phishing_dataset.csv",
    "Malware_dataset.csv",
    "DefacementSitesURLFiltered.csv"
]

# 读取本地数据集
train_urls = []
train_labels = []
for i, file_name in enumerate(FILE_NAMES):
    with open("URL/"+file_name, encoding="UTF-8") as file:
        urls = file.read().split("\n")
        train_urls.extend(urls)
        train_labels.extend([i for j in range(len(urls))])

train_urls = [" ".join(re.split('[./=%\-?]', url)) for url in train_urls]

# for label,url in zip(train_labels[:10],train_urls[:10]):
#     print(label,url)

random.seed(7)
random.shuffle(train_urls)
random.seed(7)
random.shuffle(train_labels)

# 文本预处理层
VOCAB_SIZE = 1000
text_vector = tf.keras.layers.TextVectorization(max_tokens=VOCAB_SIZE)
text_vector.adapt(train_urls)

# 神经网络结构
model = tf.keras.Sequential([
    text_vector,
    tf.keras.layers.Embedding(len(text_vector.get_vocabulary()), 64),
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dense(len(FILE_NAMES), activation='softmax'),
])

# model.summary()

# 编译神经网络
model.compile(
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    optimizer=tf.keras.optimizers.Adam(),
    metrics=['accuracy']
)

# 训练
model.fit(train_urls, train_labels, epochs=10)

model.save("url_model")
