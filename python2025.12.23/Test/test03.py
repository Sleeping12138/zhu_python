quarter = int(input("请输入季度（1~4）："))

if quarter == 1:
    print("第一季度包含：1月、2月、3月")
elif quarter == 2:
    print("第二季度包含：4月、5月、6月")
elif quarter == 3:
    print("第三季度包含：7月、8月、9月")
elif quarter == 4:
    print("第四季度包含：10月、11月、12月")
else:
    print("您输错了，请输入1~4的整数")

