#!/usr/bin/env bash

# --------------------------
# Fixed base arguments
# --------------------------
POP_SIZE=50
K=10
NUM_TRIANGLES=10
NUM_GENERATIONS=200

# --------------------------
# Parameter arrays
# --------------------------
sel_meth=("roulette" "ranking" "tournament_deterministic" \
          "tournament_probabilistic" "universal" "elitist" \
          "boltzmann")

cross_meth=("one_point" "two_point" "uniform" "one_point_fake")
mut_meth=("basic" "uniform" "limited" "complete")
rep_strat=("traditional" "generational" "steady_state")

# --------------------------
# Nested loops for all combos
# --------------------------
source env/bin/activate #activate virtual environment
for sel in "${sel_meth[@]}"; do
  for gen_sel in "${sel_meth[@]}"; do        # generation_selection_method repeats selection list
    for cross in "${cross_meth[@]}"; do
      for mut in "${mut_meth[@]}"; do
        for rep in "${rep_strat[@]}"; do

          echo "Running: sel=$sel gen_sel=$gen_sel cross=$cross mut=$mut rep=$rep"

          python main.py new \
            "$POP_SIZE" \
            "$K" \
            "$NUM_TRIANGLES" \
            "$NUM_GENERATIONS" \
            "$sel" \
            "$gen_sel" \
            "$cross" \
            "$mut" \
            "$rep"

        done
      done
    done
  done
done
