import time


def get_num(__min, __max, lst):
    ''' 获取在指定区间内的元素，左闭右开 Close left and open right'''
    res = []
    for i in lst:
        if i >= __min and i < __max:
            res.append(i)
    return res


def get_num_all_closed(__min, __max, lst):
    ''' 获取在指定区间内的元素，左闭右闭 Close left and right'''
    res = []
    for i in lst:
        if i >= __min and i <= __max:
            res.append(i)
    return res


def date_to_seconds(date, mode="%Y-%m-%d %H:%M:%S"):
    ''' 日期转化为秒 '''
    timeArray = time.strptime(date, mode)
    timeStamp = int(time.mktime(timeArray))  # 秒
    return timeStamp


def group(min_, max_, num):
    interval_max = max_ - min_
    avg_interval = round((interval_max / num), 3)  # 保留三位小数
    result = []
    for i in range(num):
        if i == 0:
            result.append((min_, min_ + avg_interval))
        elif i == (num - 1):
            start = i * avg_interval + min_
            result.append((start, max_))
        else:
            start = round((i * avg_interval + min_), 3)
            end = round((start + avg_interval), 3)
            result.append((start, end))
    return result
