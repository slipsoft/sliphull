import wget
import zipfile
import ssl
import pandas as pd
import matplotlib.pyplot as plt
import os
from algorithms import Algorithm
from glob import glob
from time import time
from collections import defaultdict
from typing import List, Dict


def download() -> bool:
    """Download the dataset from internet if it doesn't exist.

    Returns:
        bool: True if it had to be downloaded.

    """
    if os.path.isdir('samples') and len(all_files()) > 0:
        _clean_files()
        return False
    url = 'http://www-apr.lip6.fr/~buixuan/files/algav2019/Varoumas_benchmark.zip'
    ssl._create_default_https_context = ssl._create_unverified_context
    filename = wget.download(url)
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall()
    os.unlink(filename)
    _clean_files()
    return True

def _clean_files() -> None:
    """Well ok it's quite dirty, but the first file is corrupted
    and it is easier to start counting from 0.
    """
    try:
        os.rename('samples/test-1664.points', 'samples/test-0.points')
        os.rename('samples/test-1663.points', 'samples/test-1.points')
    except FileNotFoundError:
        pass


def all_files() -> List[str]:
    """Get all dataset file names."""
    return glob('samples/*')


def get_from_file(file) -> pd.DataFrame:
    """Get a dataframe from a dataset file name."""
    return pd.read_csv(file, sep=' ', names=['x', 'y'])


def get(num: int) -> pd.DataFrame:
    """Get one of the datasets.

    Args:
        num (int): The number of the dataset to plot.

    Returns:
        DataFrame: The points of this dataset.

    """
    file = 'samples/test-' + str(num) + '.points'
    return get_from_file(file)


def plot(num: int) -> None:
    """Plot one of the datasets.

    Args:
        num (int): The number of the dataset to plot.

    """
    points = get(num)
    print(points)

    # plot the points as lines
    plt.plot(points['x'], points['y'], 'C3', zorder=1)

    # plot the points as dots
    plt.scatter(points['x'], points['y'], zorder=2)

    plt.axis('off')
    plt.show()


def benchmark(algos: List[Algorithm]) -> Dict:
    """Make a benchmark of the given algorithms.

    Args:
        algos (List[Algorithm]): The algorithms to benchmark.

    Returns:
        Dict: The results of the benchmark

    """
    results = defaultdict(lambda: {
        'result': [],
        'duration': []
    })
    for index, file in enumerate(all_files()):
        points = get_from_file(file)
        for algo in algos:
            start = time()
            result = algo.execute(points)
            duration = time() - start
            results[algo.name]['result'].append(result)
            results[algo.name]['duration'].append(duration)
    return results
