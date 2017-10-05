import igraph as ig
import argparse
import io_functions as io

def print_format(node_list, partition):
        i = 0
        for cluster in partition:
                if len(cluster) < 3:
                        continue
                nodes = "";
                i = i + 1
                for x in cluster:
                        #print x
                        name = node_list[x]
                        nodes = nodes + " " + name
                print str(i) +  " 1.0 " + nodes

def build_clusters(graph, steps):
	partition = graph.community_walktrap(weights = 'weight', steps = steps).as_clustering()

        final_part = []
        i = -1
        for cluster in partition:
                i += 1
                if len(cluster) < 3:
                        continue
                if len(cluster) < 100:
                        final_part.append(cluster)
                if len(cluster) > 100:
                        if steps == 2:
                                final_part.append(cluster)
                        else:
                                part = build_clusters(partition.subgraph(i),steps-1)
                                for x in part:
                                        final_part.append(x)

        return final_part
                        


def main():
	'''
	Prints the modularity of the graph made from the given DSD matrix using the Louvain algorithm to generate clusters

	Usage: python louvain_clustering.py <dsd_file>
	'''

	parser = argparse.ArgumentParser()
	parser.add_argument("dsd_file", help = "Distance (i.e. DSD) matrix for network")
        parser.add_argument("node_list", help = "Node list")
        parser.add_argument("-p", "--ppi",  action = "store_true", help = "Flag specifying if the input is a ppi network. Defaults to false.")
	parser.add_argument("-d", "--directed", action = "store_true", help = "Flag specifying if the input represents a directed graph. Defaults to false.")

	opts = parser.parse_args()
        node_list = io.get_node_list(opts.node_list)
        #print node_list

        if opts.ppi == True:
                G = io.build_ig_graph_from_edgelist(opts.dsd_file)

        else:
                G = io.build_ig_graph_from_matrix(opts.dsd_file)

                '''
                # Remove edges if DSD value is over 3.5
                edges = []
                for edge in G.es:
                        edges.append((edge.tuple[0], edge.tuple[1], edge['weight']))
                edges_to_remove = [(n1, n2) for n1, n2, w in edges if w > 5]        # threshold of 3.5 gives best modularity
                G.delete_edges(edges_to_remove)
                '''
                for edge in G.es:
                        edge['weight'] = 1/edge['weight']


        # the first level seems to have more clusters
        partition = build_clusters(G,4)
	#print(partition)
        #for part in partition:
        #        print part
#        partition = G.community_walktrap(weights = 'weight', steps = 2).as_clustering()

        print_format(node_list, partition)

	# print modularity of clusters
	#print(G.modularity(partition, weights = 'weight'))


if __name__ == '__main__':
    main()
