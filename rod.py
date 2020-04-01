import math


class Rod:
    def __init__(self, length, center_x, center_y, angle=100):
        self.length = length
        self.initial_values = {
            "center_x": center_x,
            "center_y": center_y,
            "angle": angle
        }

        self.center_x = center_x
        self.center_y = center_y
        self.angle = angle

    def rotate(self, angle):
        self.angle += angle

    def move(self, x, y):
        self.center_x += x
        self.center_y += y

    def get_positions(self):
        """
        returns x1,y1 x2,y2 of rod
        """
        # end_x = self.rod.head_position_x + math.cos(math.radians(self.rod.angle)) * self.rod.length
        # end_y = self.rod.head_position_y + math.sin(math.radians(self.rod.angle)) * self.rod.length

        x1 = self.center_x - self.length / 2 * math.cos(math.radians(self.angle))
        y1 = self.center_y + self.length / 2 * math.sin(math.radians(self.angle))
        x2 = self.center_x + self.length / 2 * math.cos(math.radians(self.angle))
        y2 = self.center_y - self.length / 2 * math.sin(math.radians(self.angle))

        return x1, y1, x2, y2

    def add_virtual_angle(self, d_angle):
        x1 = self.center_x - self.length / 2 * math.cos(math.radians(self.angle + d_angle))
        y1 = self.center_y + self.length / 2 * math.sin(math.radians(self.angle + d_angle))
        x2 = self.center_x + self.length / 2 * math.cos(math.radians(self.angle + d_angle))
        y2 = self.center_y - self.length / 2 * math.sin(math.radians(self.angle + d_angle))

        return x1, y1, x2, y2

    def add_virtual_x(self, dx):
        x1 = self.center_x + dx - self.length / 2 * math.cos(math.radians(self.angle))
        y1 = self.center_y + self.length / 2 * math.sin(math.radians(self.angle))
        x2 = self.center_x + dx + self.length / 2 * math.cos(math.radians(self.angle))
        y2 = self.center_y - self.length / 2 * math.sin(math.radians(self.angle))

        return x1, y1, x2, y2

    def add_virtual_y(self, dy):
        x1 = self.center_x - self.length / 2 * math.cos(math.radians(self.angle))
        y1 = self.center_y + dy + self.length / 2 * math.sin(math.radians(self.angle))
        x2 = self.center_x + self.length / 2 * math.cos(math.radians(self.angle))
        y2 = self.center_y + dy - self.length / 2 * math.sin(math.radians(self.angle))

        return x1, y1, x2, y2

    def reset_position(self):
        self.center_x = self.initial_values["center_x"]
        self.center_y = self.initial_values["center_y"]
        self.angle = self.initial_values["angle"]

    def is_close_to(self, goal_rod):
        # if abs(self.center_x - goal_rod.center_x) < 10 and abs(
        #         self.center_y - goal_rod.center_y) < 10 and abs(self.angle - goal_rod.angle) <= 30:
        #     print("WIN!!!!")
        #     return True
        if self.center_x == goal_rod.center_x and self.center_y == goal_rod.center_y and self.angle == goal_rod.angle:
            print("WIN!!!!")
            return True
        return False

    def fix_angle(self):
        if self.angle < 0:
            self.angle += 360
        self.angle = self.angle % 360
