from snownlp import SnowNLP
import jieba
import pandas as pd
import fasttext

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

test_data = "F:/NLP_learnings/fasttext/testData/Data_test.txt"
train_data = 'F:/NLP_learnings/fasttext/trainData/Data_train.txt'
classifier = fasttext.supervised(train_data, "../models/classifier_model", label_prefix='__label__')
result = classifier.test(train_data)
print("准确率", result.precision)

# 原有模型在测试集上准确度
classifier = fasttext.load_model("../models/classifier_model", label_prefix='__label__')
result = classifier.test(test_data)
print("准确率", result.precision)