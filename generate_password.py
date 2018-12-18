# coding:utf-8
from password_analyse import PasswordAnalyse
import json

INFO = {
    'N': 'name', 'B': 'birthday', 'E': 'email', 'A': 'account_name', 'I': 'id_card',
}


class GeneratePassword:
    def __init__(self, path, pattern_set):
        self.path = path
        self.pattern_set = pattern_set

    def parse_info(self, info):
        name = info.get('name')
        email = info.get('email')
        account_name = info.get('account_name')
        id_card = info.get('id_card')
        birthday = info.get('birthday')

    def generate_no_info(self, count=10):
        # 'pattern' must be a list
        result_set = []
        for i in range(0, count):
            info = json.loads(self.pattern_set[i].strip('\n'))
            pattern = info.get('pattern', [])
            pattern_count = int(info.get('count', 0))
            proportion = info.get('proportion', 0.0)
            start_info = ','.join(['', '', str(pattern_count), str(proportion)])
            result_temp = [start_info]
            for item in pattern:
                filename = self.path + item + '.txt'
                file = open(filename, 'r')
                lines = file.readlines()
                lines_use = lines[:count]
                result_temp = self.multi_proportion(result_temp, lines_use)

            result_set += result_temp
            result_set = sorted(result_set, key=lambda x: x[3], reverse=True)

        return result_set

    def multi_proportion(self, list1, list2):
        result = []
        for i in list1:
            if type(i) is not list:
                i = i.strip('\n').split(',')
            for j in list2:
                if type(j) is not list:
                    j = j.strip('\n').split(',')
                re_pattern = i[0] + j[0]
                re_content = i[1] + j[1]
                re_count = int(i[2]) * int(j[2])
                re_proportion = float(i[3]) * float(j[3])

                result.append([re_pattern, re_content, str(re_count), re_proportion])
        # print(result)
        return result

    def generate_info(self, personal_info, count=10):
        # 'pattern' must be a list, 'content' must be a list
        result_set = []
        for i in range(0, count):
            info = json.loads(self.pattern_set[i].strip('\n'))
            pattern = info.get('pattern', [])
            pattern_count = int(info.get('count', 0))
            proportion = info.get('proportion', 0.0)
            start_info = ','.join(['', '', str(pattern_count), str(proportion)])
            result_temp = [start_info]
            for item in pattern:
                if item[0] in ['N', 'B', 'I', 'E', 'A']:
                    value = self.parse_value(item, personal_info)
                    info_list = [[str(item), value, 1, 100]]
                    if item[0] is 'B':
                        birthday_short = value.replace('0', '')
                        if birthday_short != value:
                            info_list.append([str(item), birthday_short, 1, 100])
                    result_temp = self.multi_proportion(result_temp, info_list)
                else:
                    filename = self.path + item + '.txt'
                    file = open(filename, 'r')
                    lines = file.readlines()
                    lines_use = lines[:count]
                    result_temp = self.multi_proportion(result_temp, lines_use)

            result_set += result_temp
            result_set = sorted(result_set, key=lambda x: x[3], reverse=True)
        return result_set
        pass

    def parse_value(self, item, personal_info):
        ana = PasswordAnalyse()
        name_value = INFO.get(item[0])
        value = personal_info.get(name_value)

        if item[0] == 'N':
            result_set = ana.process_name(value)
        elif item[0] == 'B':
            result_set = ana.process_birthday(value)
        elif item[0] == 'E':
            result_set = ana.process_email(value)
        elif item[0] == 'A':
            result_set = ana.process_account(value)
        elif item[0] == 'I':
            result_set = ana.process_idcard(value)

        result = result_set[int(item[1]) - 1]
        return result

    def save_result(self, generate_result, path='result/'):
        file = open(path + 'generate_result.txt', 'a')
        for item in generate_result:
            file.write('\t'.join([item[0], item[1]]) + '\n')
        file.close()

    def show_result(self, generate_result):
        for item in generate_result:
            print('\t'.join([item[0], item[1]]))


if __name__ == '__main__':
    path = 'result/'
    pattern_file = open('result/pattern.txt', 'r')
    pattern_set = pattern_file.readlines()
    gen = GeneratePassword(path, pattern_set)
    # result = gen.generate_no_info()
    per_info = {
        'name': '卫忠杰',
        'birthday': '19871026',
        'account_name': 'wzj871126',
        'id_card': '210602198711260513',
        'email': 'weizhongjie55@163.com'
    }
    result = gen.generate_info(per_info, count=20)
    gen.show_result(result)
    gen.save_result(result)
