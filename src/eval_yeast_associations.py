"""
Script for systematically evaluating yeast clustering results for functional
enrichment, using the FuncAssociate API

example URL (get request):
http://llama.mshri.on.ca/cgi/funcassociate/serv?id=0&method=functionate&query=YBR293W+YCL069W+YMR088C&species=Saccharomyces%20cerevisiae&namespace=sgd_systematic

"""
import sys
import time
import argparse
import requests
import httplib
import json
import logging
import traceback

API_BASE_URL = 'http://llama.mshri.on.ca/cgi/funcassociate/serv'
MIN_CL_SIZE = 3
SLEEP_TIME = 2

class FuncAssociate(object):
    """Query funcassociate to find enriched terms"""

    host = 'llama.mshri.on.ca'
    query_url = '/cgi/funcassociate/serv'

    def __init__(self):
        self.c = httplib.HTTPConnection(self.host)

    def close_conn(self):
        self.c.close()

    def jsonify(self, data):
        return (json.dumps(data)).encode('utf-8')

    def request(self, payload):
        self.c.request('POST', self.query_url, self.jsonify(payload),
                headers={'Content-type': 'application/json'})
        response = self.c.getresponse()
        if response.status == httplib.OK: return response.read()

    def available_species(self):
        payload = {'method': 'available_species',
                   'id': 0}
        return self.request(payload)

    def available_namespaces(self, species=['Homo sapiens']):
        payload = {'method': 'available_namespaces',
                   'params': species,
                   'id': 123123123}
        return self.request(payload)

    def go_associations(self,
        params=['Homo sapiens', 'hgnc_symbol',
            ['EXP', 'IDA', 'IPI', 'IMP', 'IGI', 'IEP']
        ]):
        payload = {'method': 'go_associations',
                   'params': params,
                   'id': 1}
        return self.request(payload)

################################################################################
# Functions for getting correctly clustered terms
################################################################################

def assoc_to_map(associations):
    inv_map = {}
    for line in associations:
        if not line[0].startswith('GO:'): continue
        t, gs = line[0], line[1:]
        for g in gs:
            inv_map[g] = inv_map.get(g, [])
            inv_map[g].append(t)
    return inv_map

def get_correct(cluster, terms_enriched, gene_to_term):
    num_correct = 0
    for gene in cluster:
        try:
            gene_terms = gene_to_term[gene]
            correct_terms = set(gene_terms) & set(terms_enriched)
            if correct_terms != set():
                num_correct += 1
        # some genes have no annotations, just skip them
        except KeyError: continue
    return num_correct

def is_enriched(cluster, terms_enriched, filter_above):
    return (len(terms_enriched) > 0 and len(terms_enriched) < filter_above)

def get_node_list(node_file):
    node_list = []
    try:
        fp = open(node_file, 'r')
    except IOError:
        sys.exit('Could not open file: {}'.format(node_file))

    # read the first (i.e. largest) connected component
    cur_line = fp.readline()
    while cur_line and not cur_line.isspace():
        if cur_line and not cur_line.startswith('Component'):
            node_list.append(cur_line.rstrip())
        cur_line = fp.readline()

    fp.close()
    return node_list

def read_clusters(cluster_file):
    try:
        fp = open(cluster_file, 'r')
    except IOError:
        sys.exit('Could not open file: {}'.format(cluster_file))

    clusters = [line.rstrip().split()[2:] for line in fp.readlines()]
    fp.close()
    return clusters

