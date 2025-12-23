distance = float(input("请输入公里数："))

if distance <= 3:
    cost = 13
elif distance <= 15:
    cost = 13 + (distance - 3) * 2.3
else:
    cost = 13 + 12 * 2.3 + (distance - 15) * 3.45

cost = round(cost)

print(f"费用金额：{cost} 元")

