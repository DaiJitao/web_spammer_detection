# 计算所有指标： 语义重复率、活跃天数、信息熵、新闻关注度

from server.data_annotation.entropy import count_information_entropy, count_post_num
from server.data_annotation.semantic_similarity import SemanticSimilarity
import time
from conf.config import redis_host, redis_port
from tools.utils import list_all_users, RedisClient, Indicators, list_all_users_text, get_all_data_iterator
import pandas as pd
from conf.config import incsv_fanChengCheng, fanChengCheng_db, all_data_db, incsv_all_data

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


class AllData():
    def __init__(self, incsv):
        self.incsv = incsv
        self.data = get_all_data_iterator(incsv=incsv, usecols=["uid", "newsid", 'time'], header=True)

    def encode(self):
        ''' 对newsid 进行转码 comos-htxyzsm2133938 ==》 1 '''
        news_set = set()  # 新闻集合
        for seg in self.data:
            seg = seg[["uid", "newsid"]]
            for uid, newsid in seg.values:
                news_set.add(newsid)
                size = len(news_set)
                redis_res = client.get(newsid)
                if redis_res != None:
                    client.set(newsid, size)
                else:
                    client.set(newsid, size)
        print("新闻编码转换完毕，成功写入redis！")

    def list_all_user_attention_num(self):
        # 计算每一个用户的新闻关注度，并写入redis, 数据为整个月全量数据
        # data = get_all_data_iterator(incsv=self.incsv, header=True)
        for seg in self.data:
            seg = seg[['uid', 'newsid']]
            for uid, newsid in seg.values:
                uid = str(uid)
                redis_res = client.get(uid)  # 取出用户关注的新闻
                news_code = client.get(newsid)  # 取出新闻编码
                uid_concern = uid + "_" + Indicators.concern
                if redis_res == None:  # 如果该值为不存在，则newsid存入redis
                    # 获取新闻编码
                    client.set(uid_concern, news_code)
                else:  # 如果不为空
                    redis_res = redis_res + "_" + news_code
                    client.set(uid_concern, redis_res)
        print("计算所有用户新闻关注度完毕,写入redis成功！")

    def list_all_active_days(self):
        ''' 统计用户的活跃天数, 计算所有用户 '''
        try:
            # data = get_all_data_iterator(self.incsv, usecols=['uid', 'time'], header=True, rows=500)
            data = self.data
            for seg in data:
                seg = seg[['uid', 'time']]
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


class AllIndicators(object):
    def __init__(self, incsv_file, user_db):
        self.user_file = incsv_file
        self.users = list_all_users(incsv_file)
        self.user_client = RedisClient(host=redis_host, port=redis_port, db=user_db)
        self.user_data = pd.read_csv(self.user_file, header=None)

    def post_num(self):
        ''' 统计用户的活跃天数 '''
        data = self.user_data[[0]]
        for user in self.users:
            temp = data[data[0] == int(user)]
            post_num = temp.shape[0]
            user = str(user) + "_" + Indicators.post
            self.user_client.set(user, post_num)
        print("发帖数量写入redis成功！")

    def entropy_to_redis(self):
        """ 基于计算写入redis """
        uid_result, max_interval, max_num = count_post_num(self.user_data)
        ens = count_information_entropy(uid_result, max_num, max_interval)  # 获取信息熵的结果
        for uid, value in ens.items():
            uid = str(uid) + "_" + Indicators.entropy
            value = float("%.5f" % value)
            self.user_client.set(uid, str(value))

    def active_days_to_redis(self):
        # 统计单个事件用户的活跃天数
        for uid in self.users:
            uid = str(uid) + "_" + Indicators.active_days
            dates = client.get(uid)
            if dates == None:
                self.user_client.set(uid, "1")
            else:
                num = str(len(set(dates.split("_"))))
                self.user_client.set(uid, num)
            print(num)
        print("活跃天数写入用户redis成功！")

    def news_concern_to_redis(self):
        ''' 计算新闻关注度,并写入redis '''
        for user in self.users:
            uid = str(user)
            uid_concern = "_".join([uid, Indicators.concern])  # 拼接字符串
            nums = client.get(uid_concern)
            if nums == None:
                # 写入redis
                client.set(uid_concern, "#")
                self.user_client.set(uid_concern, "1")
            else:
                concern_num = len(nums.split("_")) + 1
                nums = nums + "_" + "#"
                client.set(uid_concern, nums)
                self.user_client.set(uid_concern, concern_num)
                print(nums)

    def semantic_ratio_to_redis(self):
        ss = SemanticSimilarity()  # 初始化
        for key in self.users:
            texts = list_all_users_text(self.user_data, key)  # 获取所有文本
            rs = ss.ratio(texts)
            if len(rs) > 0:
                rs = [str(i) for i in rs]  # 转换为字符串
                temp = ",".join(rs)
            else:
                temp = "低于80%"

            uid = str(key) + "_" + Indicators.semantic
            # print(uid, " rs:", rs, " temp:", temp)
            self.user_client.set(uid, temp)
        print("写入语义重复率redis成功！")


if __name__ == "__main__":
    all = AllData(incsv=incsv_all_data)
    pass
