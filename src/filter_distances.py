#!/usr/bin/env python
import sys
import argparse
import numpy as np

DISTANCE_THRESHOLD = 6.5

def main():
    p = argparse.ArgumentParser()
    p.add_argument('input_matrix')
    p.add_argument('-t', '--threshold', nargs='?', type=float,
                   default=DISTANCE_THRESHOLD)
    opts = p.parse_args()

    in_mtx = np.loadtxt(opts.input_matrix)
    filter_func = np.vectorize(lambda x: x if x <= opts.threshold else 0.0)
    filtered_mtx = filter_func(in_mtx)
    np.savetxt(sys.stdout, filtered_mtx, fmt='%.3f')

if __name__ == '__main__':
    main()
