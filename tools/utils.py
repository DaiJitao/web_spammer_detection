import numpy as np
import collections
import pandas as pd
import redis
from conf.config import incsv_all_data, redis_port, redis_host, all_data_db


class Indicators(object):
    concern = "concern"
    semantic = "2"
    active_days = "days"
    entropy = "1"
    post = "3"

def __stop_words(file="../data/stopWords/StopWords.txt"):
    result = set()
    with open(file) as text:
        for line in text.readlines():
            result.add(line.strip())

    # with open("../data/stopWords/stopwords2.txt", encoding='utf-8') as file:
    #     for line in file.readlines():
    #         result.add(line.strip())
    return result


def all_index(data, v):
    result = []
    count = 0
    for value in data:
        if value == v:
            result.append(count)
        count += 1
    return result


# stop_words = __stop_words
# STOP_WORDS = __stop_words()

def list_all_users_text(incsv, uid):
    ''' 返回每一个用户所对应的文本 '''
    try:
        uid = int(uid)
        data = pd.read_csv(incsv, usecols=[0, 3], header=None)  # uid content
        res = data[data[0] == uid]
        return res[3]  # 返回该用户所有文本
    except Exception as e:
        print(e)


def list_all_users(incsv):
    ''' 返回所有用户 '''
    try:
        data = pd.read_csv(incsv, usecols=[0], header=None)  # uid content
        res = data[0]
        return res.unique()  # 去重
    except Exception as e:
        print(e)


def get_all_data_iterator(incsv, header=None, usecols=["uid", "newsid"], rows=1000):
    ''' 获取整个月的数据 '''
    try:
        if header == None:
            reader = pd.read_csv(incsv, usecols=usecols, header=header, chunksize=rows, iterator=True)  # 返回迭代器
        else:
            reader = pd.read_csv(incsv, usecols=usecols, chunksize=rows, iterator=True)  # 返回迭代器
        return reader
    except Exception as e:
        print(e)

class NewsEncode(object):
    ''' 对所有新闻进行编码 '''
    def __init__(self):
        self.client =  RedisClient(host=redis_host, port=redis_port, db=all_data_db)
        self.data = get_all_data_iterator(incsv=incsv_all_data, header=True)

    def encode(self):
        ''' 对newsid 进行转码 comos-htxyzsm2133938 ==》 1 '''
        news_set = set()  # 新闻集合
        for seg in self.data:
            for uid, newsid in seg.values:
                news_set.add(newsid)
                size = len(news_set)
                redis_res = self.client.get(newsid)
                if redis_res != None:
                    self.client.set(newsid, size)
                else:
                    self.client.set(newsid, size)
        print("新闻编码转换完毕，成功写入redis！")




class RedisClient(object):
    def __init__(self, host, port, db):
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def get(self, uid):
        try:
            va = self.client.get(uid)
            return va
        except Exception as e:
            print("redis取值错误", e)

    def set(self, uid, value):
        try:
            self.client.set(uid, value)
        except Exception as e:
            print("redis写入错误", e)


if __name__ == "__main__":
    newscode = NewsEncode()
    newscode.encode()

