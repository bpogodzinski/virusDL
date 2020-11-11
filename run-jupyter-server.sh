#!/bin/bash
#SBATCH --partition standard
#SBATCH --nodes 1
#SBATCH --ntasks-per-node 1
#SBATCH --time 2-00:00:00
#SBATCH --job-name jupyter-notebook-server
#SBATCH --output jupyter-notebook-%J.log

port=8000
node=$(hostname -s)
user=$(whoami)

echo -e "
Create tunnel using:
ssh -Nf -L ${port}:${node}:${port} ${user}@eagle.man.poznan.pl

Use a Browser on your local machine to go to:
localhost:${port}
"

module load python/3.7.3
jupyter notebook --no-browser --port=${port} --ip=0.0.0.0
