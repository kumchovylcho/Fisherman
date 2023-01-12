import pygame


class Boat:
    move_speed = 3

    def __init__(self, x=700, y=100):
        self.x = x
        self.y = y

    @staticmethod
    def load_boat():
        boat_left = pygame.image.load("images/boat_left.png")
        boat_right = pygame.image.load("images/boat_right.png")
        return boat_left, boat_right

    def move_left(self):
        self.x -= Boat.move_speed

    def move_right(self):
        self.x += Boat.move_speed
