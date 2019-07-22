from tools.utils import RedisClient, list_all_users, get_all_data_iterator, Indicators
from conf.config import redis_host, redis_port, fanChengCheng_db, zhaiTianLin_db, zhangDanFeng_db, jueDiQiuSheng_db, \
    all_data_db, incsv_haiTianLin, incsv_zhangDanFeng, incsv_jueDiQiuSheng

'''统计用户的新闻关注度
'''

client = RedisClient(host=redis_host, port=redis_port, db=all_data_db)  # 连接全局数据库


def list_all_user_attention_num(incsv):
    # 计算每一个用户的新闻关注度，并写入redis, 数据为整个月全量数据
    data = get_all_data_iterator(incsv=incsv, header=True)
    for seg in data:
        for uid, newsid in seg.values:
            uid = str(uid)
            redis_res = client.get(uid) # 取出用户关注的新闻
            news_code = client.get(newsid)  # 取出新闻编码
            uid_concern = uid + "_" + Indicators.concern
            if redis_res == None:  # 如果该值为不存在，则newsid存入redis
                # 获取新闻编码
                client.set(uid_concern, news_code)
            else:  # 如果不为空
                redis_res = redis_res + "_"+ news_code
                client.set(uid_concern, redis_res)
    print("计算所有用户新闻关注度完毕,写入redis成功！")


class NewsAttentionNum(object):
    def __init__(self, user_file, user_db):
        self.users = list_all_users(incsv=user_file)
        try:
            self.user_client = RedisClient(host=redis_host, port=redis_port, db=user_db)
        except Exception as e:
            print("redis连接失败", e)

    def concern_nums(self):
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
            print(uid_concern)


if __name__ == "__main__":
    # news = NewsAttentionNum(incsv_haiTianLin, zhaiTianLin_db)
    # news.concern_nums()
    # news = NewsAttentionNum(incsv_zhangDanFeng, zhangDanFeng_db)
    # news.concern_nums()
    # news = NewsAttentionNum(incsv_jueDiQiuSheng, jueDiQiuSheng_db)
    # news.concern_nums()
    pass

