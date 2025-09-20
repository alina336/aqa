from typing import List,Dict
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
def words_count():
    words = list(map(str, input("Введите слова через запятую: ").split(',')))
    result_dict={}
    for word in words:
        if word not in result_dict:
            result_dict[word] = 1
        else:
            result_dict[word] += 1

    # for word in words_list:
    #     result_dict[word] = result_dict.get(word,0)+1

    # result_dict = Counter(words_list)
    print(result_dict)


words_count()

# 2
list1 = [1, 2, 4]
list2 = [4, 3, 3, 6, 7, 8, 0]


def unique(*lists):
    uniq_list = []
    for lst in lists:
        for num in lst:
            if num not in uniq_list:
                uniq_list.append(num)
            else:
                continue
    print(*uniq_list, sep=',')


unique(list1, list2)


# 3
def analyze_phrases(**kwargs):
    result = {}
    for k, v in kwargs.items():
        result[k] = (v, len(v))
    print(result)


phrases_dict = analyze_phrases(greeting="Hello World", python_fun="Python is fun",
                               coding="I like coding", powerful="Python is powerful")
