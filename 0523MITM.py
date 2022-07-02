from mitmproxy import http
from bs4 import BeautifulSoup
# import tensorflow as tf
import numpy as np
import jieba.analyse
import re

# # 加载神经网络模型
# model = tf.keras.models.load_model('url_model')

# # 判断恶意URL
# def predict(url):
#     label = model.predict([" ".join(re.split('[./=%\-?]', url))])[0]
#     index = np.argmax(label, axis=0)
#     return index > 0 and label[index] > 0.9

# with open("hosts.txt","r",encoding="utf-8") as hs:
#     hosts=set(hs.readlines())

# # 过滤恶意host和URL
# def request(flow):
#     host,path=flow.request.host,flow.request.path
#     if host in hosts or predict(host+path):
#         redirect(flow)

def toChinese(text):
    return "".join([ch if '\u4e00' <= ch <= '\u9fff' else "" for ch in text])

with open("keywords.txt", "r", encoding="utf-8") as keyfile:
    keywords = set(keyfile.read().split("\n"))

# 过滤网页正文
def response(flow):
    headers=flow.response.headers
    if not "Content-Type" in headers or not "html" in headers["Content-type"]:
        return

    content=flow.response.content.decode("utf-8")
    soup = BeautifulSoup(content, features='html.parser')
    body=soup.find("body")
    if not body:
        return
    text=toChinese(body.get_text())
    tags=jieba.analyse.extract_tags(text)
    print(tags)

    for tag in tags:
        if tag in keywords:
            redirect(flow)
            return

# 重定向
def redirect(flow):
    flow.response = http.Response.make(200, 
        b"REDIRECTED", {"Content-Type": "text/html"})

