#!/usr/bin/python

import datasets
from algorithms import AklToussaint, Ritter

datasets.download()

algos = [
    AklToussaint()
]
print(datasets.benchmark(algos))

datasets.plot(3)