# coding:utf-8
import pandas as pd
from password_analyse import PasswordAnalyse
from generate_password import GeneratePassword
from sklearn.model_selection import train_test_split

import re

if __name__ == '__main__':
    # read-data
    info = pd.read_csv('data/12306.csv', encoding='utf-8')
    x = info
    y = x.pop('password')

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

    # data = x_train
    # data['password'] = y_train.values
    #
    # password = data['password'].values
    # email = data['email'].values
    # name = data['name'].values
    # id_card = data['id_card'].values
    # account_name = data['account_name'].values
    # phone_num = data['phone_num'].values
    #
    # # Read-wordlist
    # word_list = open('data/wordlist.txt', 'r').readlines()
    # key_list = open('data/keylist.txt', 'r').readlines()
    #
    # # Generate info-set
    # info_set = {
    #     'password': password,
    #     'email': email,
    #     'name': name,
    #     'id_card': id_card,
    #     'account_name': account_name,
    # }
    #
    # # Analyse
    # ana = PasswordAnalyse('result_test/', info_set, word_list, key_list)
    # ana.analyse_total()
    #
    # print('Train Finish.')
    path = 'result_test/'
    pattern_file = open('result_test/pattern.txt', 'r')
    pattern_set = pattern_file.readlines()

    gen = GeneratePassword(path, pattern_set)
    # result = gen.generate_no_info()
    test_data = x_test
    test_data['password'] = y_test.values
    cnt = 0
    total = 0
    file_temp = open('forppt.csv', 'w')
    for item in test_data.values:
        per_info = {
            'name': item[1],
            'birthday': item[2][6:14],
            'account_name': item[3],
            'id_card': item[2],
            'email': item[0]
        }
        result = gen.generate_info(per_info, count=25)
        result = list([i[1] for i in result][:3000])
        if item[6] in result:
            cnt = cnt + 1
            print(result.index(item[6]))
            writerow = [item[0], item[1], item[6], str(result.index(item[6]))]
            file_temp.write(','.join(writerow) + '\n')
        total = total + 1

    propo = cnt * 1.0 / total
    file_temp.write(str(propo))
    print(propo)
