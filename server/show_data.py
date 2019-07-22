import redis
import pickle
from server.data_annotation.entropy import show_data
import random

from tools.utils import list_all_users, RedisClient, Indicators
import pandas as pd
from conf.config import incsv_fanChengCheng, redis_port, redis_host, fanChengCheng_db, \
    incsv_jueDiQiuSheng, jueDiQiuSheng_db, incsv_haiTianLin, zhaiTianLin_db, incsv_zhangDanFeng, zhangDanFeng_db

class ShowData(object):
    def __init__(self):
        pass

    def list_all_data(self):
        '''
        [发帖数量，信息熵，用户Id， 用户名字，用户活跃天数，用户语义重复率，新闻关注度，疑似水军 ]
        :return:  用于前端展示数据      '''
        data = []
        userinfo, ens = show_data(self.incsv, self.entropy_file)  # [[area, text, name, time, newsid]]
        for uid, entropy in ens.items():
            postnum = len(userinfo.get(uid))  # 发帖数量
            name = "用户"
            active_days = random.choice([1, 2, 3, 7, 8])
            semantic = random.choice([0.6, 0.9, 0.4, 0.7, 0.8])
            attention = 3
            data.append([postnum, entropy, uid, name, active_days, semantic, attention, "疑似水军"])
        return data



class EventPostNum(object):
    def __init__(self, user_file, user_db):
        self.incsv = user_file  # 元数据
        self.user_client = RedisClient(host=redis_host, port=redis_port, db=user_db)
        self.__post_num() # 统计用户发帖数量

    @staticmethod
    def zhangdanfeng_entropy_data():
        '''
        [发帖数量，信息熵，用户Id， 用户名字，用户活跃天数，用户语义重复率，新闻关注度，疑似水军 ]
        :return:  用于前端展示数据
        '''
        incsv = "F:/scrapy/sina_data1.0.0/zhangDanFeng/parsedData/all_data.csv"  # 元数据
        entropy_file = "F:/pycharm_workspce/web_spammer_detection/server/data_annotation/zhangDanFeng_entropy.pkl"
        data = []
        maxnum = 0
        userinfo, ens = show_data(incsv, entropy_file)  # [[area, text, name, time, newsid]]
        for uid, entropy in ens.items():
            postnum = len(userinfo.get(uid))  # 发帖数量
            name = "测试用户"
            active_days = random.choice([1, 2, 3, 7, 8, 11, 12])
            semantic = random.choice([0.6, 0.8, 0.5, 0.7, 0.45])
            attention = 3
            data.append([postnum, entropy, uid, name, active_days, semantic, attention, "疑似水军"])
            if postnum > maxnum:
                maxnum = postnum  # 获取最大
        return data

    def __post_num(self):
        data = pd.read_csv(self.incsv, usecols=[0], header=None)
        users = list_all_users(self.incsv)
        for user in users:
            temp = data[data[0] == int(user)]
            post_num = temp.shape[0]
            user = str(user) + "_" + Indicators.post
            self.user_client.set(user, post_num)
        print("发帖数量写入redis成功！")


if __name__ == "__main__":
    pass
    # event = EventPostNum(incsv_fanChengCheng, fanChengCheng_db)
    # event = EventPostNum(incsv_zhangDanFeng, zhangDanFeng_db)
    # event = EventPostNum(incsv_haiTianLin, zhaiTianLin_db)
    # event = EventPostNum(incsv_jueDiQiuSheng, jueDiQiuSheng_db)

