# coding:utf-8
import pinyin
import re
import json
import pandas as pd


class PasswordAnalyse:
    path = ''
    infoset = {}
    wordlist = []
    keylist = []

    def __init__(self, path=path, infoset=infoset, wordlist=wordlist, keylist=keylist):
        self.path = path
        self.infoset = infoset
        self.wordlist = wordlist
        self.keylist = keylist

    # N
    def process_name(self, name):
        name_pinyin = pinyin.get(name, format="strip", delimiter=" ")
        name_initial = ''.join(pinyin.get_initial(name).split())
        name_initial_upper = ''.join(pinyin.get_initial(name).split()).upper()
        name_family = name_pinyin.split()[0]
        name_family_i = name_pinyin.split()[0].capitalize()
        name_last = ''.join(name_pinyin.split()[1:])
        name_fl = name_pinyin.split()[0] + ''.join(pinyin.get_initial(name).split()[1:])

        if name[:2] in ['欧阳', '司徒', '南宫', '夏侯', '西门', '公孙', '司马', '诸葛', '皇甫']:
            name_family = ''.join(name_pinyin.split()[0:1])
            name_last = ''.join(name_pinyin.split()[1:])
            name_fl = name_pinyin.split()[0] + ''.join(pinyin.get_initial(name).split()[2:])

        name_pinyin = ''.join(name_pinyin.split())
        name_result = [name_pinyin, name_family, name_last, name_initial, name_initial_upper, name_fl, name_family_i]
        return name_result

    # E
    def process_email(self, email):
        full_email = email.split('@')[0]

        pattern = re.compile('([a-zA-Z]+)')
        letter_email = re.findall(pattern, full_email)
        if letter_email:
            letter_email = letter_email[0]
        else:
            letter_email = ''

        pattern = re.compile('([0-9]+)')
        num_email = re.findall(pattern, full_email)
        if num_email:
            num_email = num_email[0]
        else:
            num_email = ''

        email_result = [full_email, letter_email, num_email]
        return email_result

    # A
    def process_account(self, account_name):
        full_account = account_name

        pattern = re.compile('([a-zA-Z]+)')
        letter_account = re.findall(pattern, full_account)
        if letter_account:
            letter_account = letter_account[0]
        else:
            letter_account = ''

        pattern = re.compile('([0-9]+)')
        num_account = re.findall(pattern, full_account)
        if num_account:
            num_account = num_account[0]
        else:
            num_account = ''

        account_result = [full_account, letter_account, num_account]
        return account_result

    # B
    def process_birthday(self, birthday):
        year = birthday[0:4]
        month = birthday[4:6]
        day = birthday[6:8]
        birthday_YMD = birthday
        birthday_MDY = month + day + year
        birthday_DMY = day + month + year
        birthday_D = day
        birthday_Y = year
        birthday_YM = year + month
        birthday_MY = month + year
        birthday_last2YMD = year[2:4] + month + day
        birthday_last2MDY = month + day + year[2:4]
        birthday_last2DMY = day + month + year[2:4]

        birthday_result = [birthday_YMD, birthday_MDY, birthday_DMY, birthday_D, birthday_Y, birthday_YM,
                           birthday_MY, birthday_last2YMD, birthday_last2MDY, birthday_last2DMY]
        return birthday_result

    # I
    def process_idcard(self, id_card):
        idcard_last4 = id_card[-4:]
        idcard_last6 = id_card[-6:]

        result_idcard = [idcard_last4, idcard_last6]
        return result_idcard

    # Judge if special pattern in password
    # W
    def process_word(self, password):
        # Lin Y.C.
        word_result = []
        for word in self.wordlist:
            word = word.strip('\n')
            if word in password:
                word_result.append(word)
        return word_result

    # D
    def process_date(self, password):
        # Wu H.
        pass

    # K
    def process_key(self, password):
        # Li H.M.
        key_result = []
        for key in self.keylist:
            key = key.strip('\n')
            if key in password:
                key_result.append(key)
        return key_result

    # Analyse
    def password_analyse(self, info):
        name_result = self.process_name(info.get('name'))
        email_result = self.process_email(info.get('email'))
        account_result = self.process_account(info.get('account_name'))
        birthday_result = self.process_birthday(info.get('birthday'))
        idcard_result = self.process_idcard(info.get('id_card'))

        # pattern-analyse
        password = info.get('password')
        flag = [0 for i in range(len(password))]

        # name, email, birthday, account, id_card
        flag = self.parse_pattern(password, 'N', name_result, flag)
        flag = self.parse_pattern_birthday(password, 'B', birthday_result, flag)
        flag = self.parse_pattern(password, 'E', email_result, flag)
        flag = self.parse_pattern(password, 'A', account_result, flag)
        flag = self.parse_pattern(password, 'I', idcard_result, flag)

        # word, pinyin, date, key
        word_result = self.process_word(password)
        flag = self.parse_pattern_wdk(password, 'W', word_result, flag)
        key_result = self.process_key(password)
        flag = self.parse_pattern_wdk(password, 'K', key_result, flag)

        # other
        for i in range(len(flag)):
            if flag[i] == 0:
                if password[i].isalpha():
                    flag[i] = ('L', password[i])
                elif password[i].isdigit():
                    flag[i] = ('D', password[i])
                else:
                    flag[i] = ('S', password[i])

        final_pattern = self.get_pattern(password, flag)
        return final_pattern

    def get_pattern(self, password, flag):
        final_pattern = dict()
        flag_list = flag
        # flag_list.sort(key=flag.index)
        content = []
        pattern_set = []

        for i in range(len(flag_list)):
            item = list(flag_list[i])
            pattern = item[0]
            if pattern in ['L', 'D', 'S']:
                if i and pattern == flag_list[i - 1][0][0]:
                    continue
                else:
                    length = 1
                    for j in range(i + 1, len(flag_list)):
                        if flag_list[j][0] == pattern:
                            item[1] = item[1] + flag_list[j][1]
                            length += 1
                        else:
                            break
                    item[0] = pattern + str(length)
                    pattern_set.append(item[0])
                    content.append([item[0], item[1]])
            else:
                if i and item == list(flag_list[i - 1]):
                    continue
                pattern_set.append(item[0])
                content.append(item)

        final_pattern['pattern'] = pattern_set
        final_pattern['content'] = content

        return final_pattern

    def parse_pattern_wdk(self, password, mark, result_set, flag):
        for item in result_set:
            if len(item) > 1:
                find_result = password.find(item)
                start_position = password.index(item)
                end_position = start_position + len(item) - 1
                item_length = len(item)
                overlap = self.judge_overlap(start_position, end_position, flag)
                current_type = mark + str(item_length)
                if overlap:
                    # pattern.append([mark, item_length, start_position, end_position, item])
                    for i in range(start_position, end_position + 1):
                        flag[i] = (current_type, item)
        return flag

    def parse_pattern_birthday(self, password, mark, result_set, flag):
        for item in result_set:
            if len(item) > 1:
                find_result = password.find(item)
                short_item = ''
                short_flag = False
                if find_result == -1 and len(item) >= 4:
                    short_item = ''.join(item.split('0'))
                    find_result = password.find(short_item)
                    if find_result != -1:
                        short_flag = True

                if find_result != -1:
                    start_position = find_result
                    if short_flag:
                        end_position = start_position + len(short_item) - 1
                    else:
                        end_position = start_position + len(item) - 1
                    result_type = result_set.index(item) + 1
                    overlap = self.judge_overlap(start_position, end_position, flag)
                    current_type = mark + str(result_type)
                    if overlap:
                        # pattern.append([mark, result_type, start_position, end_position, item])
                        for i in range(start_position, end_position + 1):
                            flag[i] = (current_type, item)
        return flag

    def parse_pattern(self, password, mark, result_set, flag):
        for item in result_set:
            if len(item) > 1:
                find_result = password.find(item)
                if find_result != -1:
                    start_position = find_result
                    end_position = start_position + len(item) - 1
                    result_type = result_set.index(item) + 1
                    overlap = self.judge_overlap(start_position, end_position, flag)
                    current_type = mark + str(result_type)
                    if overlap:
                        # pattern.append([mark, result_type, start_position, end_position, item])
                        for i in range(start_position, end_position + 1):
                            flag[i] = (current_type, item)
        return flag

    def judge_overlap(self, start_position, end_position, flag):
        if flag[start_position] == 0 and flag[end_position] == 0:
            return True
        elif start_position == 0 and flag[end_position] == 0:
            return True
        elif flag[start_position] != flag[start_position - 1] and flag[end_position] == 0:
            return True
        elif flag[start_position] == 0 and end_position == len(flag) - 1:
            return True
        elif flag[start_position] == 0 and flag[end_position] != flag[end_position + 1]:
            return True
        else:
            return False

    # Statistics
    def analyse_total(self):
        password_set = self.infoset.get('password')
        name_set = self.infoset.get('name')
        email_set = self.infoset.get('email')
        id_card_set = self.infoset.get('id_card')
        account_name_set = self.infoset.get('account_name')

        pattern_list = []
        content_list = []
        name_list = []

        for i in range(len(password_set)):
            info = {
                'name': str(name_set[i]),
                'birthday': str(id_card_set[i][6:14]),
                'password': str(password_set[i]),
                'email': str(email_set[i]),
                'id_card': str(id_card_set[i]),
                'account_name': str(account_name_set[i]),
            }
            result = self.password_analyse(info)

            pattern = result.get('pattern', [])
            pattern_list.append(tuple(pattern))
            # self.save_pattern('pattern', pattern)

            content = result.get('content', [])
            if not content:
                print('Content Error!')
            else:
                for item in content:
                    current_content = str(item[0]) + ',' + str(item[1])
                    content_list.append(current_content)
                    name_list.append(item[0])

        pattern_set = set(pattern_list)
        content_set = set(content_list)
        pattern_length = len(pattern_list)

        # process pattern
        statistic_list = []
        for item in pattern_set:
            count = pattern_list.count(item)
            proportion = count * 1.0 / pattern_length * 100
            item_list = [item, count, proportion]
            statistic_list.append(item_list)

        statistic_list = sorted(statistic_list, key=lambda c: int(c[1]), reverse=True)
        filename = self.path + 'pattern.txt'
        file = open(filename, 'w')
        for i in statistic_list:
            statistic_dict = {
                'pattern': i[0],
                'count': str(i[1]),
                'proportion': str(i[2])
            }
            file.write(json.dumps(statistic_dict) + '\n')
        file.close()

        # print('pattern finish')

        # process content
        content_dict = dict()
        for item in content_set:
            count = content_list.count(item)
            item = item.split(',')
            proportion = count * 1.0 / name_list.count(item[0]) * 100
            statistic_result = [item[0], item[1], str(count), str(proportion)]
            filename = item[0]

            # Order
            if filename in content_dict.keys():
                content_dict[filename].append(statistic_result)
            else:
                content_dict[filename] = [statistic_result]

        for key in content_dict.keys():
            class_info = content_dict[key]
            class_info = sorted(class_info, key=lambda class_item: int(class_item[2]), reverse=True)
            filename = self.path + key + '.txt'
            file = open(filename, 'w')
            for i in class_info:
                file.write(','.join(i) + '\n')
            file.close()


if __name__ == '__main__':
    # read-data
    data = pd.read_csv('data/12306.csv', encoding='utf-8')
    data = data.drop_duplicates()
    password = data['password'].values
    email = data['email'].values
    name = data['name'].values
    id_card = data['id_card'].values
    account_name = data['account_name'].values
    phone_num = data['phone_num'].values

    # Read-wordlist
    word_list = open('data/wordlist.txt', 'r').readlines()
    key_list = open('data/keylist.txt', 'r').readlines()

    # Generate info-set
    info_set = {
        'password': password,
        'email': email,
        'name': name,
        'id_card': id_card,
        'account_name': account_name,
    }

    # Analyse
    ana = PasswordAnalyse('result/', info_set, word_list, key_list)
    ana.analyse_total()

    print('Finish')

