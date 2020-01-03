#!/usr/bin/python

import datasets
from algorithms import RitterAklToussaint, Ritter

datasets.download()

algos = [
    RitterAklToussaint(),
    Ritter()
]
bench = datasets.benchmark(algos, 0, 5)
print(bench)

datasets.plot(1, [
    bench['RitterAklToussaint']['result'][1],
    bench['Ritter']['result'][1]
]).show()