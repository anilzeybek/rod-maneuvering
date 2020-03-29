import math


def line_line_collision(x1, y1, x2, y2, x3, y3, x4, y4):
    uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
    uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
    if 0 <= uA <= 1 and 0 <= uB <= 1:
        return True
    else:
        return False


def line_polygon_collision(rod, polygon):
    rod_end_x = rod.head_position_x + math.cos(math.radians(rod.angle)) * rod.length
    rod_end_y = rod.head_position_y + math.sin(math.radians(rod.angle)) * rod.length

    left = line_line_collision(rod.head_position_x, rod.head_position_y, rod_end_x, rod_end_y, polygon.x1, polygon.y1,
                               polygon.x2, polygon.y2)
    right = line_line_collision(rod.head_position_x, rod.head_position_y, rod_end_x, rod_end_y, polygon.x2, polygon.y2,
                                polygon.x3, polygon.y3)
    top = line_line_collision(rod.head_position_x, rod.head_position_y, rod_end_x, rod_end_y, polygon.x3, polygon.y3,
                              polygon.x4, polygon.y4)
    bottom = line_line_collision(rod.head_position_x, rod.head_position_y, rod_end_x, rod_end_y, polygon.x1, polygon.y1,
                                 polygon.x4, polygon.y4)

    if left or right or top or bottom:
        return True
    else:
        return False
