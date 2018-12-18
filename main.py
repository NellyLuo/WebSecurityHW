# coding:utf-8
import argparse
import pandas as pd
from password_analyse import PasswordAnalyse
from generate_password import GeneratePassword

DATA_PATH = 'data/'
WORD_LIST_PATH = 'data/wordlist.txt'
KEY_LIST_PATH = 'data/keylist.txt'
TRAIN_DATA_PATH = 'data/12306.csv'
PATTERN_FILE = 'result/pattern.txt'
PATTERN_PATH = 'result/'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", help="Number of password", type=int)

    parser.add_argument("-n", "--name", help="Input name")
    parser.add_argument("-b", "--birthday", help="Input Birthday")
    parser.add_argument("-e", "--email", help="Input Email")
    parser.add_argument("-i", "--idcard", help="Input ID card")
    parser.add_argument("-a", "--account", help="Input Account")

    parser.add_argument("-g", "--generate", help="No information", action='store_true')
    parser.add_argument("-t", "--train", help="Train your own model", action='store_true')
    parser.add_argument("--analyse", help="Analyse your own data")

    args = parser.parse_args()
    count = args.count
    pattern_file = open(PATTERN_FILE, 'r')
    pattern_set = pattern_file.readlines()
    gen = GeneratePassword(PATTERN_PATH, pattern_set)

    # User give info
    if args.name and args.birthday and args.email and args.idcard and args.account:
        info = {
            'name': args.name,
            'birthday': args.birthday,
            'email': args.email,
            'id_card': args.idcard,
            'account_name': args.account
        }

        if count:
            result = gen.generate_info(info, count)
        else:
            result = gen.generate_info(info)

        gen.save_result(result)
        gen.show_result(result)

    elif args.generate:
        if count:
            result = gen.generate_no_info(count)
        else:
            result = gen.generate_no_info()

        gen.save_result(result)
        gen.show_result(result)

    elif args.train:
        # read data
        data = pd.read_csv(TRAIN_DATA_PATH, encoding='utf-8')
        password = data['password'].values
        email = data['email'].values
        name = data['name'].values
        id_card = data['id_card'].values
        account_name = data['account_name'].values
        phone_num = data['phone_num'].values
        info_set = {
            'password': password,
            'email': email,
            'name': name,
            'id_card': id_card,
            'account_name': account_name,
        }

        # read wordlist
        word_list = open(WORD_LIST_PATH, 'r').readlines()
        key_list = open(KEY_LIST_PATH, 'r').readlines()

        print('=== Train Start ===\n')
        ana = PasswordAnalyse('/result_test', info_set, word_list, key_list)
        ana.analyse_total()
        print('=== Train Finish ===\n')

    elif args.analyse:
        print("-- To be Continued. --\n")
        print("-- Maybe there will be an Edition-3. Who knows. --\n")
        analyse_content = args.analyse
        if analyse_content == 'word':
            pass
        elif analyse_content == 'keyboard':
            pass
        elif analyse_content == 'structure':
            pass
        elif analyse_content == 'special':
            pass
        elif analyse_content == 'date':
            pass
        elif analyse_content =='cd_attack':
            pass
        pass

    else:
        print("Oops! Failed to deal with the parameter. Please input again.\n")
