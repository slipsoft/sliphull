import wget
import zipfile
import ssl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os
import numpy as np
from algorithms import Algorithm, PointSet, QuickHull
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


def plot(points: PointSet, areas=[]) -> plt:
    """Plot one of the datasets.

    Args:
        points (PointSet): The points of the dataset to plot.
        areas (List[Area]): An array of Area objects to plot.

    """
    plt.figure()
    patches = []
    for area in areas:
        color = np.random.rand(3,)
        area.plot(plt, color)
        patches.append(mpatches.Patch(color=color, label=area.name))
    plt.legend(handles=patches)

    # plot the points as lines
    #plt.plot(points.x_col(), points.y_col(), 'r')

    # plot the points as dots
    points.plot(plt)

    plt.title('Algorithm comparision (%d points)' % len(points))
    plt.axis('equal')
    plt.tight_layout()
    return plt


def benchmark(algos: List[Algorithm], begin=0, end=NB_FILES, step=1) -> Dict:
    """Make a benchmark of the given algorithms.

    Args:
        algos (List[Algorithm]): The algorithms to benchmark.
        begin (int): Index of the first dataset to use.
        end (int): Index of the last dataset to use.
        step (int): Number of files to combine.

    Returns:
        Dict: The results of the benchmark

    """
    results = defaultdict(lambda: {
        'result': [],
        'duration': [],
        'quality': [],
    })
    data = []
    for idx, file in enumerate(ALL_FILES[begin:end]):
        modulo = idx % step
        if modulo == 0:
            points = get_from_file(file)
        else:
            points += get_from_file(file)
        if modulo == step - 1:
            data.append(points)
            area = QuickHull().execute(points).area()
            for algo in algos:
                start = time()
                result = algo.execute(points)
                duration = time() - start
                results[algo.name]['result'].append(result)
                results[algo.name]['duration'].append(duration)
                results[algo.name]['quality'].append(result.area()/area - 1)

    # Plot the duration comparision
    fig, ax1 = plt.subplots()
    ax1.set_ylabel('Quality (Lower is best)')
    ax1.bar(range(1, len(algos) + 1),
            [np.mean(results[algo]['quality']) for algo in results],
            0.3)
    ax2 = ax1.twinx()
    ax2.set_ylabel('Duration (s)')
    ax2.boxplot([results[algo]['duration'] for algo in results])
    # set ticks and labels on ax (otherwise it does not work)
    ax2.set_xticklabels(results.keys())
    # reduce size of x labels
    ax2.tick_params(axis='x', which='major', labelsize=7)
    plt.title('Algorithm comparision (%d executions | %d points)' %
              ((end - begin) / step, len(data[0])))
    plt.tight_layout()

    return results, data
