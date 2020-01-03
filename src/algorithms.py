import csv
import numpy as np
from abc import ABC, abstractmethod
from typing import List
from math import sqrt
import matplotlib.pyplot as plt


def square_dist(point1, point2):
    return (point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2


def dist(point1, point2):
    return sqrt(square_dist(point1, point2))


def middle(point1, point2):
    return Point((point1.x + point2.x) / 2, (point1.y + point2.y) / 2)


def in_ABC(P, A, B, C):
    """Test if P is inside the triangle ABC.

    Not tested yet

    Args:
        P (Point): The point to test
        A (Point): Point A of the triangle
        B (Point): Point B of the triangle
        C (Point): Point C of the triangle

    Returns:
        bool: True if it is inside or else False
    """
    l1 = ((B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)) / \
        ((B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y))
    if l1 > 1 or l1 < 0:
        return False
    l2 = ((C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)) / \
        ((B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y))
    if l2 > 1 or l2 < 0:
        return False
    l3 = 1 - l1 - l2
    return l3 <= 1 and l1 >= 0


class Point(object):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def coords(self):
        return (self.x, self.y)


class PointSet(list):
    @staticmethod
    def from_csv(file):
        with open(file, newline='') as csvfile:
            pointreader = csv.reader(csvfile, delimiter=' ', )
            return PointSet([Point(int(row[0]), int(row[1])) for row in pointreader])

    def x_col(self):
        return [p.x for p in self]

    def y_col(self):
        return [p.y for p in self]


def akl_toussaint(points: PointSet):
    top = points[0]
    bottom = top
    left = top
    right = top
    # get initial values
    for p in points:
        if (p.x < left.x):
            left = p
        if (p.x > right.x):
            right = p
        if (p.y > top.y):
            top = p
        if (p.y < bottom.y):
            bottom = p

    rest = PointSet([top, bottom])
    if left != top and left != bottom:
        rest.append(left)
    if right != top and right != bottom:
        rest.append(right)

    for p in points:

        if (p == top):
            continue
        if (p == bottom):
            continue
        if (p == right):
            continue
        if (p == left):
            continue

        d = (top.x - left.x) * (p.y - left.y) - \
            (top.y - left.y) * (p.x - left.x)
        if d > 0:
            rest.append(p)
            continue

        d = (right.x - top.x) * (p.y - top.y) - \
            (right.y - top.y) * (p.x - top.x)
        if d > 0:
            rest.append(p)
            continue

        d = (bottom.x - right.x) * (p.y - right.y) - \
            (bottom.y - right.y) * (p.x - right.x)
        if d > 0:
            rest.append(p)
            continue

        d = (left.x - bottom.x) * (p.y - bottom.y) - \
            (left.y - bottom.y) * (p.x - bottom.x)
        if d > 0:
            rest.append(p)
            continue

    return rest, Poly([top, right, bottom, left])


class Area(ABC):
    """Class representing an area.

    Not sure about how to store the list of points.
    """

    def __init__(self, name):
        super().__init__()
        self.name = name

    @abstractmethod
    def plot(self, plt: plt, color='g'):
        pass


class Circle(Area):
    def __init__(self, center: Point, radius, name=''):
        super().__init__(name)
        self.center = center
        self.radius = radius

    def plot(self, plt: plt, color='g'):
        circle = plt.Circle(self.center.coords(),
                            self.radius, color=color,
                            fill=False)
        ax = plt.gca()
        ax.add_artist(circle)
        return


class Poly(Area):
    def __init__(self, points, name=''):
        super().__init__(name)
        self.points = PointSet(points)

    def plot(self, plt: plt, color='g'):
        xs = self.points.x_col()
        ys = self.points.y_col()

        # append a copy of the first point to close the shape
        xs.append(self.points[0].x)
        ys.append(self.points[0].y)
        plt.plot(xs, ys, color=color)

        return


class Algorithm(ABC):
    """Abstract class representing a Convex Hull algorithm.

    Each subclass must implement these functions:

        - def _execute(self, points: PointSet) -> Area
    """

    def __init__(self):
        super().__init__()
        self.name = self.__class__.__name__

    @abstractmethod
    def execute(self, points: PointSet) -> Area:
        """Run the algorithm and return the result and the duration.

        Args:
            points (PointSet): The points.

        Returns:
            result (Area): The convex Hull.
        """
        pass


class Ritter(Algorithm):
    def execute(self, points: PointSet) -> Area:
        """Ritter's bounding circle algorithm."""
        dummy = points[0]
        prev_dist = 0
        for point in points[1:]:
            dist = square_dist(dummy, point)
            if prev_dist < dist:
                prev_dist = dist
                a = point

        prev_dist = 0
        for point in points:
            dist = square_dist(a, point)
            if prev_dist < dist:
                prev_dist = dist
                b = point
        c = middle(a, b)
        rsq = prev_dist / 4
        r = sqrt(rsq)

        for p in points:
            dx = p.x - c.x
            dy = p.y - c.y
            dsq = dx * dx + dy * dy
            if dsq > rsq:
                dist = sqrt(dsq)
                r = (r + dist) / 2
                factor = r / dist
                c = Point(p.x - dx * factor, p.y - dy * factor)
                rsq = r * r
        return Circle(c, r, self.name)


class RitterAklToussaint(Ritter):
    def execute(self, points: PointSet) -> Area:
        points, area = akl_toussaint(points)
        # return area
        return super().execute(points)
