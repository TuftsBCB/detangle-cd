#!/usr/sup/bin/python2.7

from dsdio import read_adjacency, read_names
from PPIparser import printPPI
import sys

"""
Converts the adjacency matrix + names list to the "source\ttarget\tweight\n" format
"""

if __name__ == "__main__":
    print sys.argv
    printPPI(sys.argv[1], read_adjacency(sys.argv[2]), read_names(sys.argv[3]))
