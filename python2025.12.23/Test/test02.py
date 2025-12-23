num = float(input("请输入一个数："))

if num > 100:
    print(f"{num} 大于 100")
else:
    print(f"{num} 不大于 100")

if num < 0:
    print(f"{num} 小于 0")
else:
    print(f"{num} 不小于 0")

if 80 <= num <= 100:
    print(f"{num} 在 80~100 之间")
else:
    print(f"{num} 不在 80~100 之间")

