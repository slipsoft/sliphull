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
        """Not finished but it's only the first implementation."""
        dummy = points.iloc[0]
        prev_sq_dist = 0
        for idx, point in points.iterrows():
            sq_dist = square_dist(dummy, point)
            if prev_sq_dist < sq_dist:
                prev_sq_dist = sq_dist
                a = point
        prev_sq_dist = 0
        for idx, point in points.iterrows():
            sq_dist = square_dist(a, point)
            if prev_sq_dist < sq_dist:
                prev_sq_dist = sq_dist
                b = point
        center = middle(a, b)
        return Circle(center, dist(center, b))
