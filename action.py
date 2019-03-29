from step import Step


class Action:
    def __init__(self, name, direction, amount):
        self.step = Step(name, direction, amount)
        self.weight = 0
        self.usage_depth = []
