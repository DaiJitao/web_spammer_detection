import pandas
from tools import get_num_all_closed, get_num, date_to_seconds, group
from math import log2

''' 数据标注 '''


def get_reviews_num(incsv, uid):
    ''' 统计发帖的数量 '''
    data = pandas.read_csv(incsv, header=None)
    data = data[[0, 7]]  # x['6525265489']
    d = data[data[0] == 7117146750]
    print(d[7])
    dates = list(map(date_to_seconds, [i for i in d[7]]))
    max_cmt_num = 10  # 用户最长的评论数
    all_cmt_num = len(dates)  # 获取用户的评论数
    dates.sort()  # 从小到大排序
    min_, max_ = dates[0], dates[-1]
    result = group(min_, max_, max_cmt_num)
    print(result)


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


if __name__ == "__main__":
    incsv = "F:/scrapy/sina_data1.0.0/fanChengCheng/parsedData/all_data.csv"
    get_reviews_num(incsv, 0)

    norm1 = (2 / 12) * log2(12 / 2) + 4 * (4 / 12) * log2(12 / 4)
    shui1 = (1 / 12) * log2(1 / 12) + (8 / 12) * log2(12 / 8) + (3 / 12) * log2(12 / 3)
    shui2 = (10 / 12) * log2(12 / 10)
    shui3 = (12 / 12) * log2(1)
    print("norm %0.18f, shui1:%.18f, shui2 %.18f, shui3:%.18f" % (norm1, shui1, shui2, shui3))
