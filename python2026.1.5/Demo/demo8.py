class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def teach(self, other, skill):
        print(f"{self.name} 交 {other.name} 学 {skill}")

    def works(self, amount):
        print(f"{self.name} 上班赚了 {amount}元")

    def borrow(self, other, amount):
        print(f"{self.name} 向 {other.name} 借了 {amount}元")

    def __str__(self):
        print(f"{self.age}岁的 {self.name}")


if __name__ == "__main__":
    zhangsan = Human("张三", 35)
    lisi = Human("李四", 8)
    zhangsan.teach(lisi, "python")
    lisi.teach(zhangsan, "跳皮筋")
    zhangsan.works(1000)
    lisi.borrow(zhangsan, 200)
    print(zhangsan)
    print(lisi)
