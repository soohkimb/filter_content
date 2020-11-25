import pandas as pd
import csv
import codecs


# 전체 게시글 추가
dataset = []
contents = []
f = open('output.csv', 'r', encoding='utf-8')
rdf = csv.reader(f)
for line in rdf:
    contents.append(line[0] + ' ' + line[1])
f.close()
del contents[0]

# 전체 필터 추가
filters = []
pos = codecs.open("filter.txt", 'rb', encoding='UTF-8')
while True:
    line = pos.readline()
    line = line.replace('\n', '').replace('\r', '')
    filters.append(line)
    if not line:
        break
pos.close()
del filters[-1]

# 전체 게시글에서 필터링된 column 추가
for post in contents:
    flag = False
    for filt in filters:
        if filt in post:
            flag = True
            break
    if flag:
        dataset.append({
            "flag": 1,
            "content": post
        })
    else:
        dataset.append({
            "flag": 0,
            "content": post
        })
df = pd.DataFrame(dataset)
df.to_csv('./dataset.csv', sep=',', na_rep='NaN', encoding='utf=8')



