import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cluster_file")
    parser.add_argument("node_map")
    opts = parser.parse_args()

    f = open(opts.node_map, 'r')
    node_map = {l.rstrip().split()[1]: l.rstrip().split()[0]
                  for l in f.readlines()}
    f.close()

    cl_ix = 1
    cf = open(opts.cluster_file, 'r')
    for line in cf.readlines():
        cluster = line.rstrip().split(', ')
        mapped_cluster = [node_map[n] for n in cluster]
        # skip clusters with singleton nodes
        print '{}\t1.0\t{}'.format(cl_ix, '\t'.join(mapped_cluster))
        cl_ix += 1

    cf.close()

if __name__ == '__main__':
    main()
