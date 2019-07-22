import pandas
from tools import get_num_all_closed, get_num, date_to_seconds, group
from tools.utils import RedisClient, Indicators
from math import log2
import pickle
from conf.config import redis_port, redis_host, pkl_fanChengCheng_entropy, pkl_jueDiQiuSheng_entropy, \
    pkl_zhaiTianLin_entropy, pkl_zhangDanFeng_entropy, fanChengCheng_db, jueDiQiuSheng_db, zhaiTianLin_db, \
    zhangDanFeng_db

day_seconds = 86400  # 一天的秒数


def __user_data_parse(data, uid):
    ''' 统计发帖的数量 { uid:num , interval: 2136 }  时间间隔 '''
    ud = data[data[0] == uid]
    size = ud.shape[0]
    if size >= 3:
        times = []  # 用户的发帖时间
        for i, (uid_, date) in ud.iterrows():
            time = date_to_seconds(date)
            times.append(time)
        times.sort()  # 从小到大排序
        interval = times[-1] - times[0]  # 统计最大时间间隔 秒
        if interval <= day_seconds:
            return {"times": times, "interval": interval, "post_num": len(times)}
    else:
        return None


def count_post_num(temp):
    ''' 统计发帖的数量 { uid:num } '''
    # temp = pandas.read_csv(incsv, header=None)
    data = temp[[0, 7]]  # 0:uid, 7: time  x['6525265489']
    uid_set = set()
    max_num = 0  # 最大用户发帖数量
    max_interval = 0  # 最大时间间隔
    uid_result = dict()
    for i, (uid, time) in data.iterrows():
        if uid not in uid_set:  # 如果不在集合里面
            uid_set.add(uid)
            result = __user_data_parse(data, uid)
            if result != None:
                num = result['post_num']  # 用户发帖数量
                interval = result['interval']  # 用户发帖时间间隔
                uid_result.update({str(uid): result})
                if max_num < num:
                    max_num = num
                if max_interval < interval:
                    max_interval = interval
            else:
                pass
        else:  # 如果在集合里面
            pass

    return uid_result, max_interval, max_num


def group_num(times, avg_interval):
    """分组 分为固定窗口 [[1, 11], [11, 21], [21, 31], [31, 41], [41, 51], [51, 61], [61, 71], [71, 81], [81, 91], [91, 101]]
    """
    start = times[0]
    end = times[-1]
    time_windows = []
    while True:
        tmp = (start + avg_interval)
        if end > tmp:
            d = [start, tmp]
            start = tmp
            time_windows.append(d)
        else:
            break

    time_windows.append([start, tmp])
    # 统计在每一个窗口内的发帖数量
    result = {}
    win_len = len(time_windows)
    for i in range(win_len):
        window_start, window_end = time_windows[i]
        if i == (win_len - 1):  # 如果是最后一个窗口
            res = get_num_all_closed(window_start, window_end, times)
            result.update({str([window_start, window_end]): len(res)})
        else:  # 如果是不是最后一个窗口
            res = get_num(window_start, window_end, times)
            result.update({str([window_start, window_end]): len(res)})
    return result


def __get_entropy(post_info, k):
    '''
    计算用户的信息熵
    :param post_info:  {'[1, 11]': 2, '[11, 21]': 2, '[21, 31]': 1, '[31, 41]': 1}
    :param k: 所有用户中最大的发帖数量
    :return:
    '''
    _sum = 0
    for v in post_info.values():
        if v != 0:
            p = v / k  # 计算概率
            _sum = _sum + p * log2(1 / p)
    return _sum


def count_information_entropy(result, max_num, max_interval):
    '''
    :param result:
    :param max_num: k : max_num 用户最大的发帖数量
    :param max_interval:
    :return:
    '''
    avg_interval = max_interval // max_num  # 平均时间间隔 1259
    ens = {}
    for (uid, v) in result.items():
        times = v['times']
        result = group_num(times, avg_interval)
        Entropy = __get_entropy(result, max_num)
        ens.update({uid: Entropy})
    return ens


def post_rules(dates, groups):
    """
    统计每一个时间段的发帖数量
    :param dates:
    :param groups:
    :return:
    """
    dates_len = len(dates)
    groups_len = len(groups)
    r = dict()
    for i in range(groups_len):
        _min, _max = groups[i]
        if i == groups_len - 1:  # 如果是最后一行
            res = get_num_all_closed(_min, _max, dates)
            index = str(i + 1)
            r[index] = len(res)
        else:
            res = get_num(_min, _max, dates)
            index = str(i + 1)
            r[index] = len(res)
        #
        for i in res:
            dates.remove(i)
    return r


