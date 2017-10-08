#!/bin/sh

mkdir -p clusters

# generate spectral clusters
python ./src/clustering/generate_clusters.py ./data/protein.links.yeast.experiment.txt -a 1 -p 300 -s > ./data/clusters/yeast_ppi_spectral_300.txt
python ./src/clustering/generate_clusters.py ./data/dsd/yeast/yeast_network_0_filtered_4.5.dsd -n ./data/dsd/yeast/yeast_network_0.dsd -a 1 -p 300 -s > ./data/clusters/yeast_dsd_4.5_spectral_300.txt
python ./src/clustering/generate_clusters.py ./data/dsd/yeast/yeast_network_0_filtered_5.dsd -n ./data/dsd/yeast/yeast_network_0.dsd -a 1 -p 300 -s > ./data/clusters/yeast_dsd_5_spectral_300.txt
python ./src/clustering/generate_clusters.py ./data/dsd/yeast/yeast_network_0_filtered_5.5.dsd -n ./data/dsd/yeast/yeast_network_0.dsd -a 1 -p 300 -s > ./data/clusters/yeast_dsd_5.5_spectral_300.txt
python ./src/clustering/generate_clusters.py ./data/dsd/yeast/yeast_network_0_filtered_6.dsd -n ./data/dsd/yeast/yeast_network_0.dsd -a 1 -p 300 -s > ./data/clusters/yeast_dsd_6_spectral_300.txt
python ./src/clustering/generate_clusters.py ./data/dsd/yeast/yeast_network_0_filtered_6.5.dsd -n ./data/dsd/yeast/yeast_network_0.dsd -a 1 -p 300 -s > ./data/clusters/yeast_dsd_6.5_spectral_300.txt

# run clustering recursively to split large clusters
python ./src/clustering/split_clusters.py ./data/protein.links.yeast.experiment.txt ./data/clusters/yeast/yeast_ppi_spectral_300.txt -s > ./data/clusters/yeast/yeast_ppi_spectral_300_split.txt
python ./src/clustering/split_clusters.py ./data/dsd/yeast/yeast_network_0_filtered_4.5.dsd ./data/clusters/yeast/yeast_dsd_4.5_spectral_300.txt -n ./data/dsd/yeast/yeast_network_0_filtered_4.5.nodelist -s > ./data/clusters/yeast/yeast_dsd_4.5_spectral_300_split.txt
python ./src/clustering/split_clusters.py ./data/dsd/yeast/yeast_network_0_filtered_5.dsd ./data/clusters/yeast/yeast_dsd_5_spectral_300.txt -n ./data/dsd/yeast/yeast_network_0_filtered_5.nodelist -s > ./data/clusters/yeast/yeast_dsd_5_spectral_300_split.txt
python ./src/clustering/split_clusters.py ./data/dsd/yeast/yeast_network_0_filtered_5.5.dsd ./data/clusters/yeast/yeast_dsd_5.5_spectral_300.txt -n ./data/dsd/yeast/yeast_network_0_filtered_5.5.nodelist -s > ./data/clusters/yeast/yeast_dsd_5.5_spectral_300_split.txt
python ./src/clustering/split_clusters.py ./data/dsd/yeast/yeast_network_0_filtered_6.dsd ./data/clusters/yeast/yeast_dsd_6_spectral_300.txt -n ./data/dsd/yeast/yeast_network_0_filtered_6.nodelist -s > ./data/clusters/yeast/yeast_dsd_6_spectral_300_split.txt
python ./src/clustering/split_clusters.py ./data/dsd/yeast/yeast_network_0_filtered_6.5.dsd ./data/clusters/yeast/yeast_dsd_6.5_spectral_300.txt -n ./data/dsd/yeast/yeast_network_0_filtered_6.5.nodelist -s > ./data/clusters/yeast/yeast_dsd_6.5_spectral_300_split.txt

# filter small clusters
python ./src/clustering/filter_clusters.py ./data/clusters/yeast/yeast_ppi_spectral_300_split.txt > ./data/clusters/yeast/yeast_ppi_spectral_300_split_filtered.txt
python ./src/clustering/filter_clusters.py ./data/clusters/yeast/yeast_dsd_4.5_spectral_300_split.txt > ./data/clusters/yeast/yeast_dsd_4.5_spectral_300_split_filtered.txt
python ./src/clustering/filter_clusters.py ./data/clusters/yeast/yeast_dsd_5_spectral_300_split.txt > ./data/clusters/yeast/yeast_dsd_5_spectral_300_split_filtered.txt
python ./src/clustering/filter_clusters.py ./data/clusters/yeast/yeast_dsd_5.5_spectral_300_split.txt > ./data/clusters/yeast/yeast_dsd_5.5_spectral_300_split_filtered.txt
python ./src/clustering/filter_clusters.py ./data/clusters/yeast/yeast_dsd_6_spectral_300_split.txt > ./data/clusters/yeast/yeast_dsd_6_spectral_300_split_filtered.txt
python ./src/clustering/filter_clusters.py ./data/clusters/yeast/yeast_dsd_6.5_spectral_300_split.txt > ./data/clusters/yeast/yeast_dsd_6.5_spectral_300_split_filtered.txt
