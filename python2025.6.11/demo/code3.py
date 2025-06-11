# class Student(object):
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#
# stu = Student(name='zhangsan', age=18)
# print(isinstance(stu, Student))
# print(stu.__dict__)


class Student(object):
    numbers = 0

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    @classmethod
    def get_number(cls):
        return cls.numbers


stu = Student('zhangsan', 18)
print(stu.get_name())
print(stu.get_age())
print(stu.get_number())
print(stu.__dict__)