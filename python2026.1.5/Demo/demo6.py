# class Student:
#     def __init__(self, name, age, sex, grade):
#         # 受保护变量
#         self._name = name
#         self._age = age
#         self._sex = sex
#         self._grade = grade
#
#     def __str__(self):
#         return 'Student(name={}, age={}, sex={}, grade={})'.format(self._name, self._age, self._sex, self._grade)
#
#     @staticmethod
#     def return_info():
#         return 'Student(name={}, age={}, sex={}, grade={})'
#
#
# print(Student.return_info())


# class People:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#
# class Student(People):
#     grade = 'grade1'
#
#     def __init__(self, name, age):
#         super().__init__(name, age)
#
#     def __str__(self):
#         return 'Student(name={}, age={})'.format(self.name, self.age)
#
#     @classmethod
#     def get_grade(cls):
#         return cls.grade
#
#
# stu = Student('zhangsan', 18)
# print(Student.get_grade())


# class People:
#     def __init__(self, name='zhangsan', age=19):
#         self.name = name
#         self.age = age
#
#
# p = People('zhangsan', 20)
# print(isinstance(p, People))


class MyException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


try:
    raise MyException('test')
except MyException as e:
    print(e)
else:
    print("no error")
finally:
    print("over")
