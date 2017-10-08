#!/bin/sh

mkdir -p clusters

# generate walktrap clusters
python ./src/clustering/walktrap_clustering.py ./data/protein.links.yeast.experiment.txt -p > ./data/clusters/yeast_ppi_wt.txt
python ./src/clustering/walktrap_clustering.py ./data/dsd/yeast/yeast_network_0_filtered_4.dsd -n ./data/dsd/yeast/yeast_network_0_filtered_4.nodelist > ./data/clusters/yeast_dsd_4_spectral.txt
python ./src/clustering/walktrap_clustering.py ./data/dsd/yeast/yeast_network_0_filtered_4.5.dsd -n ./data/dsd/yeast/yeast_network_0_filtered_4.5.nodelist > ./data/clusters/yeast_dsd_4.5_spectral.txt
python ./src/clustering/walktrap_clustering.py ./data/dsd/yeast/yeast_network_0_filtered_5.dsd -n ./data/dsd/yeast/yeast_network_0_filtered_5.nodelist > ./data/clusters/yeast_dsd_5_spectral.txt
python ./src/clustering/walktrap_clustering.py ./data/dsd/yeast/yeast_network_0_filtered_5.5.dsd -n ./data/dsd/yeast/yeast_network_0_filtered_5.5.nodelist > ./data/clusters/yeast_dsd_5.5_spectral.txt
python ./src/clustering/walktrap_clustering.py ./data/dsd/yeast/yeast_network_0_filtered_6.dsd -n ./data/dsd/yeast/yeast_network_0_filtered_6.nodelist > ./data/clusters/yeast_dsd_6_spectral.txt

# generate modified walktrap clusters
# because we're working directly from c++ source, this has a few steps

