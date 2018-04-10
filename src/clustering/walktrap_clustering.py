''' 
unused script to run the walktrap algorithm
If you want to use this you have to fix the igraph.subgraph bug (this bug is fixed in louvain_under100.py so follow that example)

'''
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

def format2(cluster, G):
        nodes = ""
        for x in cluster:
                nodes = nodes + " " + G.vs[x]["name"]
        nodes = " 1.0 " + nodes + "\n"
        return nodes

def build_clusters(graph, steps):
	partition = graph.community_walktrap(weights = 'weight', steps = steps).as_clustering()

        final_part = []
        i = -1
        for cluster in partition:
                i += 1
                #if len(cluster) < 3:
                #        continue
                if len(cluster) <= 100:
                        final_part.append(format2(cluster, graph))
                if len(cluster) > 100:
                        if len(partition) == 1:
                                final_part.append(format2(cluster, graph))
                        elif steps == 1:
                                final_part.append(format2(cluster, graph))
                        else:
                                print "Spliting a cluster"
                                subG = partition.subgraph(i)
#                                print subG.vs["name"]
                                part = build_clusters(subG, steps-1)
                                for c in part:
                                        final_part.append(c)
                                        
        return final_part
'''
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
                        

'''
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
                G = io.build_ig_graph_from_matrix(opts.dsd_file, node_list = node_list)

                #for edge in G.es:
                #        edge['weight'] = 1/edge['weight']


        # the first level seems to have more clusters
        partition = build_clusters(G,4)
	#print(partition)
        #for part in partition:
        #        print part
        #        partition = G.community_walktrap(weights = 'weight', steps = 2).as_clustering()
        f = open("trial", "w")
        i = 0
        for line in partition:
                f.write(str(i) + line)
                i += 1

        #print_format(node_list, partition)

	# print modularity of clusters
	#print(G.modularity(partition, weights = 'weight'))


if __name__ == '__main__':
    main()
