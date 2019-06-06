import pandas
from pprint import pprint
from math import log2
import time, datetime

''' 数据标注 '''


def date_to_seconds(date, mode="%Y-%m-%d %H:%M:%S"):
    ''' 日期转化为秒 '''
    timeArray = time.strptime(date, mode)
    timeStamp = int(time.mktime(timeArray))  # 秒
    return timeStamp

def group(min_, max_, num):
    interval_max = max_ - min_
    avg_interval = round((interval_max / num), 3) # 保留三位小数
    result = []
    for i in range(num):
        if i == 0:
            result.append( (min_, min_+ avg_interval) )
        elif i == (num-1):
            start = i * avg_interval + min_
            result.append((start, max_))
        else:
            start = round((i * avg_interval + min_), 3)
            end = round( (start + avg_interval), 3)
            result.append((start, end))
    return result


def get_reviews_num(incsv, uid):
    ''' 统计发帖的数量 '''
    data = pandas.read_csv(incsv, header=None)
    data = data[[0, 7]]  # x['6525265489']
    d = data[data[0] == 7117146750 ]
    print(d[7])
    dates = list(map(date_to_seconds, [i for i in d[7]]))
    max_cmt_num = 10 # 用户最长的评论数
    all_cmt_num = len(dates) # 获取所有的评论数
    dates.sort() # 从小到大排序
    min_, max_ = dates[0], dates[-1]
    result = group(min_, max_, max_cmt_num)
    print(result)






if __name__ == "__main__":
    incsv = "F:/scrapy/sina_data1.0.0/fanChengCheng/parsedData/all_data.csv"
    get_reviews_num(incsv, 0)
    shui = (6/10)*log2(10/6) + (3/10) * log2(10/3) + (1/10)*log2(10/1)
    norm = (2/10)*log2(10/2) + (1/10)*log2(10/1)
    norm2 = 6 * (1 / 10) * log2(10 / 1)
    print("norm %0.18f, norm2:%.18f, 水军H %.18f" %(norm, norm2, shui))
    # print(group(10, 35, 3))



