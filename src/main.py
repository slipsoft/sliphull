#!/usr/bin/env python

import datasets
import matplotlib.pyplot as plt
from algorithms import *
from pprint import pprint

datasets.download()

algos = [
    RitterAklToussaint(),
    Ritter(),
    QuickHull(),
    QuickHullAklToussaint(),
]

bench, data = datasets.benchmark(algos, end=500, step=10)
pprint(bench)

datasets.plot(data[2], [
    bench['RitterAklToussaint']['result'][2],
    bench['Ritter']['result'][2],
    bench['QuickHull']['result'][2],
    bench['QuickHullAklToussaint']['result'][2],
])

AklToussaint().execute(datasets.get(2))
plt.show()
