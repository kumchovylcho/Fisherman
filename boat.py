import pygame


class Boat:
    move_speed = 3
    move_horizontal_due_waves = 0.18

    def __init__(self, x=700, y=95):
        self.x = x
        self.y = y

    @staticmethod
    def load_boat():
        boat_left = pygame.image.load("images/boat_left.png")
        boat_right = pygame.image.load("images/boat_right.png")
        return boat_left, boat_right

    def move_left(self, second_passed):
        if self.x > -10:
            self.x -= Boat.move_speed
            if second_passed % 2 == 0:
                self.y -= Boat.move_horizontal_due_waves
            else:
                self.y += Boat.move_horizontal_due_waves

    def move_right(self, second_passed):
        if self.x < 1450:
            self.x += Boat.move_speed
            if second_passed % 2 == 0:
                self.y -= Boat.move_horizontal_due_waves
            else:
                self.y += Boat.move_horizontal_due_waves
