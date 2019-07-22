from pyspark import SparkContext, SparkConf
import time
import csv


# d = [("1", "dai"), ("1", "hou"), ("2", "yanzhen"), ("2", "yanzhen2"), ("3", "wu")]



def dateTime_to_date(datetime, mode="%Y-%m-%d %H:%M:%S"):
    ''' 日期转换 '''
    array = time.strptime(datetime, mode)
    year = str(array.tm_year)
    mon = str(array.tm_mon)
    if len(mon) != 2:
        mon = "0" + mon
    day = str(array.tm_mday)
    if len(day) !=2 :
        day = "0" + day
    day = str(year + mon + day)
    return day

def read_csv(incsv):
    result = []
    with open(incsv, "r") as csvfile:
        lines = csv.reader(csvfile)
        count = 0
        for i in lines:  # 避免表头
            if count > 0 and len(i) > 7:
                id, time_ = str(i[0]), dateTime_to_date(i[7])
                result.append((id, time_))
            count += 1
    return result

def count_days(y):
    if len(y) == 1:
        return 1
    else:
        return y[-1] - y[0] + 1

def count(uid, y):
    '''
    x 为uid
    '''
    days = count_days(y)
    return (str(days), uid)


''' 文件启动方法 $SPARK_HOME/bin/spark-submit active_days_spark.py  ; pyspark --master yarn'''
sc = SparkContext("local[4]", "active days App")

incsv = "/mnt/daijitao/projects/spammer_detection/data/sina_data/comments_data/parsed/all_data_4.csv"
outfile_date = "/active_days_date" # hadoop路径
outfile_num = "/active_days_num"

d = read_csv(incsv)  # 读取数据
rdda = sc.parallelize(d, 500)

# res.repartition(1).saveAsTextFile(outfile) # 中间计算结果保存

# 统计用户的活跃天数 第二次计算
# infile = "file:///mnt/daijitao/projects/spammer_detection/data/result_active_days.txt"
# rdd2 = sc.textFile(infile)
res = rdda.reduceByKey(lambda x, y : str(x) + "_" + str(y))
rdd1 = res.map(lambda row: (row[0], sorted([ int(i) for i in set(row[1].split("_"))])     ))
rdd1.take(100)
rdd3 = rdd1.map(lambda row: count(row[0], row[1]) ) # 日期混合
rdd4 = rdd3.reduceByKey(lambda x, y: str(x) + "_" + str(y))
# rdd4.repartition(1).saveAsTextFile(outfile_date)
# rdd4.coalesce(1).saveAsTextFile(outfile_date)
rdd5 = rdd4.map(lambda row: {row[0]:len(row[1].split("_"))} )
rdd5.repartition(1).saveAsTextFile("/active_num_dict")
print("文件保存成功！")

m = 2
n = 7
res = []
for k in range(m, n+1):
    for i in range(k, 8):
        t = (i-k, i)
        res.append(t)