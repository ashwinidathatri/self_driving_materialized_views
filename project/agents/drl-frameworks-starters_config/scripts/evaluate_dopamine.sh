source ~/miniconda3/etc/profile.d/conda.sh

echo "--- STARTING DOPAMINE EXPERIMENTS ---"
conda activate dopamine-env
echo
echo "--- STARTING DOPAMINE CARTPOLE EXPERIMENTS ---"
mkdir -p results/dbse/runtime
echo
for fullfile in experiments/dbse/dopamine/*.gin; do 
    filename=$(basename -- "$fullfile")
    experiment="${filename%.*}"
    echo "--- STARTING EXPERIMENT ${experiment} --- "
    #bash ./scripts/clean_caches.sh
    python src/dopamine/run_evaluation.py --base_dir="results/dbse/" --gin_files="experiments/dbse/dopamine/${experiment}.gin"
    echo "--- EXPERIMENT ${experiment} COMPLETED --- "
    echo
done
echo "--- DOPAMINE CARTPOLE EXPERIMENTS COMPLETED ---"
echo
echo "--- DOPAMINE EXPERIMENTS COMPLETED ---"
echo
