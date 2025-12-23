while True:
    price = float(input("请输入商品价格："))
    weight = float(input("请输入商品重量："))
    if weight == 0:
        break
    print(price *  weight)

print("结束")