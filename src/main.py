#!/usr/bin/python

import datasets
from algorithms import RitterAklToussaint, Ritter
from pprint import pprint

datasets.download()

algos = [
    RitterAklToussaint(),
    Ritter()
]
bench = datasets.benchmark(algos, 0, 20)
pprint(bench)

datasets.plot(1, [
    bench['RitterAklToussaint']['result'][1],
    bench['Ritter']['result'][1],
]).show()