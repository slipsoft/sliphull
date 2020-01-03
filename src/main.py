#!/usr/bin/python

import datasets
from algorithms import AklToussaint, Ritter

datasets.download()

algos = [
    AklToussaint(),
    # Ritter()
]
print(datasets.benchmark(algos, 10, 15))

datasets.plot(3)