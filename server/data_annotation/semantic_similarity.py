from conf.config import stop_words_file, fanChengCheng_db, redis_host, redis_port, incsv_fanChengCheng, zhaiTianLin_db, \
    incsv_haiTianLin, jueDiQiuSheng_db, incsv_jueDiQiuSheng, zhangDanFeng_db, incsv_zhangDanFeng
import jieba_fast as jieba
from tools.utils import list_all_users_text, RedisClient, list_all_users, Indicators
import redis
import pickle

''' 链接redis '''
client = redis.Redis(host=redis_host, port=redis_port, db=fanChengCheng_db, decode_responses=True)

''' 数据标注 '''


class SemanticSimilarity(object):
    def __init__(self):
        pass

    def cut(self, text):
        '''
        分词
        :param text:
        :return:
        '''
        try:
            d = [line.rstrip() for line in open(stop_words_file, mode='r', encoding='utf-8')]  # 停用词
            stop_words = {}.fromkeys(d)
            cut_words = jieba.cut(text)
        except Exception as e:
            print(e)
        cut_words_clean = []
        for seg in cut_words:
            if seg not in stop_words:
                cut_words_clean.append(seg)  # 去除停用词

        return cut_words_clean

    def common_words(self, cutwds_lst1, cutwds_lst2):
        '''
        找出共现词
        :param cutwds_lst1:
        :param cutwds_lst2:
        :return: []
        '''
        cmn_words = []
        tmp = {}.fromkeys(cutwds_lst2)
        for words in cutwds_lst1:
            if words in tmp:
                cmn_words.append(words)
        return cmn_words

    def short_words_num(self, lst1, lst2):
        return min(len(lst1), len(lst2))

    def ratio(self, texts, thred=0.8):
        '''
        计算语义重复率
        :param texts: [ doc, doc ]
        :return:
        '''
        cut_texts = []
        # 对所有文本进行分词
        for text in texts:
            seg = self.cut(text)
            cut_texts.append(seg)
        ratios = []  # 该用户的比率
        size = len(cut_texts)
        for i in range(size):
            for j in range(i + 1, size):
                common_words_ = self.common_words(cut_texts[i], cut_texts[j])
                n = self.short_words_num(cut_texts[i], cut_texts[j])
                if n != 0:
                    ratio = len(common_words_) / n
                else:
                    ratio = 0.0
                if ratio > thred:
                    ratio = float("%.3f" % ratio)
                    ratios.append(ratio)
        return ratios


class EventSemanticSim():
    ''' 统计每个事件的语义重复率 '''

    def __init__(self, user_file, user_db):
        self.user_file = user_file
        self.user_client = RedisClient(host=redis_host, port=redis_port, db=user_db)

    def save_redis(self):
        ss = SemanticSimilarity()  # 初始化
        all_users = list_all_users(self.user_file)
        for key in all_users:
            texts = list_all_users_text(self.user_file, key)  # 获取所有文本
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
    # event = EventSemanticSim(user_file=incsv_fanChengCheng, user_db=fanChengCheng_db)
    # event.save_redis()

    event = EventSemanticSim(user_file=incsv_zhangDanFeng, user_db=zhangDanFeng_db)
    event.save_redis()

    event = EventSemanticSim(user_file=incsv_haiTianLin, user_db=zhaiTianLin_db)
    event.save_redis()

    event = EventSemanticSim(user_file=incsv_jueDiQiuSheng, user_db=jueDiQiuSheng_db)
    event.save_redis()