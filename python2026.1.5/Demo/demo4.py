class MyException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


try:
    raise MyException('test异常')
except MyException as e:
    print(e)
