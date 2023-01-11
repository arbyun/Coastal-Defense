import math
from pygame import gfxdraw


def get_bullet_path(surface, x, y, radius, start_angle, stop_angle, color):
    start_angle = int(start_angle % 360)
    stop_angle = int(stop_angle % 360)
    if start_angle == stop_angle:
        gfxdraw.circle(surface, x, y, radius, color)
    else:
        gfxdraw.arc(surface, x, y, radius, start_angle, stop_angle, color)


def calculate_angle(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    return math.degrees(math.atan2(y1 - y0, x1 - x0))


def calculate_center_angle(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    return (x0 + x1) / 2, (y0 + y1) / 2
