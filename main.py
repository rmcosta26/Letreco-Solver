import string
import itertools
from math import log2
import pickle
import numpy as np


def countnpos(word):
    un = np.unique(list(word))
    a = []
    for i in un:
        pos = []
        ind = 0
        for j in range(word.count(i)):
            ind = list(word).index(i, ind)
            pos.append(ind)
            ind += 1
        a.append((i, word.count(i), pos))
    return a


def freq_letter(database):
    alf = list(string.ascii_uppercase)
    freq = []
    for i in range(len(alf)):
        count = 0
        for j in database:
            if alf[i] in j:
                count += 1
        count = round(count/len(database) * 100, 2)
        freq.append((alf[i], count))

    freq = dict(freq)

    return freq


def filter_postrue(database, letter, pos):
    data = []
    for i in database:
        if letter == i[pos]:
            data.append(i)
    return data


def filter_posfalse(database, letter, pos):
    data = []
    for i in database:
        if letter != i[pos]:
            data.append(i)
    return data


def filter_letterfalse(database, letter):
    data = []
    for i in database:
        if letter not in i:
            data.append(i)
    return data


def filter_lettertrue(database, letter):
    data = []
    for i in database:
        if letter in i:
            data.append(i)
    return data


def receive_info(database, guess, result):
    data = []
    data = database
    for i in range(5):
            # print(i)
        if result[i] is 'y':
            data = filter_lettertrue(data, guess[i])
            data = filter_postrue(data, guess[i], i)

        elif result[i] is 'm':
            data = filter_lettertrue(data, guess[i])
            data = filter_posfalse(data, guess[i], i)

        elif result[i] is 'n':
            if len(np.unique(guess)) == 5:
                data = filter_letterfalse(data, guess[i])
            else:
                if guess.count(guess[i]) > 1:
                    l = []
                    ind = 0
                    for k in range(guess.count(guess[i])):
                        ind = list(guess).index(guess[i], ind)
                        l.append(result[ind])
                        ind += 1
                    if len(np.unique(l)) != 1:
                        data = filter_lettertrue(data, guess[i])
                        data = filter_posfalse(data, guess[i], i)
                    else:
                        data = filter_letterfalse(data, guess[i])
                else:
                    data = filter_letterfalse(data, guess[i])
    return data


def possible_match_rate(database):
    matches = []
    for word in database:
        sum = 0
        comb = itertools.combinations_with_replacement(['y', 'm', 'n'], 5)
        for i in comb:
            data = database
            data = receive_info(data, word, str(i[0]+i[1]+i[2]+i[3]+i[4]))
            p = len(data)/len(database)
            if p != 0:
                sum += p * (log2(1)-log2(p))
        matches.append((word, sum))
    matches = dict(matches)
    return matches


def sorted_rate(database):
    data = database
    global rate_sorted
    temp = []
    for i in data:
        temp.append((i, rate_sorted[i]))
    temp = dict(temp)
    temp = dict(sorted(temp.items(), key=lambda x: x[1], reverse=True))
    return temp


def return_sorted_bylen(data, size):
    temp = list(data.keys())
    temp = temp[:size]
    sbl = []
    for i in temp:
        sbl.append((i, data[i]))
    sbl = dict(sbl)
    return sbl


def run_manual(database):
    global rate_sorted
    data = database
    # print(rate_sorted)
    for j in range(6):
        guess = str(input())
        result = str(input())
        data = receive_info(data, guess, result)
        r = sorted_rate(possible_match_rate(data))
        print(return_sorted_bylen(r, 5))
        print(len(r))
        print('\n')


with open('palavras-letreco.pickle', 'rb') as f:
    l_database = pickle.load(f)

with open('rate_sorted.pickle', 'rb') as f:
    rate_sorted = pickle.load(f)


run_manual(l_database)
