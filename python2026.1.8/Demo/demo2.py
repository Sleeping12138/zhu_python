# import csv
#
# with open('../files/test1.csv','r',encoding='utf-8') as file:
#     reader = csv.reader(file)
#     ret = list(reader)
#     for item in ret:
#         print(item)

# with open('../files/test2.csv','r',encoding='utf-8') as file:

import json

# data = {
#     "total": 1,
#     "data": [
#         {
#             "id": 1953,
#             "name": "江南一点雨",
#             "gender": "男",
#             "birthday": "2021-12-01",
#             "idCard": "111111198811111111",
#             "wedlock": "未婚",
#             "nationId": 1,
#             "nativePlace": "test",
#             "politicId": 13,
#             "email": "2@2.com",
#             "phone": "test",
#             "address": "test",
#             "departmentId": 89,
#             "jobLevelId": 9,
#             "posId": 29,
#             "engageForm": "劳动合同",
#             "tiptopDegree": "本科",
#             "specialty": "test",
#             "school": "test",
#             "beginDate": "2021-12-01",
#             "workState": "在职",
#             "workID": "00000067",
#             "contractTerm": 0.0,
#             "conversionTime": "2021-12-01",
#             "notWorkDate": None,
#             "beginContract": "2021-12-01",
#             "endContract": "2021-12-01",
#             "workAge": None,
#             "nation": {
#                 "id": 1,
#                 "name": "汉族"
#             },
#             "politicsstatus": {
#                 "id": 13,
#                 "name": "普通公民"
#             },
#             "department": {
#                 "id": 89,
#                 "name": "莲湖区市场",
#                 "parentId": None,
#                 "depPath": None,
#                 "enabled": None,
#                 "children": [],
#                 "result": None,
#                 "parent": None
#             },
#             "jobLevel": {
#                 "id": 9,
#                 "name": "教授",
#                 "titleLevel": None,
#                 "createDate": None,
#                 "enabled": None
#             },
#             "position": {
#                 "id": 29,
#                 "name": "技术总监",
#                 "createDate": None,
#                 "enabled": None
#             },
#             "salary": None
#         }
#     ]
# }
# with open('../files/tmp10.txt', 'w', encoding='utf-8') as file:
#     json.dump(data, file, ensure_ascii=False)


# with open('../resource/学生信息.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)
# print(data)

#
# with open('../files/tmp10.txt', 'r', encoding='utf-8') as file:
#     data = json.load(file)
#
# print(data)
# print(data['data'][0])
# temp = data['data'][0]
# temp['nation']['name'] = '回族'
# data['data'][0] = temp
#
# with open('../files/test.json', 'w', encoding='utf-8') as file:
#     json.dump(data, file, ensure_ascii=False)


