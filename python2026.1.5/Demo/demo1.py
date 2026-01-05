# class People:
#     def __init__(self, name, age, sex):
#         self.name = name
#         self.age = age
#         self.sex = sex
#
#     def speak(self, message):
#         print(message + "----")
#
#
# class Student(People):
#     def __init__(self, name, age, sex, grade):
#         super().__init__(name, age, sex)
#         self.grade = grade
#
#     def speak(self, message, str):
#         super().speak(message)
#         print(str)
#
#     def __str__(self):
#         return f"name: {self.name}, age: {self.age}, sex: {self.sex}, grade: {self.grade}"
#
#
# stu = Student('John', 18, 'Male', '1st')
# print(stu)
# stu.speak("hello", "world")
#
#
# class A:
#     sum_num = 0
#
#     def __init__(self, number):
#         self.number = number
#
#
# a = A(1)
# b = A(2)
# c = A(3)
#
# print(a.sum_num)
# a.sum_num += 1
# print(b.sum_num)
# print(c.sum_num)


