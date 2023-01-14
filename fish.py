import pygame


class Fish:
    __SWIM_SPEED = 2
    __FISH_WIDTH = 120
    __FISH_HEIGHT = 80
    __FISH_FLOAT_SPEED = 0.4

    def __init__(self, x_pos: int or float, y_pos: int or float):
        self.x_pos = x_pos
        self.y_pos = y_pos

    @property
    def x_pos(self):
        return self.__x_pos

    @x_pos.setter
    def x_pos(self, value):
        if isinstance(value, (int, float)):
            self.__x_pos = value
        else:
            raise ValueError("You must enter integer or a float value for the WIDTH.")

    @property
    def y_pos(self):
        return self.__y_pos

    @y_pos.setter
    def y_pos(self, value):
        if isinstance(value, (int, float)):
            self.__y_pos = value
        else:
            raise ValueError("You must enter integer or a float value for the HEIGHT")

    @staticmethod
    def load_pictures():
        left_direction = pygame.image.load("images/fish_1_left.png")
        right_direction = pygame.image.load("images/fish_1_right.png")
        return pygame.transform.scale(left_direction, (Fish.__FISH_WIDTH, Fish.__FISH_HEIGHT)), \
               pygame.transform.scale(right_direction, (Fish.__FISH_WIDTH, Fish.__FISH_HEIGHT))

    def swim_left(self, seconds_passed: int):
        self.x_pos -= Fish.__SWIM_SPEED
        if seconds_passed % 2 == 0:
            self.y_pos -= Fish.__FISH_FLOAT_SPEED
        else:
            self.y_pos += Fish.__FISH_FLOAT_SPEED

    def swim_right(self, seconds_passed: int):
        self.x_pos += Fish.__SWIM_SPEED
        if seconds_passed % 2 == 0:
            self.y_pos -= Fish.__FISH_FLOAT_SPEED
        else:
            self.y_pos += Fish.__FISH_FLOAT_SPEED

    def check_left_wall(self):
        return True if self.x_pos < 0 else False

    def check_right_wall(self, screen_width: int):
        return True if self.x_pos > screen_width - Fish.__FISH_WIDTH else False
