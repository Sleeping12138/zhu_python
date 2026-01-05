class Teacher:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name


t = Teacher('zhangsan')
print(t.get_name())


class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(self.name + "吃吃吃")


class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)

    def eat(self):
        print(self.name + "吃吃吃")


d = Dog('bb')
print(isinstance(d, Dog))
