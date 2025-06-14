# 闭包
# def fun1(fn):
#     def inner(a, b):
#         print("hello world")
#         return fn(a, b)
#
#     return inner
#
#
# def fun2(fn):
#     def inner(a,b):
#         print("hello python")
#         return fn(a,b)
#     return inner
#
# @fun2
# @fun1
# def sum(a, b):
#     return a + b
from abc import ABC, abstractmethod


# print(sum(3, 4))

# def func(flag):
#     def fun(fn):
#         def inner(a, b):
#             if flag == '+':
#                 print("+")
#             else:
#                 print("-")
#             return fn(a, b)
#
#         return inner
#
#     return fun
#
#
# @func('+')
# def sum(a, b):
#     return a + b
#
#
# print(sum(1, 2))

# class Student(object):
#     def __init__(self, fn):
#         self.__fn = fn
#
#     def __call__(self, *args, **kwargs):
#         print("this is a test")
#         self.__fn()
#
#
# @Student
# def fun():
#     print('hello world')
#
#
# fun()

# class Student(object):
#     def __init__(self,name,age):
#         self.name = name
#         self.age = age
#
#
# stu = Student('zhangsan',18)
# print(stu.__dict__)

# class Animal(ABC):
#     @abstractmethod
#     def eat(self):
#         pass
#
# class Dog(Animal):
#
#     def eat(self):
#         print("dog is eating.")
#
# dog = Dog()
# dog.eat()

# add_lambda = lambda x, y: x + y
# print(add_lambda(1, 2))
#
# my_list = [1,4,2,5,7,3,9,10]
# my_list.sort(reverse=True)
# print(my_list)
#
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
#     def name(self,name):
#         self.__name = name
#
#
# stu = Student('zhangsan', 21)
# print(stu.name)
# stu.name = 'lisi'
# print(stu.name)

# class Student(object):
#     def __init__(self, name, age):
#         self.__name = name
#         self.__age = age
#
#     def get_name(self):
#         return self.__name
#
#     def set_name(self, name):
#         self.__name = name
#
#     name = property(get_name, set_name)
#
#
# stu = Student('John',18)
# print(stu.name)
# stu.name = 'zhagnsan'
# print(stu.name)
