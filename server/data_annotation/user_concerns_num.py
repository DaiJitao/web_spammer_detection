

''' 统计每一个用户的事件关注度 '''

d =  \
{'1': '7045569170',
 '8': '1918436011',
 '3': '5837767229',
 '6': '2691025184',
 '9': '5144973254',
 '17': '2810385795',
 '7': '3944698962',
 '11': '1874813260',
 '15': '1774766301',
 '30': '1957968052',
 '20': '2483840887',
 '26': '6303627386',
 '4': '5900138307',
 '14': '1822748794',
 '13': '1571209957',
 '16': '2708382817',
 '25': '1907083965'}

for i in d:
    print(i)

def sort_dict_by_key(dict_):
    tmp = [int(i) for i in list(dict_.keys())]
    tmp.sort()
    res = {}
    for key in tmp:
        key = str(key)
        res[key] = dict_[key]
    return res

def my_range(f=0, end=10, st=1):
    res = 0
    while res < end:
        yield res
        res += 1