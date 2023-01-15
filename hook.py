import pygame
from boat import Boat
from fishing_line import FishLine


class Hook:
    __DROP_SPEED = 4
    __GET_BACK_SPEED = 8
    __CAUGHT_FISH_SPEED = 2

    def __init__(self, boat: Boat):
        self.picture = pygame.image.load("images/hook.png")
        self.picture = pygame.transform.scale(self.picture, (15, 30))
        self.y_pos = boat.y + 160
        self.is_hook_moving = False
        self.bottom_reached = False
        self.is_caught = False

    def drop_hook(self):
        self.y_pos += Hook.__DROP_SPEED
        if self.y_pos >= 900:
            self.bottom_reached = True
            self.is_caught = False
    def get_hook_back(self, fishing_line: FishLine):
        if self.y_pos >= fishing_line.advance_line + 60:
            self.y_pos -= Hook.__GET_BACK_SPEED
        else:
            self.is_hook_moving = False
            self.bottom_reached = False

    def caught_fish(self, fishing_line: FishLine):
        if self.y_pos >= fishing_line.advance_line + 60:
            self.y_pos -= Hook.__CAUGHT_FISH_SPEED
        else:
            self.is_hook_moving = False
            self.bottom_reached = False
            self.is_caught = True

    def fix_bug_fishing_every_second_time(self):
        if self.y_pos < 210:
            self.is_caught = False
