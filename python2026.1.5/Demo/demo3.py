# try:
#     num1 = int(input("请输入第一个数字："))
#     num2 = int(input("请输入第二个数字："))
#
#     op1 = input("请输入运算符：")
#     if op1 not in ["+", "-", "*", "/"]:
#         print("输入运算符号错误")
#         exit()
#     if op1 == "+":
#         print(num1 + num2)
#     elif op1 == "-":
#         print(num1 - num2)
#     elif op1 == "*":
#         print(num1 * num2)
#     elif op1 == "/":
#         print(num1 / num2)
#
# except ValueError as e:
#     print("num1或num2输入错误", e)
# except ZeroDivisionError as e:
#     print("除数不能为0", e)



try:
    num1 = int(input("请输入第一个数字："))
    num2 = int(input("请输入第二个数字："))
except ValueError as e:
    print("num1或num2输入错误", e)
else:
    print("num1和num2没有明显错误")
finally:
    print("程序结束")

