"""
Quick script to filter small clusters out of results files

"""
import sys
import argparse
import io_functions as io

DEFAULT_MIN_SIZE = 3

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Original clusters input file")
    parser.add_argument("-c", "--cutoff", nargs="?", default=DEFAULT_MIN_SIZE,
                        help="Cutoff for filtering cluster size")
    opts = parser.parse_args()

    clusters = io.read_clusters(opts.input_file)
    filtered_clusters = [c for c in clusters if len(c) >= int(opts.cutoff)]
    io.output_clusters(filtered_clusters, '')


if __name__ == '__main__':
    main()
