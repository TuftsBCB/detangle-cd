#!/usr/bin/env python
"""
Output clusters in a graph, similar to draw_clusters.py but outputs a
text file rather than an image

"""
import sys
import argparse
import igraph as ig
import io_functions as io

# default to using igraph for graph computation
USE_NETWORKX = 0

# default to using spectral clustering
DEFAULT_ALG = 1

# options for clustering algorithm
SPECTRAL = 1
THRESHOLD = 2
HIERARCHICAL = 3

def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("network_file", help="Original network input file")
    parser.add_argument("dsd_file", help="Distance (i.e. DSD) matrix for network")
    parser.add_argument("-a", "--algorithm", nargs="?", default=DEFAULT_ALG,
                        help="The clustering algorithm to use - 1 for spectral,\
                              2 for threshold clustering, and 3 for simple\
                              shortest-path divisive hierarchical clustering.\
                              Defaults to spectral clustering.")
    parser.add_argument("-c", "--no_conversion", action="store_true")
    parser.add_argument("-d", "--directed", action="store_true",
                        help="Flag specifying if the input represents\
                              a directed graph. Defaults to false.")
    parser.add_argument("-n", "--node_list", nargs="?",
                        help="Optionally specify a list of the nodes in\
                              the DSD file. Default is all the nodes in the\
                              graph.")
    parser.add_argument("-o", "--output_file", nargs="?", default="",
                        help="Optionally specify an output file. Output is to\
                              stdout if no file is specified.")
    parser.add_argument("-p", "--parameter", nargs="?", default='',
                        help="Specify a parameter (i.e. number of clusters,\
                              distance threshold) to be used with clustering\
                              algorithm. If none is provided, a sensible\
                              default is used.")
    parser.add_argument("-s", "--simple_conversion", action="store_true")
    opts = parser.parse_args()

    if USE_NETWORKX:
        import clustering_algs_nx as cl
        # G = io.build_nx_graph_from_matrix(opts.dsd_file, opts.directed)
        G = io.build_nx_graph_from_edgelist(opts.dsd_file, opts.directed)
    else:
        import clustering_algs_ig as cl
        if opts.node_list:
            G = io.build_ig_graph_from_matrix(opts.dsd_file, opts.directed)
        else:
            # G = io.build_ig_graph_from_edgelist(opts.dsd_file, opts.directed)
            # temporary, TODO remove after consensus experiments
            G = ig.Graph.Read_Ncol(opts.dsd_file, directed=opts.directed)

    # nodes = io.get_node_list(opts.node_list) if opts.node_list else []
    if opts.node_list:
        nodes = io.get_node_list(opts.node_list)
    else:
        nodes = zip(*sorted([(v.index, v['name']) for v in G.vs],
                            key=lambda x: x[0]))[1]

    opts.algorithm = int(opts.algorithm)
    if opts.algorithm == SPECTRAL:
        k_val = int(opts.parameter) if opts.parameter else 100
        clusters = cl.spectral_clustering(G, n_clusters=k_val, node_map=nodes,
                                          no_conversion=opts.no_conversion,
                                          simple_conversion=opts.simple_conversion)
    elif opts.algorithm == THRESHOLD:
        filter_weight = float(opts.parameter) if opts.parameter else 5.0
        clusters = cl.threshold_clustering(G, threshold=filter_weight,
                                              node_map=nodes)
    elif opts.algorithm == HIERARCHICAL:
        filter_weight = float(opts.parameter) if opts.parameter else 1.0
        clusters = cl.hierarchical_clustering(G, threshold=filter_weight)
    else:
        sys.exit('Please pick a valid clustering algorithm')

    io.output_clusters(clusters, opts.output_file)


if __name__ == '__main__':
    main()


