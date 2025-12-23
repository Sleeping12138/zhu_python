month = int(input("请输入月份（1~12）："))

if month >= 1 and month <= 3:
    print(f"{month}月在第一季度")
elif month >= 4 and month <= 6:
    print(f"{month}月在第二季度")
elif month >= 7 and month <= 9:
    print(f"{month}月在第三季度")
elif month >= 10 and month <= 12:
    print(f"{month}月在第四季度")
else:
    print("您输错了，请输入1~12的整数")

