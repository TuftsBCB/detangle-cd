# detangle-cd

Code for Hall-Swan et al. 2017, "Detangling PPI networks to uncover functionally meaningful clusters".

## Requirements

Many scripts in this repository require `numpy`, `pandas`, and any recent version of `scikit-learn`.

Running our implementations of spectral clustering and Louvain clustering require the Python igraph package: `pip install python-igraph` or `conda install -c conda-forge python-igraph`.

## Reproducing Experiments

All of the scripts should be run from the repo root.

To run DSD on the yeast network, and generate the filtered DSD matrices: `./scripts/dsd.sh`

To run (spectral|walktrap|Louvain) clustering: `./scripts/clusters_(spectral|wt|louvain).sh`

To calculate GO term enrichment (using the method described in the paper) for the generated clusters: `./scripts/calc_enrichment.sh`

To generate tables and figures from enrichment results: `./scripts/tables_and_figures.sh`

### Note

This repository is mostly for purposes of reproducing the experiments and results in the above paper. I'll try to respond to any issues posted on the GitHub issue tracker, but I won't be actively maintaining or adding functionality to the repo.

