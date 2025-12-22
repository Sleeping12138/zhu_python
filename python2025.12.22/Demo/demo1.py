# number = int(input("Enter a number: "))
# print(number)


# number = int(input("Enter a number: "))
# print(number, 12, True, sep="*", end="@@@")
#
# temp = 100
# print(type(temp))

# price = 3.5
# weight = 10
# print(price * weight)
# input()


# price = float(input("Enter price: "))
# weight = float(input("Enter weight: "))
# sum = price * weight
# print(sum)
#
#
# print("购买了" + str(weight) + "斤苹果，每斤" + str(price) + "元，总价花费了" + str(sum) + "元")
# print("购买了%d斤苹果，每斤%.2f元，总价花费了%.2f元" % (weight, price, sum))
# print(f"购买了{weight}斤苹果，每斤{price:.2f}元，总价花费了{sum:.2f}元")
#
# number = int(input("Enter a number: "))
# price = float(input("Enter price: "))
# sum = number * price
#
# print("个数为%d,单价为%.2f,总价为%.2f" % (number, price, sum))

# stu_name = input("请输入学生姓名：")
# math = int(input("请输入学生数学成绩："))
# chinese = int(input("请输入学生语文"))
# english = int(input("请输入学生英语"))
#
# sum = math + chinese + english
# avg = sum / 3
#
# print(f"学生{stu_name}的数学成绩是{math},语文成绩是{chinese},英语成绩是{english},总分是{sum},平均分是{avg:.2f}")
# print("学生%s的数学成绩是%d,语文成绩是%d,英语成绩是%d,总分是%d,平均分是%.2f" % (stu_name, math, chinese, english, sum, avg))
# print("学生{}的数学成绩是{:.2f},语文成绩是{:.2f},英语成绩是{:.2f},总分是{:.2f},平均分是{:.2f}".format(stu_name, math, chinese, english, sum, avg))


# number = int(input("请输入一个整数："))
# if number % 2 == 0:
#     print("偶数")
# else:
#     print("奇数")

# user_name = input("请输入用户名：")
# password = input("请输入密码：")
# if user_name == "admin" and password == "123456":
#     print("登录成功")
# else:
#     print("用户名或密码错误")
score = input("请输入分数：").strip()
if score.isdigit():
    score = int(score)
    if score > 100 or score < 0:
        print("输入的分数有误")
    elif score >= 90:
        print("优秀")
    elif score >= 80:
        print("良好")
    elif score >= 60:
        print("及格")
    else:
        print("不及格")
else:
    print("输入的分数格式错误")


