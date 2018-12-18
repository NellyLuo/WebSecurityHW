# coding:utf-8

data_key = open('data/count_keylist.txt', 'r')

key_list = []
for line in data_key.readlines():
    key = line.strip('\t').strip('\n').split(':')
    key_list.append(key[0])

result_file = open('data/keylist.txt', 'w')
for i in key_list:
    result_file.write(i + '\n')

data_key.close()
result_file.close()
