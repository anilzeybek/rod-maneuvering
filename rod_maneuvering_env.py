import gym
import pygame
from gym import spaces
from rod import Rod
from polygon import Polygon


class RodManeuveringEnv(gym.Env):
    def __init__(self, n=30, alpha=0.1, gamma=0.97, epsilon=0.1, rod_length=180, start_x=90, start_y=450,
                 goal_x=510, goal_y=180, goal_angle=260):
        self.n = n
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.env_width = 600
        self.env_height = 600
        self.screen = pygame.display.set_mode((self.env_width, self.env_height))

        self.action_space = spaces.Discrete(6)
        self.rod = Rod(rod_length, start_x, start_y)
        self.goal_rod = Rod(rod_length, goal_x, goal_y, goal_angle)

        self.reset()

        self.polygons = [Polygon(95, 83, 146, 32, 169, 103, 116, 153),
                         Polygon(51, 179, 145, 203, 224, 255, 131, 232),
                         Polygon(129, 280, 120, 412, 227, 488, 236, 360),
                         Polygon(287, 99, 354, 111, 377, 173, 313, 161),
                         Polygon(485, 12, 552, 45, 583, 106, 515, 78),
                         Polygon(433, 145, 469, 270, 447, 394, 413, 273),
                         Polygon(409, 431, 414, 490, 456, 527, 452, 468),
                         Polygon(447, 543, 504, 505, 573, 523, 512, 562)]

    def step(self, action):
        """
        action == 0 -> up
        action == 1 -> down
        action == 2 -> right
        action == 3 -> left
        action == 4 -> +10 degree
        action == 5 -> -10 degree
        """
        assert self.action_space.contains(action)

        reward = -1

        rod_positions = self.rod.get_positions()
        if self._check_collision(rod_positions[0], rod_positions[1], rod_positions[2], rod_positions[3]):
            print("--reset--")
            self.reset()
            return self.get_obs(), 0, False, {}

        if action == 0:
            virtual_positions = self.rod.add_virtual_y(-30)
            if not self._check_collision(virtual_positions[0], virtual_positions[1], virtual_positions[2],
                                         virtual_positions[3]):
                self.rod.center_y -= 30

        elif action == 1:
            virtual_positions = self.rod.add_virtual_y(30)
            if not self._check_collision(virtual_positions[0], virtual_positions[1], virtual_positions[2],
                                         virtual_positions[3]):
                self.rod.center_y += 30

        elif action == 2:
            virtual_positions = self.rod.add_virtual_x(30)
            if not self._check_collision(virtual_positions[0], virtual_positions[1], virtual_positions[2],
                                         virtual_positions[3]):
                self.rod.center_x += 30

        elif action == 3:
            virtual_positions = self.rod.add_virtual_x(-30)
            if not self._check_collision(virtual_positions[0], virtual_positions[1], virtual_positions[2],
                                         virtual_positions[3]):
                self.rod.center_x -= 30

        elif action == 4:
            if not self._check_collision(self.rod.add_virtual_angle(10)[0], self.rod.add_virtual_angle(10)[1],
                                         self.rod.add_virtual_angle(10)[2], self.rod.add_virtual_angle(10)[3]):
                self.rod.angle += 10

        elif action == 5:
            if not self._check_collision(self.rod.add_virtual_angle(-10)[0], self.rod.add_virtual_angle(-10)[1],
                                         self.rod.add_virtual_angle(-10)[2], self.rod.add_virtual_angle(-10)[3]):
                self.rod.angle -= 10

        self.rod.fix_angle()

        done = False
        if self.rod.is_close_to(self.goal_rod):
            done = True
            reward = 100
            self.reset()

        return self.get_obs(), reward, done, {}

    def get_obs(self):
        encrypted_angle = self.rod.angle // 10
        encrypted_x = self.rod.center_x // 30
        encrypted_y = self.rod.center_y // 30

        return encrypted_x, encrypted_y, encrypted_angle

    def _draw_line(self, positions, color):
        pygame.draw.rect(self.screen, color, [positions[0], positions[1], 3, 3])
        pygame.draw.line(self.screen, color, (positions[0], positions[1]), (positions[2], positions[3]))

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

    def render(self, mode='human'):
        rod_positions = self.rod.get_positions()
        goal_positions = self.goal_rod.get_positions()

        self.screen.fill((225, 225, 225))
        self._draw_line(rod_positions, (255, 0, 0))
        self._draw_line(goal_positions, (0, 255, 0))

        for polygon in self.polygons:
            pygame.draw.polygon(self.screen, (128, 128, 128), polygon.get_coordinates())

        pygame.display.update()
