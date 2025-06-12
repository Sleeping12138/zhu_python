# class Student(object):
#     numbers = 0
#
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def get_name(self):
#         return self.name
#
#     @classmethod
#     def get_numbers(cls):
#         return cls.numbers
#
#     @staticmethod
#     def print_info():
#         print("hello world")
#
#
# stu = Student("zhangsan", 18)
# print(stu.get_name())
# print(Student.get_numbers())
# print(Student.print_info())
from abc import ABC, abstractmethod
from typing import Union


# class Student(object):
#
#     def print_set(self, *args):
#         print(args)
#
#     def print_dict(self, **kwargs):
#         print(kwargs)
#
#
# stu = Student()
# my_set = {1, 2, 3, 4, 5}
# my_dict = {'zhangsan': 18, 'lisi': 20}
# stu.print_set(*my_set)
# stu.print_dict(**my_dict)
#
#
# class People(object):
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def say_hello(self):
#         print('hello world')
#
#
# class Student(People):
#     def __init__(self, name, age, score):
#         super().__init__(name, age)
#         self.score = score
#
#     def say_hello(self):
#         print('hello student')
#
#
# stu = Student('zhangsan', 18, 100)
# stu.say_hello()
# print(stu.__dict__)

# class Student(object):
#     def __init__(self, name, age):
#         self.__name = name
#         self.__age = age
#
#     @property
#     def name(self):
#         return self.__name
#
#     @name.setter
#     def name(self, name):
#         self.__name = name
#
#
# stu = Student('zhangsan', 21)
# print(stu.name)
# stu.name = 'lisi'
# print(stu.name)

# class Student(object):
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def __str__(self):
#         return 'Student name: %s, age: %d' % (self.name, self.age)
#
#     def __eq__(self, other):
#         return self.name == other.name and self.age == other.age
#
#
# stu = Student('zhangsan', 18)
# print(stu)

# def fun(a: int, b: int) -> int:
#     return a + b
#
#
# ret = fun(1, 2)
# print(ret)

# def fun(a:int, b:int) -> Union[int, float]:
#     return a + b

# 抽象方法需要继承ABC
# 抽象方法中要有@abstractmethod方法
# class People(ABC):
#
#     @abstractmethod
#     def get_name(self) -> str:
#         pass
#
#
# class Student(People):
#     def __init__(self, name):
#         self.name = name
#
#     def get_name(self) -> str:
#         return self.name

# stu = Student('zhangsan')
# print(stu.get_name())

# class People(object):
#     def hello(self):
#         print('hello people')
#         super().hello()
#
#
# class Human(object):
#     def hello(self):
#         print('hello human')
#
#
# class Student(People, Human):
#     def hello(self):
#         super().hello()
# stu = Student()
# print(stu.hello())
# print(Student.__mro__)