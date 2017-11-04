#!/bin/sh

mkdir -p ./data/clusters
mkdir -p ./data/clusters/yeast
mkdir -p ./data/clusters/yeast/louvain/
mkdir -p ./data/clusters/yeast/louvain/over100/
mkdir -p ./data/clusters/yeast/louvain/under100/

# generate louvain over100 clusters
python ./src/clustering/louvain/louvain_clustering.py ./data/protein.links.yeast.experiment.txt ./data/yeast_ppi.nodelist -p > ./data/clusters/yeast/louvain/louvain_output.txt
mv ./trial* ./data/clusters/yeast/louvain/over100/

# generate louvain under100 clusters
python ./src/clustering/louvain/louvain_under100.py ./data/protein.links.yeast.experiment.txt ./data/yeast_ppi.nodelist -p > ./data/clusters/yeast/louvain/louvain_output.txt
mv ./trial* ./data/clusters/yeast/louvain/over100/
