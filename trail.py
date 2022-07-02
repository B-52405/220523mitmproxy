from mitmproxy import http,ctx
from bs4 import BeautifulSoup
import jieba
import jieba.analyse
import re

def toChinese(text):
    return "".join([ch if '\u4e00' <= ch <= '\u9fff' else "" for ch in text])

print(toChinese("asd你好"))

