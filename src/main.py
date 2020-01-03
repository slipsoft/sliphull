#!/usr/bin/env python

import datasets
import matplotlib.pyplot as plt
from algorithms import AklToussaint, RitterAklToussaint, Ritter
from pprint import pprint

datasets.download()

algos = [
    RitterAklToussaint(),
    Ritter()
]
bench = datasets.benchmark(algos, 0, 30)
pprint(bench)

datasets.plot(2, [
    bench['RitterAklToussaint']['result'][2],
    bench['Ritter']['result'][2],
])

AklToussaint().execute(datasets.get(2))
plt.show()
