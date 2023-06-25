import matplotlib.pyplot as plt
import numpy as np
import copy
import time
import random
import math

K = 3


class Point:
    def __init__(self, x, y, colour):
        if random.randint(0, 100) == 99:
            self.x = random.randint(-5000, 5001)
            self.y = random.randint(-5000, 5001)
        else:
            self.x = x
            self.y = y
        self.colour = colour


def create_training_points(set_of_points, set_of_points1, set_of_points2, set_of_points3, set_of_points4):
    training_set = [Point(-4500, -4400, 'R'), Point(-4100, -3000, 'R'), Point(-1800, -2400, 'R'),
                    Point(-2500, -3400, 'R'), Point(-2000, -1400, 'R'),
                    Point(4500, -4400, 'G'), Point(4100, -3000, 'G'), Point(1800, -2400, 'G'), Point(2500, -3400, 'G'),
                    Point(2000, -1400, 'G'),
                    Point(-4500, 4400, 'B'), Point(-4100, 3000, 'B'), Point(-1800, 2400, 'B'), Point(-2500, 3400, 'B'),
                    Point(-2000, 1400, 'B'),
                    Point(4500, 4400, 'P'), Point(4100, 3000, 'P'), Point(1800, 2400, 'P'), Point(2500, 3400, 'P'),
                    Point(2000, 1400, 'P')]
    for point in training_set:
        insert_point(set_of_points, point)
        insert_point(set_of_points1, point)
        insert_point(set_of_points2, point)
        insert_point(set_of_points3, point)
        insert_point(set_of_points4, point)


def insert_point(set_of_points, point):
    row = int(point.y / 500 + 10)
    column = int(point.x / 500 + 10)
    if row == 20:
        row = 19
    if column == 20:
        column = 19

    set_of_points[row][column].append(point)


def init_set_of_points():
    set_of_points = []
    for i in range(20):
        set_of_points.append([])
        for j in range(20):
            set_of_points[i].append([])
    return set_of_points


def is_position_available(x, y, set_of_points):
    row = int(y / 500 + 10)
    column = int(x / 500 + 10)
    if row == 20:
        row = 19
    if column == 20:
        column = 19

    for point in set_of_points[row][column]:
        if point.x == x and point.y == y:
            return False

    return True


def get_coordinates(colour, set_of_points):
    x, y = 0, 0
    if colour == 'R':
        x = random.randint(-5000, 500)
        y = random.randint(-5000, 500)
    elif colour == 'G':
        x = random.randint(-499, 5001)
        y = random.randint(-5000, 500)
    elif colour == 'B':
        x = random.randint(-5000, 500)
        y = random.randint(-499, 5001)
    elif colour == 'P':
        x = random.randint(-499, 5001)
        y = random.randint(-499, 5001)

    if not is_position_available(x, y, set_of_points):
        x, y = get_coordinates(colour, set_of_points)

    return x, y


def find_nearest_neighbours(point, set_of_points):
    neighbours = []
    row = int(point.y / 500 + 10)
    column = int(point.x / 500 + 10)
    if row == 20:
        row = 19
    if column == 20:
        column = 19

    neighbours = find_nearest_neighbours_helper(point, neighbours, set_of_points[row][column])
    if column > 0:
        neighbours = find_nearest_neighbours_helper(point, neighbours, set_of_points[row][column - 1])
    if column < 19:
        neighbours = find_nearest_neighbours_helper(point, neighbours, set_of_points[row][column + 1])
    if row > 0:
        neighbours = find_nearest_neighbours_helper(point, neighbours, set_of_points[row - 1][column])
        if column > 0:
            neighbours = find_nearest_neighbours_helper(point, neighbours, set_of_points[row - 1][column - 1])
        if column < 19:
            neighbours = find_nearest_neighbours_helper(point, neighbours, set_of_points[row - 1][column + 1])
    if row < 19:
        neighbours = find_nearest_neighbours_helper(point, neighbours, set_of_points[row + 1][column])
        if column > 0:
            neighbours = find_nearest_neighbours_helper(point, neighbours, set_of_points[row + 1][column - 1])
        if column < 19:
            neighbours = find_nearest_neighbours_helper(point, neighbours, set_of_points[row + 1][column - 1])

    if len(neighbours) < K:
        neighbours.clear()
        for r in set_of_points:
            for c in r:
                neighbours = find_nearest_neighbours_helper(point, neighbours, c)

    return neighbours


def find_nearest_neighbours_helper(point, neighbours, current_set_of_points):
    for p in current_set_of_points:
        distance = distance_between_points(p, point)
        if len(neighbours) == 0:
            neighbours.append(p)
        elif len(neighbours) < K:
            flag = False
            for i in range(len(neighbours)):
                x = distance_between_points(neighbours[i], point)
                if x > distance:
                    neighbours.insert(i, p)
                    flag = True
                    break
            if not flag:
                neighbours.append(p)
        else:
            for i in range(len(neighbours)):
                x = distance_between_points(neighbours[i], point)
                if x > distance:
                    neighbours.insert(i, p)
                    del neighbours[-1]
                    break

    return neighbours


