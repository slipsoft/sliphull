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

bench, data = datasets.benchmark(algos, end=100, step=3)
pprint(bench)

num = 0
datasets.plot(data[num], [
    # bench['RitterAklToussaint']['result'][num],
    bench['Ritter']['result'][num],
    bench['QuickHull']['result'][num],
    # bench['QuickHullAklToussaint']['result'][num],
])

AklToussaint().execute(datasets.get(2))
plt.show()
