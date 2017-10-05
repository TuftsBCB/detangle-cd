#!/usr/bin/env python
"""
Script for splitting large clusters in a clustering into smaller clusters,
by progressively running spectral clustering with 2 cluster centers (i.e.
finding an approximate min cut)

"""
import sys
import argparse
import logging
import traceback
import igraph as ig
import io_functions as io
import clustering_algs_ig as cl

MAX_CL_SIZE = 100
MAX_STEP = 10

def names_to_ids(G, cluster):
    # map from vertex name to vertex ID in G
    return [v.index for v in G.vs if v["name"] in cluster]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("network_file", help="Network file used for initial\
                                              clustering")
    parser.add_argument("cluster_file", help="Clustering results file")
    parser.add_argument("-c", "--no_conversion", action="store_true")
    parser.add_argument("-d", "--directed", action="store_true",
                        help="Flag specifying if the input represents\
                              a directed graph. Defaults to false.")
    parser.add_argument("-n", "--node_list", nargs="?",
                        help="Optionally specify a list of the nodes in\
                              the DSD file. Default is all the nodes in the\
                              graph.")
    parser.add_argument("-s", "--simple_conversion", action="store_true")
    opts = parser.parse_args()

    if opts.node_list:
        node_list = io.get_node_list(opts.node_list)
    clusters = io.read_clusters(opts.cluster_file)
    if opts.node_list:
        G = io.build_ig_graph_from_matrix(opts.network_file, False, node_list)
    else:
        G = ig.Graph.Read_Ncol(opts.network_file, directed=opts.directed)

    clusters_to_process, final_clusters = [], []
    for cluster in clusters:
        if len(cluster) > MAX_CL_SIZE:
            clusters_to_process.append(cluster)
        else:
            final_clusters.append(cluster)

    # if all nodes have been clustered, stop looping, otherwise continue to
    # recurse on each large cluster
    step = 1
    while clusters_to_process:
        processing = clusters_to_process
        clusters_to_process = []

        for cluster in processing:
            id_cluster = names_to_ids(G, cluster)
            SG = G.subgraph(cluster)

            cluster_size = len(cluster)
            num_clusters = 2
            '''
            num_clusters = (int(cluster_size / float(100)) if cluster_size > 200
                                                           else 2)
            '''
            clusters = cl.spectral_clustering(SG, num_clusters,
                                              no_conversion=opts.no_conversion,
                                              simple_conversion=opts.simple_conversion)
            for cluster in clusters:
                if len(cluster) > MAX_CL_SIZE:
                    clusters_to_process.append([SG.vs[i]['name'] for i in cluster])
                else:
                    final_clusters.append([SG.vs[i]['name'] for i in cluster])
        step += 1

    io.output_clusters(final_clusters, '')

if __name__ == '__main__':
    try:
        main()
    except Exception:
        logging.basicConfig(filename='log.txt',
                            format="%(asctime)s\n%(message)s")
        logging.error('{}\n{}'.format(' '.join(sys.argv), traceback.format_exc()))
        sys.stderr.write(traceback.format_exc())

