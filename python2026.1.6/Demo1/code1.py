# # l = list()
#
# #
# # items5 = [35, 12, 99, 45, 66]
# # items6 = [45, 58, 29]
# # print(items5 + items6)
# # items8 = ['apple', 'waxberry', 'pitaya', 'peach', 'watermelon']
# #
# # print(items8[-1::-1])
# #
# # print(items6*2)
# #
# # print(items8[::])
# #
# # for item in items8:
# #     print(item)
#
# class Student(object):
#     number = 0
#
#     def __init__(self, name, score):
#         self.name = name
#         self.__score = score
#
#     # def a(self):
#     #     return self.__score
#
#     # def b(self,score):
#     #     self.__score =  score
#     @property
#     def score(self):
#         return self.__score
#
#     @score.setter
#     def score(self, score: int):
#         if 0 <= score <= 100:
#             self.__score = score
#         else:
#             raise ValueError('bad score')
#
#
#
# #
# # s = Student('Bob', 90)
# # s.score = "60"
# #
# # print(s.score)
# def sum(a: int, b: int):
#     return a + b
#
#
# print(sum("a", "2"))
#

# number = input("请输入：")


class Student:
    number = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def add_number(cls):
        cls.number += 1


Student.add_number()
Student.add_number()
Student.add_number()
Student.add_number()
print(Student.number)
