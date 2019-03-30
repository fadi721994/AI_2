import utils


class Step:
    def __init__(self, name, direction, amount):
        self.car_name = name
        self.direction = direction
        self.amount = amount

    def print_step(self):
        print("Car " + self.car_name + " Direction " + str(self.direction) + " amount " + str(self.amount))

    def to_string(self):
        return self.car_name + utils.get_direction_initial(self.direction) + str(self.amount)
