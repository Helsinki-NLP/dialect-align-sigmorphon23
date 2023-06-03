#! /bin/bash -l

#SBATCH -J eval
#SBATCH -o log_eval.%j.out
#SBATCH -e log_eval.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 6
#SBATCH --mem-per-cpu=1G
#SBATCH -A project_2005047
#SBATCH -t 5:00:00

module load parallel

# parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh "eflomal" {} ::: fwd rev isc uni gdf gdfa

# parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh "fastalign" {} ::: fwd rev isc uni gdf gdfa

# parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh "eflomal_corpus_priors" {} ::: fwd rev isc uni gdf gdfa

# parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh "giza" {} ::: fwd rev isc uni gdf gdfa

# parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh "leven" {} ::: fwd rev isc uni gdfa

# parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh "leven/aai" {} ::: fwd rev isc uni gdfa

# parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh "leven_corpus_pmi" {} ::: fwd rev isc uni gdfa

# parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh "leven_corpus_pmi/aai" {} ::: fwd rev isc uni gdfa

# parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh "m2m_max11_delXY" {} ::: fwd rev isc uni gdfa

# parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh "m2m_max11_delXY/aai" {} ::: fwd rev isc uni gdfa

parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh "m2m_max22_delXY_eqmap" {} ::: fwd rev isc uni gdfa

########################################

#parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh {} "sym" ::: eflomal eflomal_corpus_priors eflomal_leven_priors

# parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh {} "fwd" ::: m2m_max22 m2m_max22_delXY m2m_max22_delXY_eqmap m2m_max22_eqmap

#parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh "leven" {} ::: fwd fwd+aai rev rev+aai sym sym+aai

#parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh {} "fwd+aai" ::: leven_corpus_pmi leven_doc_pmi leven_swap m2m_max11_delXY m2m_max11_delXY_init

#parallel -j $SLURM_CPUS_PER_TASK source evaluate_exp.sh "m2m_asym_max21_max12_delXY" {} ::: fwd rev sym
