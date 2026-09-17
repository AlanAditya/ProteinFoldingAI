import json

notebook_path = "/Users/adityadude/Documents/Python/ProteinFolding/Display.ipynb"

with open(notebook_path, 'r') as f:
    nb = json.load(f)

# Get the last cell
last_cell = nb['cells'][-1]

# Define the full correct source
correct_source = [
    "view = show_pdb(\"./output/Vriti_SARS_COV2-Spike/test_4f4a4_unrelaxed_rank_001_alphafold2_ptm_model_4_seed_000.pdb\", show_sidechains, show_mainchains, color)\n",
    "view.spin(True)\n",
    "view.show()\n",
    "from IPython.display import HTML, display\n",
    "display(HTML('<div style=\"text-align:center; font-family:Arial; font-weight:bold; font-size:24px; margin-top:10px;\">SARS-CoV-2 Spike Protein</div>'))"
]

last_cell['source'] = correct_source

with open(notebook_path, 'w') as f:
    json.dump(nb, f, indent=1)
