# import pytest
# import yaml
#
#
# def write_yaml(data):
#     with open("./test.yml", "w", encoding="utf-8") as f:
#         # 将数据写入yaml文件
#         yaml.safe_dump(data, f)
#
#
# def read_yaml():
#     with open("./test.yml", "r", encoding="utf-8") as f:
#         # 读取yaml文件
#         return yaml.safe_load(f)
#
#
# def clear_yaml():
#     with open("./test.yml", "w", encoding="utf-8") as f:
#         # 清空yaml文件
#         f.truncate()
#
#
# def test_01():
#     data = {"name": "xiaoming", "age": 18}
#     write_yaml(data)
#
#
# def test_02():
#     data = read_yaml()
#     print(data)
