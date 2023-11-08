import pygame
from utils import flip_image, LEVELS, level_up

class Boat:
    LEVEL = 0
    __MOVE_SPEED = 3
    __BOAT_WIDTH = 250
    __BOAT_HEIGHT = 130

    def __init__(self, x=700, y=50):
        self.x = x
        self.y = y
        self.caught_fishes = 0

    @staticmethod
    def load_boat():
        boat_right = pygame.image.load("images/boat_right.png")
        boat_right = pygame.transform.scale(boat_right, (Boat.__BOAT_WIDTH, Boat.__BOAT_HEIGHT))

        boat_left = flip_image(boat_right)
        boat_left = pygame.transform.scale(boat_left, (Boat.__BOAT_WIDTH, Boat.__BOAT_HEIGHT))
        return boat_left, boat_right

    def move_left(self):
        if self.x > 0:
            self.x -= Boat.__MOVE_SPEED

    def move_right(self, screen_width: int):
        if self.x < screen_width - Boat.__BOAT_WIDTH:
            self.x += Boat.__MOVE_SPEED

    def caught_fish(self):
        self.caught_fishes += 1
        level_up(Boat.LEVEL, self.caught_fishes)

