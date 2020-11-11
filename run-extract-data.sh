#!/bin/bash
#SBATCH --partition standard
#SBATCH --nodes 1
#SBATCH --ntasks-per-node 4
#SBATCH --time 3-00:00:00
#SBATCH --mem 120GB
#SBATCH --job-name data-preprocessing
#SBATCH --output logs/data-preprocess-%J.log

module load python/3.7.3

python extract-data.py
