class Rod:
    def __init__(self, length, head_position_x, head_position_y, angle=-100):
        self.length = length
        self.initial_values = {
            "head_position_x": head_position_x,
            "head_position_y": head_position_y,
            "angle": angle
        }

        self.head_position_x = head_position_x
        self.head_position_y = head_position_y
        self.angle = angle

    def rotate(self, angle):
        self.angle += angle

    def move(self, x, y):
        self.head_position_x += x
        self.head_position_y += y

    def reset_position(self):
        self.head_position_x = self.initial_values["head_position_x"]
        self.head_position_y = self.initial_values["head_position_y"]
        self.angle = self.initial_values["angle"]
