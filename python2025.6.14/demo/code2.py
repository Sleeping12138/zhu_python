# class File(object):
#     def __init__(self,file_name,file_model):
#         self.file_name = file_name
#         self.file_model = file_model
#
#     # 用于在with语句中将返回值给对象的
#     def __enter__(self):
#         print("enter")
#         self.file = open(self.file_name,self.file_model)
#         return self.file
#
#     # with语句中结束时触发的函数
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print("exit")
#         self.file.close()
#
# with File("test.txt","w") as f:
#     f.write("hello world")
#
# my_list = [x for x in range(10)]
# print(my_list)

# mylist = [x for x in range(10) if x % 2 == 0]
# print(mylist)

# data = (x for x in range(10))
# # print(next(data))
#
# for i in data:
#     print(i)

# def generator(n):
#     for i in range(n):
#         print('begin')
#         yield i
#         print('end')
#
# g = generator(10)
# print(next(g))
# for i in g:
#     print(i)

# data = (x for x in range(100))
# for i in data:
#     print(i)

# data = (x for x in 'abcdefghijklmnop')
# print(next(data))
# print(next(data))
# print(next(data))
# print(next(data))

# def generator(n):
#     for i in range(n):
#         yield i
#
# g = generator(10)
# for i in g:
#     print(i)

# 三目运算符
# a = 10
# b = 20
# num = a if a>b else b
# print(num)

# s = input("please input")
# ret = 'yes' if s == "hello" else 'no'
# print(ret)
#
# s1='hello'
# s2 = 'hello'
# print(s1 is s2)

# a = 10
# b = 20
# a, b = b, a
# print(a, b, sep=',', end='')

# import copy
#
# my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# # print(id(my_list))
# ret = copy.copy(my_list)
# print(id(my_list))
# print(id(ret))