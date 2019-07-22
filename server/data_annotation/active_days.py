from tools import date_to_seconds
import time
import pandas
import pickle

import csv
from tools.utils import list_all_users, RedisClient, Indicators, get_all_data_iterator
from conf.config import redis_port, redis_host, all_data_db, fanChengCheng_db, zhangDanFeng_db, zhaiTianLin_db, \
    jueDiQiuSheng_db, pkl_active_days_all_user, incsv_all_data, incsv_fanChengCheng, incsv_jueDiQiuSheng, incsv_zhangDanFeng, incsv_haiTianLin

'''统计用户说我活跃天数'''

client = RedisClient(host=redis_host, port=redis_port, db=all_data_db)  # 连接全局数据库


def dateTime_to_id(datetime, mode="%Y-%m-%d %H:%M:%S"):
    ''' 日期转换 '''
    array = time.strptime(datetime, mode)
    year = str(array.tm_year)
    mon = str(array.tm_mon)
    if len(mon) == 1:
        mon = "0" + mon
    day = str(array.tm_mday)
    if len(day) == 1:
        day = "0" + day
    day = str(year + mon + day)
    return day


class AllUserActiveDays(object):
    '''  统计所有用户的活跃天数
     '''

    def __init__(self, incsv_all_data):
        self.incsv = incsv_all_data

    def count_active_days(self):
        ''' 统计用户的活跃天数, 计算所有用户 '''
        try:
            data = get_all_data_iterator(incsv_all_data, usecols=['uid', 'time'], header=True, rows=500)
            for seg in data:
                for uid, date in seg.values:
                    dateid = dateTime_to_id(date)
                    new_uid = str(uid) + "_" + Indicators.active_days
                    days_num = client.get(new_uid)
                    if days_num == None:
                        client.set(new_uid, dateid)
                    else:
                        days_num = days_num + "_" + dateid
                        client.set(new_uid, days_num)
            print(new_uid, "统计所有用户活跃天数完毕，写入redis成功!")
            return True
        except Exception as e:
            print("统计所有用户活跃天数完毕失败，{}!".format(e))

    def save_days_pkl(self, outfile, data):
        with open(outfile, "wb") as file:
            pickle.dump(data, file)  # 文件保存

    def pkl_to_redis(self, pkl_file):
        """ 把所有用户的活跃天数写入到redis """
        with open(pkl_file, mode="rb") as file:
            data = pickle.load(file)
        for uid, days in data.items():
            print(uid, days)


class EventActiveDays():
    ''' 统计某个事件的用户天数 '''

    def __init__(self, user_file, user_db):
        self.user_file = user_file
        try:
            self.user_client = RedisClient(host=redis_host, port=redis_port, db=user_db)
        except Exception as e:
            print("redis连接失败", e)

    def add_active_days_redis(self):
        """ 把该事件添加到redis """
        data = pandas.read_csv(self.user_file, usecols=[0, 7])  # 读取用户id 和 时间日期
        for uid, time in data.values:
            dateid = dateTime_to_id(time)
            uid = str(uid) + "_" + Indicators.active_days
            redis_dates = client.get(uid)
            if redis_dates == None:
                client.set(uid, dateid)
            else:
                dateid = redis_dates + "_" + dateid
                client.set(uid, dateid)

    def count_active_days(self):
        # 统计单个事件用户的活跃天数
        users = list_all_users(incsv=self.user_file)  # 获取用户文件
        for uid in users:
            uid = str(uid) + "_" + Indicators.active_days
            dates = client.get(uid)
            if dates == None:
                self.user_client.set(uid, "1")
            else:
                num = str(len(set(dates.split("_"))))
                self.user_client.set(uid, num)
        print("写入用户redis成功！")


if __name__ == "__main__":
    d = dateTime_to_id('2019-03-11 22:51:40')
    # incsv = "F:/scrapy/sina_data1.1.0/comments_data/parsed/all_data_4.csv"
    # outfile = "active_days.pkl"
    # res = count_user_days(incsv)
    # save_user_days(outfile, res)
    # print(res)
    # event = EventActiveDays(incsv_fanChengCheng, fanChengCheng_db)
    # event.add_active_days_redis()
    # event.count_active_days()
    event = EventActiveDays(incsv_zhangDanFeng, zhangDanFeng_db)
    event.add_active_days_redis()
    event.count_active_days()

    event = EventActiveDays(incsv_jueDiQiuSheng, jueDiQiuSheng_db)
    event.add_active_days_redis()
    event.count_active_days()

    event = EventActiveDays(incsv_haiTianLin, zhaiTianLin_db)
    event.add_active_days_redis()
    event.count_active_days()