def read_associations(assoc_file, node_list, default_background=False):
    try:
        fp = open(assoc_file, 'r')
    except IOError:
        sys.exit('Could not open file: {}'.format(assoc_file))

    associations = []
    assoc_genes = set()
    unassoc_genes = set()
    attrib_dict = {}
    for line in fp.readlines():
        l = line.rstrip().split('\t')
        try:
            if l[0] == '':
                if default_background:
                    unassoc_genes = set(line.strip().split()).union(node_list - assoc_genes)
                else:
                    unassoc_genes = node_list - assoc_genes
                # other_genes = set(line.strip().split(' ')).union(unassoc_genes)
                associations.append([l[0]] + list(unassoc_genes))
            else:
                # associations.append([l[0]] + l[2].split(' '))
                if default_background:
                    genes = list(set(l[2].split(' ')))
                else:
                    genes = list(set(l[2].split(' ')) & node_list)
                # unassoc_genes.update(set(l[2].split(' ')) - node_list)
                if genes == []: continue
                assoc_genes.update(genes)
                associations.append([l[0]] + genes)
        except IndexError:
            # sys.exit('broken')
            # unassoc_genes = node_list - assoc_genes
            # other_genes = set(line.strip().split(' ')).union(unassoc_genes)
            # associations.append(list(other_genes))
            continue
        if l[0] != '':
            attrib_dict[l[0]] = l[1]
    fp.close()
    return associations, attrib_dict

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cluster_file", help="Cluster results file")
    parser.add_argument("node_list", help="List of node names")
    parser.add_argument('-a', '--association_file', required=False,
                        default=None)
    parser.add_argument('-d', '--default_background', action='store_true')
    parser.add_argument('-f', '--filter_above', type=int, default=0)
    opts = parser.parse_args()
    clusters = read_clusters(opts.cluster_file)
    node_list = get_node_list(opts.node_list)
    if opts.association_file:
        associations, attrib_dict = read_associations(opts.association_file,
                                                      set(node_list),
                                                      opts.default_background)
        '''
        with open('assoc.txt', 'w') as f:
            for assoc in associations:
                f.write('{}\t{}\n'.format(assoc[0], ' '.join(assoc[1:])))
        with open('attrib.txt', 'w') as f:
            f.write(str(attrib_dict))
        exit()
        '''
        gene_to_term = assoc_to_map(associations)
    filtered_clusters = [cl for cl in clusters if len(cl) >= MIN_CL_SIZE]
    enriched_clusters, total_clusters = 0, len(filtered_clusters)
    total_nodes = len(node_list)
    num_enrichments, top_log_odds = 0, 0
    valid_clusters, nodes_enriched = 0, 0
    nodes_correctly_enriched = 0
    bins_all = {}
    bins_enriched = {}
    unused_nodes = sum([len(cl) for cl in clusters if len(cl) < MIN_CL_SIZE])
    over_100s = [len(cl) for cl in clusters if len(cl) > 100]
    for ix, cluster in enumerate(filtered_clusters, 1):
        # print("CLUSTER", cluster)
        # if ix != 141: continue
        cluster_size = len(cluster)
        if cluster_size < MIN_CL_SIZE:
            continue
        power_of_2 = 2**(cluster_size-1).bit_length()
        if power_of_2 in bins_all:
            bins_all[power_of_2] += 1
        else:
            bins_all[power_of_2] = 1
            bins_enriched[power_of_2] = 0
        #clustered_nodes = clustered_nodes + cluster_size

        if opts.association_file:
            data = {
                "id": 0,
                "method":"functionate",
                # "species":"Saccharomyces cerevisiae",
                # "namespace":"sgd_systematic",
                "params": [{
                    "query": cluster,
                    "associations": associations,
                    "attrib_dict": attrib_dict,
                }],
                "jsonrpc":2.0
            }
        else:
            data = {
                "id": 0,
                "method":"functionate",
                "species":"Saccharomyces cerevisiae",
                "namespace":"sgd_systematic",
                "query": ' '.join(cluster),
                "jsonrpc":2.0
            }
        if opts.association_file:
            fa = FuncAssociate()
            response = fa.request(payload=data)
            result_json = json.loads(response)
        else:
            response = requests.get(API_BASE_URL, params=data)
            if response.status_code != 200:
                # this might happen if the cluster is too large, if so it won't
                # count anyway so just skip it
                continue
            result_json = response.json()

        # print 'Cluster {}'.format(ix)
        # print result_json
        if not result_json or 'result' not in result_json or result_json['result'] is None:
            print 'No result for cluster {}'.format(ix)
            '''
            if result_json:
                print result_json
            '''
            continue

        if 'over' in result_json['result']:
            # print result_json['result']
            result = result_json['result']['over']
            '''
            for ann in result:
                print '{}\t{}'.format(ann[-2], ann[-1])
            '''
            if result:
                if opts.filter_above > 0:
                    terms_enriched = [r[6] for r in result]
                    if is_enriched(cluster, terms_enriched, opts.filter_above):
                        enriched_clusters += 1
                        nodes_enriched += len(cluster)
                        correct_nodes = get_correct(cluster,
                                                    terms_enriched,
                                                    gene_to_term)
                        nodes_correctly_enriched += correct_nodes
                        num_enrichments += len(result)
                        bins_enriched[power_of_2] += 1

                else:
                    enriched_clusters += 1
                    nodes_enriched += len(cluster)
                    terms_enriched = [r[6] for r in result]
                    correct_nodes = get_correct(cluster,
                                                terms_enriched,
                                                gene_to_term)
                    nodes_correctly_enriched += correct_nodes
                    num_enrichments += len(result)
                    bins_enriched[power_of_2] += 1

                try:
                    top_log_odds += result[0][3]
                except IndexError:
                    print result
            valid_clusters = valid_clusters + 1
        time.sleep(SLEEP_TIME) # be nice to the API, wait a bit before next request

    ratios = {}

    sorted_be = sorted(bins_enriched.items())
    sorted_ba = sorted(bins_all.items())
    for i in bins_all.keys():
        ratios[i] = bins_enriched[i]/float(bins_all[i])

    print "Number of unused nodes: {}".format(unused_nodes)
    print "Enriched clusters (for p=0.05): {}".format(enriched_clusters)
    print "Total clusters: {}".format(total_clusters)
    print "Valid clusters: {}".format(valid_clusters)
    print "Enrichment ratio: {}".format(enriched_clusters / float(total_clusters))
    print "Nodes placed in an enriched cluster: {}/{} ({:.3f}%)".format(
            nodes_enriched, total_nodes, nodes_enriched / float(total_nodes))
    print "Nodes correctly clustered: {}/{} ({:.3f}%)".format(
            nodes_correctly_enriched, total_nodes,
            nodes_correctly_enriched / float(total_nodes))
    print "Average number of enrichments: {}".format(num_enrichments / float(total_clusters))
    print "Average top log odds score: {}".format(top_log_odds / float(total_clusters))
    print "Enrichment ratio for each cluster size:"
    for i in ratios.keys():
        print "Size: {}".format(i) + " Ratio: {}".format(ratios[i])
    print "total bins: "
    print sorted_ba
    print "enriched clusters: "
    print sorted_be
    print "clusters over 100 nodes: "
    print over_100s

if __name__ == '__main__':
    logging.basicConfig(filename='log.txt', level=20,
                        format="%(asctime)s\n%(message)s")
    try:
        main()
    except Exception:
        logging.error('{}\n{}'.format(' '.join(sys.argv), traceback.format_exc()))
        sys.exit(traceback.format_exc())

    logging.info('{}\n{}\n'.format(' '.join(sys.argv), 'Completed successfully'))
