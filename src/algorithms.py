import numpy as np
from abc import ABC, abstractmethod
from pandas import DataFrame
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


class Area(ABC):
    """Class representing an area.

    Not sure about how to store the list of points.
    """

    @abstractmethod
    def plot(self, plt: plt):
        pass


class Circle(Area):
    def __init__(self, center: Point, radius):
        super().__init__()
        self.center = center
        self.radius = radius

    def plot(self, plt: plt):
        circle = plt.Circle(self.center.coords(),
                            self.radius, color='g', fill=False)
        ax = plt.gca()
        ax.add_artist(circle)


class Algorithm(ABC):
    """Abstract class representing a Convex Hull algorithm.

    Each subclass must implement these functions:

        - def _execute(self, points: DataFrame) -> Area
    """

    def __init__(self):
        super().__init__()
        self.name = self.__class__.__name__

    @abstractmethod
    def execute(self, points: DataFrame) -> Area:
        """Run the algorithm and return the result and the duration.

        Args:
            points (DataFrame): The points.

        Returns:
            result (Area): The convex Hull.
        """
        pass


class AklToussaint(Algorithm):
    def execute(self, points: DataFrame) -> Area:
        # exemple iteration
        for idx, x, y in points.itertuples():
            # print(x)
            # print(y)
            pass
        return Area()


class Ritter(Algorithm):
    def execute(self, points: DataFrame) -> Area:
        """Ritter's bounding circle algorithm."""
        dummy = points.iloc[0]
        prev_dist = 0
        for idx, point in points.iterrows():
            dist = square_dist(dummy, point)
            if prev_dist < dist:
                prev_dist = dist
                a = point

        prev_dist = 0
        for idx, point in points.iterrows():
            dist = square_dist(a, point)
            if prev_dist < dist:
                prev_dist = dist
                b = point
        c = middle(a, b)
        rsq = prev_dist / 4
        r = sqrt(rsq)

        for idx, p in points.iterrows():
            dx = p.x - c.x
            dy = p.y - c.y
            dsq = dx * dx + dy * dy
            if dsq > rsq:
                dist = sqrt(dsq)
                r = (r + dist) / 2
                factor = r / dist
                c = Point(p.x - dx * factor, p.y - dy * factor)
                rsq = r * r
        return Circle(c, r)
