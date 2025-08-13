# class Student():
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def study(self):
#         print(f"{self.name} is studying")
#
#
# stu = Student('zhangsan',18)
# stu.study()

# class Student():
#     name = 'hello world'
#
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def study(self):
#         print(f"{self.name} is studying")
#
#     @staticmethod
#     def eat():
#         print(f"{Student.name} is eating")
#
#     @classmethod
#     def sleep(cls):
#         print(f"{cls.name} is sleeping")
# #
# #
# # stu = Student('zhangsan', 18)
#
#
# class Student():
#     def __init__(self, name, age):
#         self.__name = name
#         self.__age = age
#
#     def get_name(self):
#         return self.__name
#
#     def get_age(self):
#         return self.__age
#
#     def set_age(self, age):
#         __age = age
#
#     def set_name(self, name):
#         self.__name = name


# class Person():
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def eat(self):
#         print(f"{self.name} is eating")
#
#
# class Student(Person):
#     def __init__(self, name, age, classroom):
#         super().__init__(name, age)
#         self.classroom = classroom
#
#
# stu = Student('zhangsan', 18, 'python')
# stu.eat()

# from abc import ABC, abstractmethod
#
#
# class Animal(ABC):
#     @abstractmethod
#     def eat(self):
#         pass
#
#
# class Dog(Animal):
#     def eat(self):
#         print('dog is eating')
#
#
# class Cat(Animal):
#     def eat(self):
#         print('cat is eating')


# from abc import ABC, abstractmethod
#
#
# class People(ABC):
#     @abstractmethod
#     def eat(self):
#         pass
#
# from Demo.code2 import Color
# print(Color.RED.name)
# print(Color.RED.value)
#
# import json
#
# data = {
#     'name': 'zhangsan',
# }
#
# print(type(json.dumps(data)))
# print(type(json.loads(json.dumps(data))))

# from collections.abc import Iterable
#
# print(isinstance([], Iterable))
# print(isinstance({}, Iterable))

# from collections.abc import Iterable
#
# my_list = [range(11)]
# print(isinstance(iter(my_list), Iterable))


# my_list = list(range(11))
# iterator = iter(my_list)
# while True:
#     try:
#         print(next(iterator))
#     except StopIteration:
#         print('over')
#         break


# my_list = list(range(11))
# iterator = iter(my_list)
# while True:
#     try:
#         print(next(iterator))
#     except StopIteration:
#         break

# class MyIterable():
#     def __init__(self):
#         pass
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         # 编写next逻辑，注意终止条件必须为raise StopIteration，因为后续使用的for的底层是使用异常来进行终止的
#         pass


# class MyIterable():
#     def __init__(self):
#         pass
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         # 编写next逻辑
#         pass


# from collections.abc import Iterator, Iterable
#
# my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# iterator = iter(my_list)
# print(isinstance(my_list, Iterable))  # True
# print(isinstance(my_list, Iterator))  # False
# print(isinstance(iterator, Iterable))  # True
# print(isinstance(iterator, Iterator))  # True

def generator():
    index = 1
    while True:
        number = yield index
        print(number)
        index += 1

        if index == 11:
            return 'over'


g = generator()
print(next(g))
print(g.send(100))

