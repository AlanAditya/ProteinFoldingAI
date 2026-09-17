import sys

pdb_path = "./output/Vriti_SARS_COV2-Spike/test_4f4a4_unrelaxed_rank_001_alphafold2_ptm_model_4_seed_000.pdb"

min_y = float('inf')
max_y = float('-inf')

with open(pdb_path, 'r') as f:
    for line in f:
        if line.startswith("ATOM") or line.startswith("HETATM"):
            try:
                y = float(line[38:46])
                if y < min_y: min_y = y
                if y > max_y: max_y = y
            except ValueError:
                pass

print(f"Min Y: {min_y}")
print(f"Max Y: {max_y}")
