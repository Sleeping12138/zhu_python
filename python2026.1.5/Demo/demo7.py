class Student:
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

    def set_score(self, score):
        self.score = score

    def show_info(self):
        print(f'Student(name={self.name}, age={self.age}, score={self.score})')



