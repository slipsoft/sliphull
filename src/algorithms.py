from abc import ABC, abstractmethod
from pandas import DataFrame
from typing import List

class Algorithm(ABC):
    """Abstract class representing a Convex Hull algorithm.

    Each subclass must implement these functions:

        - def _execute(self, points: DataFrame) -> List[int]
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def execute(self, points: DataFrame) -> List[int]:
        """Run the algorithm and return the result and the duration.

        Args:
            points (DataFrame): The points.

        Returns:
            result (List[int]): The convex Hull.
        """
        pass


class AklToussaint(Algorithm):
    def execute(self, points: DataFrame) -> List[int]:
        return [];


class Ritter(Algorithm):
    pass
