#!/bin/sh

mkdir -p ./data/clusters
<<<<<<< HEAD
mkdir -p ./data/clusters/louvain/
mkdir -p ./data/clusters/louvain/over100/
mkdir -p ./data/clusters/louvain/under100/
=======
mkdir -p ./data/clusters/yeast
mkdir -p ./data/clusters/yeast/louvain/
mkdir -p ./data/clusters/yeast/louvain/over100/
mkdir -p ./data/clusters/yeast/louvain/under100/
>>>>>>> 71b2e258c6c5d0be3af37177b59af42a6a2b70ee

# generate louvain over100 clusters
python ./src/clustering/louvain/louvain_clustering.py ./data/protein.links.yeast.experiment.txt ./data/yeast_ppi.nodelist -p > ./data/clusters/yeast/louvain/louvain_output.txt
mv ./trial* ./data/clusters/yeast/louvain/over100/

# generate louvain under100 clusters
python ./src/clustering/louvain/louvain_under100.py ./data/protein.links.yeast.experiment.txt ./data/yeast_ppi.nodelist -p > ./data/clusters/yeast/louvain/louvain_output.txt
mv ./trial* ./data/clusters/yeast/louvain/under100/
