import numpy as np
import collections


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


# stop_words = __stop_words
# STOP_WORDS = __stop_words()


class Stack(object):
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.stack = collections.deque([])

    def push(self, x):
        """
        self.stack = []
        Push element x onto stack.
        :type x: int
        :rtype: void
        """
        self.stack.append(x)
        q = self.stack
        for i in range(len(q) - 1):
            q.append(q.popleft())

    def pop(self):
        """
        Removes the element on top of the stack and returns that element.
        :rtype: int
        """
        return self.stack.popleft()

    def top(self):
        """
        Get the top element.
        :rtype: int
        """
        return self.stack[0]

    def empty(self):
        """
        Returns whether the stack is empty.
        :rtype: bool
        """
        if len(self.stack) == 0:
            return True
        else:
            return False


if __name__ == "__main__":
    pass
