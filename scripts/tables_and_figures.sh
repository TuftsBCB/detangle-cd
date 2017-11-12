mkdir -p ./figures
python ./src/plot_cluster_dist.py ./data/clusters/louvain/under100/under100_ppi_median.txt ./data/clusters/louvain/under100_f5_0_median.txt -n Louvain -o ./figures/louvain.pdf
python ./src/plot_cluster_dist.py ./data/clusters/walktrap/p300_no_recursion_enrichment.txt /data/clusters/walktrap/dsd_5_5_p300_enrichment.txt -n Walktrap -o ./figures/walktrap.pdf
python ./src/plot_cluster_dist.py ./data/clusters/spectral/spectral_ppi_split_filtered.txt ./data/clusters/spectral/spectral_f5_5_split_filtered.txt -n Spectral -o ./figures/spectral.pdf
