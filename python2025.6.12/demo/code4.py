# my_list = [1, 2, 3, 4, 5]
# print(my_list[100])

# try:
#     a = 10
#     b = 0
#     c = a / b
# except ZeroDivisionError as e:
#     print(f"除数为0异常,{e}")
# except Exception as e:
#     print(f"未知异常,{e}")
# else:
#     print("没有异常发生")
# finally:
#     print("finally")

# class Student(object):
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     @property
#     def get_name(self):
#         return self.name
#
#     @get_name.setter
#     def get_name(self, name):
#         self.name = name

# def get_name(self):
#     return self.name
#
# def get_age(self):
#     return self

# try:
#     a = 10
#     b = 0
#     c = a/b
# except (ZeroDivisionError, TypeError) as e:
#     print(f"{e}")

# class AgeError(Exception):
#     def __init__(self, message):
#         self.message = message
#
#     def __str__(self):
#         return self.message
#
#
# while True:
#     try:
#         age = int(input("请输入您的年龄:"))
#         if not (0 <= age <= 100):
#             raise AgeError("您输入的年龄有误！！！")
#         break
#     except ValueError:
#         print("输入的不是整数")
#     except AgeError as e:
#         print(f"{e}")

#
# class SexError(Exception):
#     def __init__(self, msg):
#         self.msg = msg
#
#     def __str__(self):
#         return self.msg
#

# file = open('./test.txt', 'w', encoding='utf-8')
# file.write('hello world')

#
# file = open('./test2.txt','r',encoding='utf-8')
# print(file.read())