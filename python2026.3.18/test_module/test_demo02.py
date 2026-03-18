class TestDemo02:

    def setup_class(self):
        print("前置类")

    def teardown_class(self):
        print("后置类")

    def setup_method(self):
        print("前置操作")

    def teardown_method(self):
        print("后置操作")

    def test01(self):
        print("001")

    def test02(self):
        print("002")

    def test03(self):
        print("003")