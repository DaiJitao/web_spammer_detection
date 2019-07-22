
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


if __name__ =="__main__":
    data = "2019-03-14 00:19:28"
    print(dateTime_to_date(data))