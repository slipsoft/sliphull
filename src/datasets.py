import wget
import zipfile
import ssl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
from numpy.random import rand
from algorithms import Algorithm, PointSet
from glob import glob
from time import time
from collections import defaultdict
from typing import List, Dict

#: Index of the last file after cleaning
NB_FILES = 1663
ALL_FILES = ['samples/test-%s.points' % i for i in range(NB_FILES)]


def download() -> bool:
    """Download the dataset from internet if it doesn't exist.

    Returns:
        bool: True if it had to be downloaded.

    """
    if os.path.isdir('samples') and len(ALL_FILES) > 0:
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
        os.rename('samples/test-%s.points' %
                  (NB_FILES + 1), 'samples/test-0.points')
        os.replace('samples/test-%s.points' %
                  (NB_FILES), 'samples/test-1.points')
    except FileNotFoundError:
        pass


def get_from_file(file: str) -> PointSet:
    """Get a PointSet from a dataset file name."""
    return PointSet.from_csv(file)


def get(num: int) -> PointSet:
    """Get one of the datasets.

    Args:
        num (int): The number of the dataset to plot.

    Returns:
        PointSet: The points of this dataset.

    """
    file = 'samples/test-%s.points' % (num)
    return get_from_file(file)


def plot(num: int, areas=[]) -> plt:
    """Plot one of the datasets.

    Args:
        num (int): The number of the dataset to plot.

    """
    points = get(num)

    plt.figure()
    patches = []
    for area in areas:
        color = rand(3,)
        area.plot(plt, color)
        patches.append(mpatches.Patch(color=color, label=area.name))
    plt.legend(handles=patches)

    # plot the points as lines
    #plt.plot(points.x_col(), points.y_col(), 'r')

    # plot the points as dots
    points.plot(plt)

    plt.axis('equal')
    return plt


def benchmark(algos: List[Algorithm], begin=0, end=NB_FILES) -> Dict:
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
    for file in ALL_FILES[begin:end]:
        points = get_from_file(file)
        for algo in algos:
            start = time()
            result = algo.execute(points)
            duration = time() - start
            results[algo.name]['result'].append(result)
            results[algo.name]['duration'].append(duration)

    # Plot the duration comparision
    fig, ax = plt.subplots()
    ax.set_ylabel('Duration (s)')
    ax.boxplot([results[algo]['duration'] for algo in results])
    ax.set_xticklabels(results.keys())  # set ticks and labels on ax1 (otherwise it does not work)
    ax.tick_params(axis='x', which='major', labelsize=7)  # reduce size of x labels

    plt.title('Algorithm comparision (%d executions)' % (end - begin))
    plt.tight_layout()
    return results
