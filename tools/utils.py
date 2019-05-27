import numpy as np

def __stop_words(file="../data/stopWords/StopWords.txt"):
    result = set()
    with open(file) as text:
        for line in text.readlines():
            result.add(line.strip())

    # with open("../data/stopWords/stopwords2.txt", encoding='utf-8') as file:
    #     for line in file.readlines():
    #         result.add(line.strip())
    return result

def all_index(data, v):
    result = []
    count = 0
    for value in data:
        if value == v:
            result.append(count)
        count += 1
    return result

stop_words = __stop_words

if __name__ == "__main__":
    pass


