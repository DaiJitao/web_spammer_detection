from snownlp import SnowNLP
import jieba
import pandas as pd

content = "代继涛"
s = SnowNLP(content)

print(s.sentiments)
content = "王蒙蒙"
s = SnowNLP(content)

print(s.sentiments)

s = jieba.cut(content)
print(" ".join(s))

file_name = r"F:/scrapy/sina_data1.0.0/jueDiQiuSheng/parsedData/all_data.csv"
good = pd.read_csv(file_name, header=None)
print(good.shape)

import conf

CONF = conf.CONF

print(CONF.base)

import matplotlib
