# import random
#
# target = random.randint(1, 100)
# num = -1
# while num != target:
#     num = int(input("请输入一个整数:"))
#     if (num > target):
#         print("数猜大了")
#     elif (num < target):
#         print("数猜小了")
#     else:
#         print("恭喜您猜对了!!!")

# i = 1
# while i <= 9:
#     j = 1
#     while j <= i:
#         print(f"{j}*{i}={j * i}\t", end="")
#         j += 1
#     print()
#     i += 1

# str = "hello world"
# for x in str:
#     print(x)

# range的三种方式
# for i in range(0,10,2):
#     print(f"{i} ", end="")

# i = 0
# for i in range(10):
#     print(f"{i} ", end="")
# print(i)
#
# for i in range(1, 10):
#     for j in range(1, i + 1):
#         print(f"{j}*{i}={j * i}\t",end="")
#     print()


# str = "hello world"
# print(len(str))
#

#
# bool = False
# if not bool:
#     print("hhh")

# def length(str):
#     i = 0
#     for j in str:
#         i+=1
#     return i
#
# print(length("hello world"))

# def sum(a, b):
#     return a + b
#
#
# print(sum(1, 2))

# str = None
# print(str)
# print(type(str))

# def sum(a,b):
#     """
#     :param a:
#     :param b:
#     :return:
#     """
#     return a+b
#
# print(sum(1,2))


num = 100
def setNum():
    global num
    num = 200
setNum()
print(num)
