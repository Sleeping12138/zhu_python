import csv

#
# with open('../files/test2.csv', 'w',encoding='utf-8') as file:
#     w = csv.writer(file)


# with open('../resource/example1.csv', 'r',encoding='utf-8') as file:
#     r = csv.reader(file)
#     ret = list(r)
#     print(ret)

data = [['name', 'zjy'], ['age', '18']]

with open('../resource/tmp_2.csv', 'w', encoding='utf-8',newline='') as file:
    w = csv.writer(file,delimiter='\t')
    w.writerows(data)
