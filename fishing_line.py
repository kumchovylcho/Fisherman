from boat import Boat


class FishLine:

    def __init__(self, boat: Boat):
        self.tip_of_the_rod = boat.x + 35   # default
        self.advance_line = 150

    def rotate_fisherman_right(self, boat: Boat):
        self.tip_of_the_rod = boat.x + 210

    def rotate_fisherman_left(self, boat: Boat):
        self.tip_of_the_rod = boat.x + 35
