class Test01():
    def setup_class(self):
        print('setup_class')

    def setup_method(self):
        print('setup_method')

    def test_01(self):
        assert 1 == 1
        print('test_01')

    def test_02(self):
        print('test_02')

    def test_03(self):
        print('test_03')

    def teardown_method(self):
        print('teardown_method')

    def teardown_class(self):
        print('teardown_class')
