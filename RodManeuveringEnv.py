import gym
import pygame
from gym import spaces
from Rod import Rod
import math


class RodManeuveringEnv(gym.Env):
    def __init__(self, env_width=450, env_height=450, rod_length=135, start_x=69, start_y=371):
        pygame.init()

        self.env_width = env_width
        self.env_height = env_height
        self.screen = pygame.display.set_mode((self.env_width, self.env_height))

        self.action_space = spaces.Discrete(4)
        self.rod = Rod(rod_length, start_x, start_y)
        self.reset()

    def step(self, action):
        """
        action == 0 -> up
        action == 1 -> down
        action == 2 -> +10 degree
        action == 3 -> -10 degree
        """
        assert self.action_space.contains(action)

        if action == 0:
            angle_x = math.cos(math.radians(self.rod.angle))
            angle_y = math.sin(math.radians(self.rod.angle))
            if not self._check_collision(self.rod.head_position_x + angle_x, self.rod.head_position_y + angle_y,
                                         self.rod.head_position_x + math.cos(
                                             math.radians(self.rod.angle)) * self.rod.length,
                                         self.rod.head_position_y + math.sin(
                                             math.radians(self.rod.angle)) * self.rod.length):
                self.rod.head_position_x += angle_x
                self.rod.head_position_y += angle_y

        elif action == 1:
            angle_x = math.cos(math.radians(self.rod.angle))
            angle_y = math.sin(math.radians(self.rod.angle))
            if not self._check_collision(self.rod.head_position_x - angle_x, self.rod.head_position_y - angle_y,
                                         self.rod.head_position_x + math.cos(
                                             math.radians(self.rod.angle)) * self.rod.length,
                                         self.rod.head_position_y + math.sin(
                                             math.radians(self.rod.angle)) * self.rod.length):
                self.rod.head_position_x -= angle_x
                self.rod.head_position_y -= angle_y
        elif action == 2:
            if not self._check_collision(self.rod.head_position_x, self.rod.head_position_y,
                                         self.rod.head_position_x + math.cos(
                                             math.radians(self.rod.angle + 1)) * self.rod.length,
                                         self.rod.head_position_y + math.sin(
                                             math.radians(self.rod.angle + 1)) * self.rod.length):
                self.rod.angle += 1
        elif action == 3:
            if not self._check_collision(self.rod.head_position_x, self.rod.head_position_y,
                                         self.rod.head_position_x + math.cos(
                                             math.radians(self.rod.angle - 1)) * self.rod.length,
                                         self.rod.head_position_y + math.sin(
                                             math.radians(self.rod.angle - 1)) * self.rod.length):
                self.rod.angle -= 1

        end_x = self.rod.head_position_x + math.cos(math.radians(self.rod.angle)) * self.rod.length
        end_y = self.rod.head_position_y + math.sin(math.radians(self.rod.angle)) * self.rod.length

        self.screen.fill((225, 225, 225))
        pygame.draw.line(self.screen, (255, 0, 0), (self.rod.head_position_x, self.rod.head_position_y), (end_x, end_y))
        pygame.draw.polygon(self.screen, (128, 128, 128), [(72, 63), (89, 115), (128, 78), (112, 25)])
        pygame.draw.polygon(self.screen, (128, 128, 128), [(42, 136), (111, 151), (168, 191), (97, 175)])
        pygame.draw.polygon(self.screen, (128, 128, 128), [(217, 75), (235, 122), (285, 131), (267, 84)])
        pygame.draw.polygon(self.screen, (128, 128, 128), [(365, 11), (386, 58), (437, 80), (415, 35)])
        pygame.draw.polygon(self.screen, (128, 128, 128), [(353, 202), (325, 110), (310, 203), (336, 291)])
        pygame.draw.polygon(self.screen, (128, 128, 128), [(98, 209), (178, 270), (171, 364), (91, 310)])
        pygame.draw.polygon(self.screen, (128, 128, 128), [(307, 323), (340, 351), (342, 394), (311, 365)])
        pygame.draw.polygon(self.screen, (128, 128, 128), [(336, 407), (379, 377), (430, 391), (385, 420)])

        pygame.display.update()

    def _check_collision(self, start_x, start_y, end_x, end_y):
        if start_x < 0 or start_x > self.env_width or \
                start_y > self.env_height or start_y < 0 or \
                end_x > self.env_width or end_x < 0 or \
                end_y > self.env_height or end_y < 0:
            self.reset()
            return True
        else:
            return False

    def reset(self):
        self.rod.reset_position()

    def render(self, mode='human'):
        pass
