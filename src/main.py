#!/usr/bin/python

import datasets
from algorithms import AklToussaint, Ritter

datasets.download()

algos = [
    # AklToussaint(),
    Ritter()
]
bench = datasets.benchmark(algos, 0, 5)

datasets.plot(1, [bench['Ritter']['result'][1]])