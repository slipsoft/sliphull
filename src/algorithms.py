import numpy as np
from abc import ABC, abstractmethod
from pandas import DataFrame
from typing import List


class Area(object):
    def __init__(self):
        super().__init__()
        self.points = np.array([])

    def getXs(self) -> np.array:
        return self.points[:, 0]

    def getXs(self) -> np.array:
        return self.points[:, 1]


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
        return Area()


class Ritter(Algorithm):
    pass
