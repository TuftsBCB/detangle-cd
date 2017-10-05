import igraph as ig
import argparse
import io_functions as io
import eval_yeast2 as eval_yeast
import sys
import random
import statistics

def formatx(partition, G, filename):
        i = 0
        clusters = []
        f = open(filename, "write")
        for cluster in partition:
                nodes = "";
                i = i + 1
                clusterx = [G.vs[x]['name'] for x in cluster]
                for x in cluster:
                        #print x
                       # name = node_list[x]
                        nodes = nodes + " " + G.vs[x]['name']
                f.write(str(i) + " 1.0 " + nodes + "\n")
                #clusters.append(clusterx)
        #return clusters

def build_clusters(graph):
	partition = graph.community_multilevel(weights = 'weight', return_levels = True)[0]

        final_part = []
        i = -1
        for cluster in partition:
                i += 1
                #if len(cluster) < 3:
                #        continue
                if len(cluster) < 100:
                        final_part.append(cluster)
                if len(cluster) > 100:
                        if len(partition) == 1:
                                final_part.append(cluster)
                        else:
                                part = build_clusters(partition.subgraph(i))
                                for x in part:
                                        final_part.append(x)

        return final_part
                        

def shuffle(G):
        x = []
        w = []
        for edge in G.adjacent(0):
                y = G.es[edge].tuple
                #print y
                #print G.es[edge]['weight']
                x.append((G.vs[y[0]]['name'], G.vs[y[1]]['name']))  
                w.append(G.es[edge]['weight'])
                      
        name = G.vs[0]['name']
        G.delete_vertices(0)
        G.add_vertex(name)
        G.add_edges(x)
        i = 0
        for edge in G.adjacent(name):
                G.es[edge]['weight'] = w[i]
                #print G.es[edge].tuple
                #print w[i]
                i += 1

        return G


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
                sys.stderr.write("Read in\n")
#                print G.vs['name']

        else:
                G = io.build_ig_graph_from_matrix(opts.dsd_file, node_list = node_list)
                sys.stderr.write("Read in\n")
                for edge in G.es:
                        edge['weight'] = 1/edge['weight']

                sys.stderr.write("flipped edges\n")

        all_info = {}

        all_info['unused_nodes'] = []
        all_info['enriched_clusters'] = []
        all_info['total_clusters'] = []
        all_info['ratio'] = []
        all_info['avg_enrichments'] = []
        all_info['avg_logodds'] = []
        all_info['cluster_sizes'] = []
        all_info['enriched_per_size'] = []

        for repeat in range(0,20):
                sys.stderr.write("starting trial " + str(repeat))
                x = random.randint(0, G.vcount()-1)
                for i in range(1,x):
                        G = shuffle(G)

                sys.stderr.write(": shuffled, ")
                partition = build_clusters(G)
                #partition = G.community_multilevel(weights = 'weight', return_levels = True)[0]

                sys.stderr.write("clustered\n")
                formatx(partition, G, "trial"+str(repeat))
                '''
                eval_yeast.evaluate(clusters)
                print x
                all_info['unused_nodes'].append(x['unused_nodes'])
                all_info['enriched_clusters'].append(x['enriched_clusters'])
                all_info['total_clusters'].append(x['total_clusters'])
                all_info['ratio'].append(x['ratio'])
                all_info['avg_enrichments'].append(x['avg_enrichments'])
                all_info['avg_logodds'].append(x['avg_logodds'])
                all_info['cluster_sizes'].append(x['cluster_sizes'])
                all_info['enriched_per_size'].append(x['enriched_per_size'])
                '''

        '''
        print "MEDIANS:"
        print "Unclustered nodes: " + str(statistics.median(all_info['unused_nodes']))
        print "Enriched_clusters: " + str(statistics.median(all_info['enriched_clusters']))
        print "Total clusters: " + str(statistics.median(all_info['total_clusters']))
        print "Enrichment ratio: " + str(statistics.median(all_info['ratio']))
        print "Avg # of enrichments: " + str(statistics.median(all_info['avg_enrichments']))
        print "Avg top log odds score: " + str(statistics.median(all_info['avg_logodds']))
        print "MEANS:"
        print "Unclustered nodes: " + str(statistics.mean(all_info['unused_nodes']))
        print "Enriched_clusters: " + str(statistics.mean(all_info['enriched_clusters']))
        print "Total clusters: " + str(statistics.mean(all_info['total_clusters']))
        print "Enrichment ratio: " + str(statistics.mean(all_info['ratio']))
        print "Avg # of enrichments: " + str(statistics.mean(all_info['avg_enrichments']))
        print "Avg top log odds score: " + str(statistics.mean(all_info['avg_logodds']))
        '''                                
                #print all_info
        # the first level seems to have more clusters
        #partition = build_clusters(G)

#        print_format(partition, G)


if __name__ == '__main__':
    main()
