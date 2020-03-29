import gym
import pygame
from gym import spaces
from rod import Rod
from polygon import Polygon
import math


class RodManeuveringEnv(gym.Env):
    def __init__(self, n=30, alpha=0.1, gamma=0.97, epsilon=0.1, rod_length=67, start_x=35, start_y=185,
                 goal_x=192, goal_y=39, goal_angle=100):
        pygame.init()

        self.n = n
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.env_width = 225
        self.env_height = 225
        self.screen = pygame.display.set_mode((self.env_width, self.env_height))
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.goal_angle = goal_angle

        self.action_space = spaces.Discrete(4)
        self.rod = Rod(rod_length, start_x, start_y)
        self.reset()

        self.polygons = [Polygon(36, 31, 45, 58, 64, 39, 56, 12),
                         Polygon(21, 68, 55, 75, 84, 95, 48, 87),
                         Polygon(108, 37, 117, 61, 142, 65, 133, 42),
                         Polygon(182, 5, 193, 29, 218, 40, 207, 18),
                         Polygon(176, 101, 162, 55, 155, 101, 168, 145),
                         Polygon(49, 105, 89, 135, 85, 182, 45, 155),
                         Polygon(153, 161, 170, 175, 171, 197, 155, 182),
                         Polygon(168, 203, 189, 188, 215, 195, 192, 210)]

    def step(self, action):
        """
        action == 0 -> up
        action == 1 -> down
        action == 2 -> +10 degree
        action == 3 -> -10 degree
        """
        assert self.action_space.contains(action)

        reward = -10

        if self._check_collision(self.rod.head_position_x, self.rod.head_position_y,
                                 self.rod.head_position_x + math.cos(
                                     math.radians(self.rod.angle)) * self.rod.length,
                                 self.rod.head_position_y + math.sin(
                                     math.radians(self.rod.angle)) * self.rod.length):
            print("--reset--")
            self.reset()
            return self.get_obs(), 0, False, {}

        if action == 0:
            dx = int(round(math.cos(math.radians(self.rod.angle)) * 10))
            dy = int(round(math.sin(math.radians(self.rod.angle)) * 10))
            if not self._check_collision(self.rod.head_position_x + dx, self.rod.head_position_y + dy,
                                         self.rod.head_position_x + dx + math.cos(
                                             math.radians(self.rod.angle)) * self.rod.length,
                                         self.rod.head_position_y + dy + math.sin(
                                             math.radians(self.rod.angle)) * self.rod.length):
                self.rod.head_position_x += dx
                self.rod.head_position_y += dy

        elif action == 1:
            dx = int(round(math.cos(math.radians(self.rod.angle)) * 10))
            dy = int(round(math.sin(math.radians(self.rod.angle)) * 10))
            if not self._check_collision(self.rod.head_position_x - dx, self.rod.head_position_y - dy,
                                         self.rod.head_position_x - dx + math.cos(
                                             math.radians(self.rod.angle)) * self.rod.length,
                                         self.rod.head_position_y - dy + math.sin(
                                             math.radians(self.rod.angle)) * self.rod.length):
                self.rod.head_position_x -= dx
                self.rod.head_position_y -= dy

        elif action == 2:
            if not self._check_collision(self.rod.head_position_x, self.rod.head_position_y,
                                         self.rod.head_position_x + math.cos(
                                             math.radians(self.rod.angle + 10)) * self.rod.length,
                                         self.rod.head_position_y + math.sin(
                                             math.radians(self.rod.angle + 10)) * self.rod.length):
                self.rod.angle += 10

        elif action == 3:
            if not self._check_collision(self.rod.head_position_x, self.rod.head_position_y,
                                         self.rod.head_position_x + math.cos(
                                             math.radians(self.rod.angle - 10)) * self.rod.length,
                                         self.rod.head_position_y + math.sin(
                                             math.radians(self.rod.angle - 10)) * self.rod.length):
                self.rod.angle -= 10

        if self.rod.angle < 0:
            self.rod.angle += 360
        self.rod.angle = self.rod.angle % 360

        end_x = self.rod.head_position_x + math.cos(math.radians(self.rod.angle)) * self.rod.length
        end_y = self.rod.head_position_y + math.sin(math.radians(self.rod.angle)) * self.rod.length

        goal_end_x = self.goal_x + math.cos(math.radians(self.goal_angle)) * self.rod.length
        goal_end_y = self.goal_y + math.sin(math.radians(self.goal_angle)) * self.rod.length

        done = False
        if self._is_rod_close_to_goal():
            done = True
            reward += 1000
            self.reset()

        self.screen.fill((225, 225, 225))
        pygame.draw.rect(self.screen, (255, 0, 0), [self.rod.head_position_x, self.rod.head_position_y, 3, 3])
        pygame.draw.line(self.screen, (255, 0, 0), (self.rod.head_position_x, self.rod.head_position_y), (end_x, end_y))

        pygame.draw.rect(self.screen, (0, 255, 0), [self.goal_x, self.goal_y, 3, 3])
        pygame.draw.line(self.screen, (0, 255, 0), (self.goal_x, self.goal_y), (goal_end_x, goal_end_y))
        for polygon in self.polygons:
            pygame.draw.polygon(self.screen, (128, 128, 128), polygon.get_coordinates())

        pygame.display.update()
        return self.get_obs(), reward, done, {}

    def get_obs(self):
        encrypted_angle = -99999
        angle_list = list(range(0, 360, 10))
        for i in range(len(angle_list)):
            if angle_list[i] == self.rod.angle:
                encrypted_angle = i
                break

        return self.rod.head_position_x, self.rod.head_position_y, encrypted_angle

    def _check_collision(self, start_x, start_y, end_x, end_y):
        if start_x < 0 or start_x > self.env_width or \
                start_y > self.env_height or start_y < 0 or \
                end_x > self.env_width or end_x < 0 or \
                end_y > self.env_height or end_y < 0:
            return True
        else:
            for polygon in self.polygons:
                if polygon.check_collision_with_line(start_x, start_y, end_x, end_y):
                    return True
            return False

    def reset(self):
        self.rod.reset_position()

    def _is_rod_close_to_goal(self):
        if abs(self.rod.head_position_x - self.goal_x) < 10 and abs(
                self.rod.head_position_y - self.goal_y) < 10 and abs(self.rod.angle - self.goal_angle) <= 30:
            print("WIN!!!!")
            return True

        return False

    def render(self, mode='human'):
        pass
