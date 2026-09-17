import json

notebook_path = "/Users/adityadude/Documents/Python/ProteinFolding/Display.ipynb"

with open(notebook_path, 'r') as f:
    notebook = json.load(f)

new_cell = {
 "cell_type": "code",
 "execution_count": None,
 "metadata": {},
 "outputs": [],
 "source": [
  "view = show_pdb(\"./output/Vriti_SARS_COV2-Spike/test_4f4a4_unrelaxed_rank_001_alphafold2_ptm_model_4_seed_000.pdb\", show_sidechains, show_mainchains, color)\n",
  "view.spin(True)\n",
  "view.addLabel(\"SARS-CoV-2 Spike Protein\", {\"position\": {\"x\":0, \"y\":0, \"z\":0}, \"backgroundColor\": \"white\", \"fontColor\": \"black\"})\n",
  "view.show()"
 ]
}

notebook['cells'].append(new_cell)

with open(notebook_path, 'w') as f:
    json.dump(notebook, f, indent=1)
