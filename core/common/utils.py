import datetime
import pygame as pg
from pygame import Vector2, FRect
import math


def rotate_towards(vector, target, angle_degrees):
    # angle_radians = math.radians(angle_degrees)
    relative_vector: Vector2 = target - vector
    rotated_vector = relative_vector.rotate(angle_degrees)
    new_vector = vector + rotated_vector
    return new_vector


def get_rotated_point(point: Vector2, length, degree):
    p2 = point.copy()
    p2.x += length
    return rotate_towards(point, p2, degree)


def find_triangle_center(vector1, vector2, vector3):
    # Calculate the average x and y coordinates
    center_x = (vector1.x + vector2.x + vector3.x) / 3
    center_y = (vector1.y + vector2.y + vector3.y) / 3

    # Create a new Vector2 with the calculated center coordinates
    center_vector = pg.math.Vector2(center_x, center_y)

    return center_vector


def center_triangle(
    vertex1: Vector2, vertex2: Vector2, vertex3: Vector2, new_center: Vector2
):
    # Find the center of the triangle
    triangle_center = find_triangle_center(vertex1, vertex2, vertex3)

    # Calculate the translation vector to move the center to the specified point
    translation_vector = new_center - triangle_center

    # Translate each vertex by the calculated vector
    new_vertex1 = vertex1 + translation_vector
    new_vertex2 = vertex2 + translation_vector
    new_vertex3 = vertex3 + translation_vector

    vertex1.xy = new_vertex1
    vertex2.xy = new_vertex2
    vertex3.xy = new_vertex3


def log_time():
    current_time = datetime.datetime.now().time()
    time_string = current_time.strftime("%H:%M:%S")
    return time_string


def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + b * t


def inv_lerp(a: float, b: float, v: float) -> float:
    return (v - a) / (b - a)


def remap(i_min, i_max, o_min, o_max, v):
    t = inv_lerp(i_min, i_max, v)
    return lerp(o_min, o_max, t)


def now():
    return pg.time.get_ticks() / 1000


def closest_point_on_line(point1, point2, target_point):
    # Calculate the direction vector of the line
    line_vector = pg.Vector2(point2[0] - point1[0], point2[1] - point1[1])

    # Calculate the vector from the first point of the line to the target point
    target_vector = pg.Vector2(target_point[0] - point1[0], target_point[1] - point1[1])

    # Calculate the dot product of the line vector and the target vector
    dot_product = line_vector.dot(target_vector)

    # Calculate the squared length of the line vector
    line_length_squared = line_vector.length_squared()

    # Calculate the parameter along the line where the closest point lies
    t = dot_product / line_length_squared

    # Clamp the parameter to ensure the closest point is within the line segment
    t = max(0, min(1, t))

    # Calculate the closest point on the line
    closest_point = (
        point1[0] + t * (point2[0] - point1[0]),
        point1[1] + t * (point2[1] - point1[1]),
    )

    return closest_point


def resize_line(point1, point2, percentage):
    # Calculate the direction vector of the original line
    line_vector = (point2[0] - point1[0], point2[1] - point1[1])

    # Calculate the length of the original line
    original_length = math.sqrt(line_vector[0] ** 2 + line_vector[1] ** 2)

    # Calculate the extension length based on the percentage
    extension_length = original_length * (percentage / 100.0)

    # Calculate the scaling factor to extend the line
    scaling_factor = (original_length + 2 * extension_length) / original_length

    # Calculate the new coordinates of both ends
    new_point1 = (
        point1[0] - extension_length * (line_vector[0] / original_length),
        point1[1] - extension_length * (line_vector[1] / original_length),
    )

    new_point2 = (
        point2[0] + extension_length * (line_vector[0] / original_length),
        point2[1] + extension_length * (line_vector[1] / original_length),
    )

    return new_point1, new_point2


def create_square_from_line(start_point: Vector2, end_point: Vector2, direction=1):
    # Calculate the direction vector of the line
    some_factor = end_point - start_point
    some_factor.normalize_ip()
    side_length = start_point.distance_to(end_point) * direction
    # Calculate the perpendicular vector for the square
    perpendicular = Vector2(some_factor.y, -some_factor.x)

    # Calculate the four vertices of the square
    p2 = start_point
    p3 = start_point - perpendicular * side_length

    p1 = end_point
    p4 = end_point - perpendicular * side_length

    # Return the list of points representing the square
    return [p1, p2, p3, p4]


def get_polygon_center(points):
    # Ensure the list of points is not empty
    if not points:
        raise ValueError("List of points cannot be empty")

    # Calculate the average x and y coordinates to find the center
    total_x = sum(point[0] for point in points)
    total_y = sum(point[1] for point in points)

    center_x = total_x / len(points)
    center_y = total_y / len(points)

    return Vector2(center_x, center_y)


def get_line_center(point1, point2):
    # Calculate the average x and y coordinates to find the center
    center_x = (point1[0] + point2[0]) / 2
    center_y = (point1[1] + point2[1]) / 2

    return Vector2(center_x, center_y)


def draw_border(screen, surface, border_color, border_width, position):
    rect = surface.get_rect()

    pg.draw.rect(
        screen,
        border_color,
        FRect(
            position.x - border_width,
            position.y - border_width,
            rect.w + border_width,
            rect.h + border_width,
        ),
        width=border_width,
    )