def distance_between_points(point1, point2):
    return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)


def classify(point, set_of_points):
    neighbours = find_nearest_neighbours(point, set_of_points)
    colours = [0, 0, 0, 0]
    for n in neighbours:
        if n.colour == 'R':
            colours[0] += 1
        elif n.colour == 'G':
            colours[1] += 1
        elif n.colour == 'B':
            colours[2] += 1
        elif n.colour == 'P':
            colours[3] += 1

    max_index = colours.index(max(colours))
    colour = None

    if max_index == 0:
        colour = 'R'
    elif max_index == 1:
        colour = 'G'
    elif max_index == 2:
        colour = 'B'
    elif max_index == 3:
        colour = 'P'

    point.colour = colour
    insert_point(set_of_points, point)

    return colour


def visualization(set_of_points, k, x_points_np, y_points_np):
    name = "result" + str(k)
    colours = []
    for row in set_of_points:
        for col in row:
            for point in col:
                if point.colour == 'R':
                    colours.append('red')
                elif point.colour == 'G':
                    colours.append('green')
                elif point.colour == 'B':
                    colours.append('blue')
                elif point.colour == 'P':
                    colours.append('purple')

    # for i in range(len(x_points_np)):
    plt.scatter(x_points_np, y_points_np, c=colours)
    plt.savefig(f'{name}.png')
    plt.close()


def main():
    t0 = time.perf_counter()

    global K

    set_of_points = init_set_of_points()
    set_of_points_1 = init_set_of_points()
    set_of_points_3 = init_set_of_points()
    set_of_points_7 = init_set_of_points()
    set_of_points_15 = init_set_of_points()
    all_points = []

    create_training_points(set_of_points, set_of_points_1, set_of_points_3, set_of_points_7, set_of_points_15)

    all_test_points_count = 40000
    successful_classification_1 = 0
    successful_classification_3 = 0
    successful_classification_7 = 0
    successful_classification_15 = 0

    for i in range(int(all_test_points_count / 4)):
        x, y = get_coordinates('R', set_of_points)
        point = Point(x, y, 'R')
        insert_point(set_of_points, point)
        all_points.append(point)

        x, y = get_coordinates('G', set_of_points)
        point = Point(x, y, 'G')
        insert_point(set_of_points, point)
        all_points.append(point)

        x, y = get_coordinates('B', set_of_points)
        point = Point(x, y, 'B')
        insert_point(set_of_points, point)
        all_points.append(point)

        x, y = get_coordinates('P', set_of_points)
        point = Point(x, y, 'P')
        insert_point(set_of_points, point)
        all_points.append(point)

    K = 1
    for point in all_points:
        new_point = copy.deepcopy(point)
        if classify(new_point, set_of_points_1) == point.colour:
            successful_classification_1 += 1

    K = 3
    for point in all_points:
        new_point = copy.deepcopy(point)
        if classify(new_point, set_of_points_3) == point.colour:
            successful_classification_3 += 1

    K = 7
    for point in all_points:
        new_point = copy.deepcopy(point)
        if classify(new_point, set_of_points_7) == point.colour:
            successful_classification_7 += 1

    K = 15
    for point in all_points:
        new_point = copy.deepcopy(point)
        if classify(new_point, set_of_points_15) == point.colour:
            successful_classification_15 += 1

    print("Success rate for K = 1: ", successful_classification_1 / all_test_points_count)
    print("Success rate for K = 3: ", successful_classification_3 / all_test_points_count)
    print("Success rate for K = 7: ", successful_classification_7 / all_test_points_count)
    print("Success rate for K = 15: ", successful_classification_15 / all_test_points_count)

    t1 = time.perf_counter()
    print("The execution of the program took: ", t1 - t0, " s")

    t0 = time.perf_counter()

    x_points = []
    y_points = []

    for row in set_of_points:
        for col in row:
            for pt in col:
                x_points.append(pt.x)
                y_points.append(pt.y)

    x_points_np = np.array(x_points)
    y_points_np = np.array(y_points)

    visualization(set_of_points_1, 1, x_points_np, y_points_np)
    visualization(set_of_points_3, 3, x_points_np, y_points_np)
    visualization(set_of_points_7, 7, x_points_np, y_points_np)
    visualization(set_of_points_15, 15, x_points_np, y_points_np)

    t1 = time.perf_counter()
    print("The visualization took: ", t1 - t0, " s")


if __name__ == "__main__":
    main()
