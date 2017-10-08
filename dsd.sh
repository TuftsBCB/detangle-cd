#!/bin/sh

mkdir -p ./data/dsd

# generate yeast DSD matrix
mkdir -p ./data/dsd/yeast
python ./src/dsd_gen.py ./data/protein.links.yeast.experiment.txt -o ./data/dsd/yeast/yeast_network

# generate human DSD matrix, will take longer
mkdir -p ./data/dsd/human
python ./src/dsd_gen.py ./data/protein.links.human.experiment.txt -o ./data/dsd/human/human_network

# generate filtered yeast DSD matrices
./src/filter_distances.py ./data/dsd/yeast/yeast_network_0.dsd -t 4 > ./data/dsd/yeast/yeast_network_0_filtered_4.dsd
./src/filter_distances.py ./data/dsd/yeast/yeast_network_0.dsd -t 4.5 > ./data/dsd/yeast/yeast_network_0_filtered_4.5.dsd
./src/filter_distances.py ./data/dsd/yeast/yeast_network_0.dsd -t 5 > ./data/dsd/yeast/yeast_network_0_filtered_5.dsd
./src/filter_distances.py ./data/dsd/yeast/yeast_network_0.dsd -t 5.5 > ./data/dsd/yeast/yeast_network_0_filtered_5.5.dsd
./src/filter_distances.py ./data/dsd/yeast/yeast_network_0.dsd -t 6 > ./data/dsd/yeast/yeast_network_0_filtered_6.dsd
./src/filter_distances.py ./data/dsd/yeast/yeast_network_0.dsd -t 6.5 > ./data/dsd/yeast/yeast_network_0_filtered_6.5.dsd

# generate filtered human DSD matrices
./src/filter_distances.py ./data/dsd/human/human_network_0.dsd -t 6 > ./data/dsd/human/human_network_0_filtered_6.dsd
./src/filter_distances.py ./data/dsd/human/human_network_0.dsd -t 6.5 > ./data/dsd/human/human_network_0_filtered_6.5.dsd
./src/filter_distances.py ./data/dsd/human/human_network_0.dsd -t 7 > ./data/dsd/human/human_network_0_filtered_7.dsd
./src/filter_distances.py ./data/dsd/human/human_network_0.dsd -t 7.5 > ./data/dsd/human/human_network_0_filtered_7.5.dsd
./src/filter_distances.py ./data/dsd/human/human_network_0.dsd -t 8 > ./data/dsd/human/human_network_0_filtered_8.dsd


