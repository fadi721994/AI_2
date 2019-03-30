from step import Step


class Action:
    def __init__(self, car, direction, amount):
        self.car = car
        self.step = Step(car.name, direction, amount)
        self.weight = 0
