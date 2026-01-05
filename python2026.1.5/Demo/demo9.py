class Bicycle:
    def __init__(self, km):
        self.km = km

    def run(self):
        print(self.km)


class EBicycle(Bicycle):
    def __init__(self, km, volume):
        super().__init__(km)
        self.volume = volume

    def fill_charge(self, vol):
        self.volume += vol

    def run(self, km):
        del_vol = km / 10
        self.volume -= del_vol
        print(self.volume)
        if (self.volume <= 0):
            super().run()