def save_entry(incsv, outfile):
    '''
    信息熵的保存，格式 {uid: Entropy}
    :param incsv:
    :param outfile:
    :return:
    '''
    temp = pandas.read_csv(incsv, header=None)
    uid_result, max_interval, max_num = count_post_num(temp)
    ens = count_information_entropy(uid_result, max_num, max_interval)  # 获取信息熵的结果
    with open(outfile, mode='wb') as file:
        pickle.dump(ens, file)  # 文件保存


def show_data(incsv, entropy_file):
    result = dict()
    tmp = pandas.read_csv(incsv, header=None)
    with open(entropy_file,mode='rb') as file:
        ens = pickle.load(file)  # 获取信息熵
    data = tmp[[0, 2, 3, 4, 7, 8]]
    for index, (uid, area, text, name, time, newsid) in data.iterrows():
        uid = str(uid)
        entropy = ens.get(uid)
        if entropy != None:
            if uid in result.keys():
                result.get(uid).append([area, text, name, time, newsid])
            else:
                result.update({uid: [[area, text, name, time, newsid]]})
    return result, ens

class EventEntropy(object):
    def __init__(self, user_db, user_pkl, user_file=None):
        self.user_client = RedisClient(host=redis_host, port=redis_port, db=user_db)
        self.user_file = user_file
        self.user_pkl_file = user_pkl
        self.user_data = pandas.read_csv(user_file, header=None)

    def save_to_redis_pkl(self):
        """ 基于pkl文件写入 """
        with open(self.user_pkl_file, mode='rb') as file:
            ens = pickle.load(file)
        for uid, value in ens.items():
            uid = str(uid) + "_" + Indicators.entropy
            value = float("%.5f" % value)
            self.user_client.set(uid, str(value))


    def save_to_redis(self):
        """ 基于计算写入redis """
        uid_result, max_interval, max_num = count_post_num(self.user_data)
        ens = count_information_entropy(uid_result, max_num, max_interval)  # 获取信息熵的结果
        for uid, value in ens.items():
            uid = str(uid) + "_" + Indicators.entropy
            value = float("%.5f" % value)
            self.user_client.set(uid, str(value))

def __main():
    outfile = "zhangDanFeng_entropy.pkl"
    # incsv = "F:/scrapy/sina_data1.0.0/zhangDanFeng/parsedData/all_data.csv"
    # # save_entry(incsv, outfile)
    with open(outfile, mode='rb') as file:
        ens = pickle.load(file)
    print(ens)

    # my_dict = ens
    # key_max = max(my_dict.keys(), key=(lambda k: my_dict[k]))
    # key_min = min(my_dict.keys(), key=(lambda k: my_dict[k]))
    # print("信息熵最高用户ID:%s, 熵值:%.12f" % (key_max, my_dict[key_max]))
    # print("信息熵最低用户ID:%s, 熵值:%.12f" % (key_min, my_dict[key_min]))
    # print("排序结果：")
    # d = sorted(ens.items(), key=operator.itemgetter(1), reverse=True)  # 从大到小排序
    # print(d)
    # print()
    # for (uid, ens_v) in d:
    #
    #     try:
    #         days = active_days[uid]
    #         if days == None:
    #             print("无此用户")
    #         else:
    #             print(uid)
    #             print(ens_v)
    #             print(len(days))
    #     except Exception as e:
    #         pass
    #     print()


if __name__ == "__main__":
    event = EventEntropy(user_pkl=pkl_fanChengCheng_entropy, user_db=fanChengCheng_db)
    event.save_to_redis_pkl()

    event = EventEntropy(user_pkl=pkl_jueDiQiuSheng_entropy, user_db=jueDiQiuSheng_db)
    event.save_to_redis_pkl()

    event = EventEntropy(user_pkl=pkl_zhangDanFeng_entropy, user_db=zhangDanFeng_db)
    event.save_to_redis_pkl()

    event = EventEntropy(user_pkl=pkl_zhaiTianLin_entropy, user_db=zhaiTianLin_db)
    event.save_to_redis_pkl()

