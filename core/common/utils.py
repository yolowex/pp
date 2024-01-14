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


def calculate_p3_position(p1, p2, distance_to_p3):
    # Calculate the vector from P1 to P2
    vector_p1_to_p2 = p2 - p1

    # Normalize the vector to get the direction
    direction_p1_to_p2 = vector_p1_to_p2.normalize()

    # Calculate the position of P3
    p3 = p1 + direction_p1_to_p2 * distance_to_p3

    return Vector2(p3)


def generate_smaller_polygons(base_polygon: list[Vector2], size):
    smaller_polygons = []
    base_x, base_y = base_polygon[0]
    base_w = base_polygon[0].distance_to(base_polygon[1])
    base_h = base_polygon[0].distance_to(base_polygon[3])
    x = 0
    while x < (base_w / size):
        y = 0
        while y < (base_h / size):
            new_point_1 = calculate_p3_position(
                base_polygon[0], base_polygon[1], size * x
            )
            new_point_2 = calculate_p3_position(
                base_polygon[0], base_polygon[3], size * y
            )
            new_point_3 = new_point_2.copy() + (base_polygon[0] - base_polygon[1])
            new_point_4 = new_point_1.copy() + (base_polygon[0] - base_polygon[3])

            y += 1
            smaller_polygons.append(
                [new_point_1, new_point_2, new_point_3, new_point_4]
            )

        x += 1

    return smaller_polygons


def cut_and_fit_squares(A, B, C):
    # Function to find the length of a vector
    def vector_length(v):
        return math.sqrt(v.x**2 + v.y**2)

    # Function to normalize a vector
    def normalize_vector(v):
        length = vector_length(v)
        return pg.Vector2(v.x / length, v.y / length)

    # Function to cut a square into smaller squares that fit into another square
    def cut_square(square, target_square):
        # Calculate the diagonal vector
        diagonal_vector = target_square[2] - target_square[0]
        diagonal_length = vector_length(diagonal_vector)

        # Normalize the diagonal vector
        diagonal_normalized = normalize_vector(diagonal_vector)

        # Calculate the number of squares that can fit along the diagonal
        num_squares = int(diagonal_length / vector_length(square[1] - square[0]))

        # Calculate the step size for cutting the square
        step_size = diagonal_length / num_squares

        # Cut the square into smaller squares along the diagonal
        cut_squares = []
        for i in range(num_squares):
            start_point = square[0] + diagonal_normalized * (i * step_size)
            end_point = start_point + diagonal_normalized * step_size
            cut_squares.append([start_point, square[1], end_point, square[0]])

        return cut_squares

    # Check if A^2 + B^2 = C^2 (Pythagorean theorem)
    # if vector_length(C[2] - C[0]) ** 2 != vector_length(A[2] - A[0]) ** 2 + vector_length(B[2] - B[0]) ** 2:
    #     print("Error: Pythagorean theorem not satisfied.")
    #     return None

    # Cut squares A and B into smaller squares that fit into C
    cut_A = cut_square(A, C)
    cut_B = cut_square(B, C)

    # Combine the cut squares into a set of polygons
    polygons = cut_A + cut_B

    return polygons


def rotate_point(point, center, angle):
    """Rotate a point around a center."""
    angle_rad = math.radians(angle)
    rotated_x = (
        center[0]
        + (point[0] - center[0]) * math.cos(angle_rad)
        - (point[1] - center[1]) * math.sin(angle_rad)
    )
    rotated_y = (
        center[1]
        + (point[0] - center[0]) * math.sin(angle_rad)
        + (point[1] - center[1]) * math.cos(angle_rad)
    )
    return Vector2(rotated_x, rotated_y)


def cut_and_fill_squares(square1, square2, target_square):
    """Cut the first two squares and fill the third square with resulting smaller squares."""
    cut_squares = []

    # Cut the first square
    intersection_points = [
        point for point in square1 if target_square.collidepoint(point)
    ]
    if len(intersection_points) == 2:
        cut_line = pg.draw.line(
            pg.Surface((1, 1)),
            (255, 255, 255),
            intersection_points[0],
            intersection_points[1],
            1,
        )
        cut_square1 = square1.clip(cut_line)
        cut_squares.append(cut_square1)

    # Cut the second square
    intersection_points = [
        point for point in square2 if target_square.collidepoint(point)
    ]
    if len(intersection_points) == 2:
        cut_line = pg.draw.line(
            pg.Surface((1, 1)),
            (255, 255, 255),
            intersection_points[0],
            intersection_points[1],
            1,
        )
        cut_square2 = square2.clip(cut_line)
        cut_squares.append(cut_square2)

    # Calculate the smaller squares that can fill the third square
    fill_squares = []
    for cut_square in cut_squares:
        for i in range(2):
            for j in range(2):
                fill_square = target_square.copy()
                fill_square.x += i * target_square.width / 2
                fill_square.y += j * target_square.height / 2
                fill_square = fill_square.clip(cut_square)
                fill_squares.append(fill_square)

    return fill_squares


def poly_to_rect(poly: list[Vector2]):
    return FRect(
        0,
        0,
        round(poly[0].distance_to(poly[1]), 2),
        round(poly[0].distance_to(poly[3]), 2),
    )


def dissect(a, b, c):
    rectangles = []

    # Arrange squares in descending order
    squares = sorted([a, b, c], reverse=True)

    # Calculate the size of the largest square
    max_size = squares[0]

    # Calculate the position and size of the two smaller squares
    small1_size = squares[1]
    small1_pos = (max_size - small1_size, 0)

    small2_size = squares[2]
    small2_pos = (0, small1_size)

    # Append rectangles to the list
    rectangles.append(FRect(0, 0, max_size, max_size))
    rectangles.append(FRect(*small1_pos, small1_size, small1_size))
    rectangles.append(FRect(*small2_pos, small2_size, small2_size))

    return rectangles


def dissect_rectangles(rect1, rect2):
    # Check if the rectangles have the same area
    rect1.width = int(rect1.width)
    rect1.height = int(rect1.height)
    rect2.width = int(rect2.width)
    rect2.height = int(rect2.height)

    if rect1.width * rect1.height != rect2.width * rect2.height:
        raise ValueError("Rectangles must have the same area")

    # Initialize variables
    sub_rectangles = []
    remaining_area = rect1.width * rect1.height

    # Iterate until the entire area is covered
    while remaining_area > 0:
        # Calculate the width and height of the next sub-rectangle
        width = min(rect1.width, remaining_area // rect1.height)
        height = min(rect1.height, remaining_area // rect1.width)

        # Create a sub-rectangle and add it to the list
        sub_rect = FRect(rect1.left, rect1.top, width, height)
        sub_rectangles.append(sub_rect)

        # Update the position and size of the first rectangle
        rect1.width -= width
        rect1.height -= height
        rect1.left += width

        # Update the remaining area
        remaining_area = rect1.width * rect1.height

    # Calculate the offset between rect1 and rect2
    dx = rect2.left - sub_rectangles[0].left
    dy = rect2.top - sub_rectangles[0].top

    # Apply the offset to all sub-rectangles
    sub_rectangles = [FRect(sub_rect.left + dx, sub_rect.top + dy, sub_rect.width, sub_rect.height) for sub_rect in sub_rectangles]

    return sub_rectangles
