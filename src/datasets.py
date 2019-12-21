import wget
import zipfile
import ssl
import pandas as pd
import matplotlib.pyplot as plt
import os
from glob import glob


def download():
    """Download the dataset from internet if it doesn't exist"""
    if os.path.isdir('samples') and len(glob('samples/*')) > 0:
        return
    url = 'http://www-apr.lip6.fr/~buixuan/files/algav2019/Varoumas_benchmark.zip'
    ssl._create_default_https_context = ssl._create_unverified_context
    filename = wget.download(url)
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall()
    os.unlink(filename)


def plot(num: int):
    """Plot one of the datasets.

    Parameters
    ----------
    num : int
        The number of the dataset to plot.

    Returns
    -------
    None

    """
    f = 'samples/test-' + str(num) + '.points'
    points = pd.read_csv(f, sep=' ', names=['x', 'y'])
    print(points)

    # plot the points as lines
    plt.plot(points['x'], points['y'], 'C3', zorder=1)

    # plot the points as dots
    plt.scatter(points['x'], points['y'], zorder=2)

    plt.axis('off')
    plt.show()
