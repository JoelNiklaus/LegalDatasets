#!/bin/bash
#SBATCH --job-name="Scrape"
#SBATCH --mail-user=joel.niklaus@inf.unibe.ch
#SBATCH --mail-type=end,fail
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=15-00:00:00
#SBATCH --mem=256GB
#SBATCH --cpus-per-task=1
#SBATCH --qos=job_epyc2_long
#SBATCH --partition=epyc2

# Put your code below this line

python ejustice.py

# IMPORTANT:
# Run with                  sbatch run_ubelix_job.sh
# check with                squeue --user=jn20t930 --jobs={job_id}
# monitor with              scontrol show --detail jobid {job_id}
# cancel with               scancel {job_id}
# monitor gpu usage with    ssh gnode14 and then nvidia-smi
# run interactive job with  srun --partition=gpu-invest --gres=gpu:rtx3090:1 --mem=64G --time=02:00:00 --pty /bin/bash
