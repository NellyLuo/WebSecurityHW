# coding:utf-8


data_pinyin = open('data/count_pinyin.txt', 'r')
data_word = open('data/count_word.txt', 'r')

pinyin_list, word_list = [], []

for line in data_pinyin.readlines():
    pinyin_list.append(line.split(',')[0])

for line in data_word.readlines():
    word_list.append(line.split(',')[0])

print(word_list)
print(pinyin_list)

pinyin_list = set(pinyin_list)
word_list = set(word_list)

result_list = pinyin_list | word_list

result_file = open('data/wordlist.txt', 'w')
for i in result_list:
    result_file.write(i + '\n')

data_pinyin.close()
data_word.close()
result_file.close()
