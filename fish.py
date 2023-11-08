import pygame
from utils import flip_image, LEVELS

class Fish:
    __SWIM_SPEED = 2
    __FISH_FLOAT_SPEED = 1

    def __init__(self, x_pos: int or float, y_pos: int or float, level, fish_width, fish_height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.level = level
        self.fish_width = fish_width
        self.fish_height = fish_height

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

    def load_pictures(self, level):
        right_direction = pygame.image.load(f"images/Fish_types/{LEVELS[level][1]}.png")
        left_direction = flip_image(right_direction)
        return pygame.transform.scale(left_direction, (self.fish_width, self.fish_height)), \
            pygame.transform.scale(right_direction, (self.fish_width, self.fish_height))

    def swim_left(self, seconds_passed: int, fish_rect):
        self.x_pos -= Fish.__SWIM_SPEED
        fish_rect.x -= Fish.__SWIM_SPEED
        if seconds_passed % 2 == 0:
            self.y_pos -= Fish.__FISH_FLOAT_SPEED
            fish_rect.y -= Fish.__FISH_FLOAT_SPEED
        else:
            self.y_pos += Fish.__FISH_FLOAT_SPEED
            fish_rect.y += Fish.__FISH_FLOAT_SPEED

    def swim_right(self, seconds_passed: int, fish_rect):
        self.x_pos += Fish.__SWIM_SPEED
        fish_rect.x += Fish.__SWIM_SPEED
        if seconds_passed % 2 == 0:
            self.y_pos -= Fish.__FISH_FLOAT_SPEED
            fish_rect.y -= Fish.__FISH_FLOAT_SPEED
        else:
            self.y_pos += Fish.__FISH_FLOAT_SPEED
            fish_rect.y += Fish.__FISH_FLOAT_SPEED

    def check_left_wall(self):
        return True if self.x_pos < 0 else False

    def check_right_wall(self, screen_width: int):
        return True if self.x_pos > screen_width - self.fish_width else False

    @staticmethod
    def increase_speed_fish_after_caught():
        Fish.__SWIM_SPEED += 1
