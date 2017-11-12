import argparse
import statistics
from ast import literal_eval

def read_file(fname):
    row = [None] * 8
    bins, enriched_bins = [], []
    bins_line, clusters_line = False, False
    with open(fname, 'r') as f:
        for line in f:
            if line.startswith('Enriched'):
                row[0] = int(line.split()[-1])
            elif line.startswith('Valid'):
                row[1] = int(line.split()[-1])
            elif line.startswith('Nodes placed'):
                l = line.strip().split()
                n, t = map(int, l[-2].split('/'))
                r = 100* (n / float(t))
                row[2] = n
                row[3] = t
                row[4] = r
            elif line.startswith('Nodes correctly'):
                l = line.strip().split()
                n, t = map(int, l[-2].split('/'))
                r = 100 * (n / float(t))
                row[5] = n
                row[6] = t
                row[7] = r
            elif line.startswith('total bins'):
                bins_line = True
            elif line.startswith('enriched clusters'):
                clusters_line = True
            elif line.startswith('['):
                list1 = literal_eval(line.strip())
                if bins_line:
                    bins = list1
                    bins_line = False
                elif clusters_line:
                    enriched_bins = list1
                    clusters_line = False
    return row, bins, enriched_bins

def get_medians(results):
    medians = [None] * len(results[0])
    for i in range(len(results[0])):
        medians[i] = statistics.median([r[i] for r in results])
    return medians

def write_medians(medians, median_bins, median_enriched, fout):
    with open(fout, 'w') as f:
        f.write('Enriched clusters (for p=0.05): {}\n'.format(medians[0]))
        f.write('Valid clusters: {}\n'.format(medians[1]))
        f.write('Nodes placed in an enriched cluster: {}/{} ({})\n'.format(medians[2], medians[3], medians[4]))
        f.write('Nodes correctly clustered: {}/{} ({})\n'.format(medians[5], medians[6], medians[7]))
        f.write(str(median_bins) + '\n')
        f.write(str(median_enriched))

def get_medians_list(bins_list):
    import math
    import numpy as np
    top_size = 0
    for i in range(len(bins_list)):
        top_size_bins = sorted(bins_list[i], key=lambda x: x[0], reverse=True)[0][0]
        if top_size_bins > top_size: top_size = top_size_bins
    end_no = math.log(top_size, 2)
    cl_sizes = map(int, np.logspace(1.0, end_no, base=2, num=end_no, endpoint=True)[1:])
    size_map = {bin: [] for bin in cl_sizes}
    for i in range(len(bins_list)):
        bins_map = {ix: num for (ix, num) in bins_list[i]}
        for size in size_map.keys():
            if size in bins_map:
                size_map[size].append(bins_map[size])
            else:
                size_map[size].append(0)
    medians_list = list((size, np.median(l)) for size, l in size_map.items())
    return medians_list

def main():
    p = argparse.ArgumentParser()
    p.add_argument('param_file')
    p.add_argument('-u', '--under', action='store_true')
    opts = p.parse_args()

    params = []
    with open(opts.param_file, 'r') as f:
        for line in f:
            params.append(line.strip())

    for param in params:
        results = []
        bins_list, enriched_list = [], []
        for i in range(0, 10):
            if opts.under:
                fname = 'under100_{}_trial{}_l5_filter50_eval.txt'.format(param, i)
            else:
                fname = 'over100_{}_trial{}_l5_filter50_eval.txt'.format(param, i)
            print fname
            result, bins, enriched_bins = read_file(fname)
            results.append(result)
            bins_list.append(bins)
            enriched_list.append(enriched_bins)
        medians = get_medians(results)
        median_bins = get_medians_list(bins_list)
        median_enriched = get_medians_list(enriched_list)
        if opts.under:
            fout = 'under100_{}_median.txt'.format(param)
        else:
            fout = 'over100_{}_median.txt'.format(param)
        write_medians(medians, median_bins, median_enriched, fout)


if __name__ == '__main__':
    main()

