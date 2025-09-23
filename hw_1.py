from typing import List, Dict
from collections import Counter

'''
HW_2
1) Написать функцию, которая принимает любое количество слов и считает сколько раз это слово повторилось,
результат вернуть в виде переменной.
2) Написать функцию, которая принимает любое количество списков и возвращает все уникальные числа.
3) Создай функцию ana, где ключи — имена фраз, а значения — сами строки.
(Вызов будет в виде phrases_dict = analyze_phrases(greeting="Hello World", python_fun="Python is fun",
coding="I like coding", powerful="Python is powerful")
Функция возвращает словарь, где ключ — имя фразы, а значение — кортеж из длины фразы и количества слов
'''


# 1
def words_count(words):
    result_dict = {}
    for word in words:
        if word not in result_dict:
            result_dict[word] = 1
        else:
            result_dict[word] += 1

    # for word in words_list:
    #     result_dict[word] = result_dict.get(word,0)+1

    # result_dict = Counter(words_list)
    return result_dict


words = ['one', 'two', 'three', 'four', 'two', 'four', 'two']
print(words_count(words))

# 2
list1 = [1, 2, 4]
list2 = [4, 3, 3, 6, 7, 8, 0]


def unique(*lists):
    uniq = set()
    for l in lists:
        uniq.update(l)
    return uniq

print(unique(list1, list2))


# 3
def analyze_phrases(**kwargs):
    result = {}
    for k, v in kwargs.items():
        result[k] = (len(v), len(v.split()))
    return result


phrases_dict = analyze_phrases(greeting="Hello World", python_fun="Python is fun",
                               coding="I like coding", powerful="Python is powerful")

print(phrases_dict)