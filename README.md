# ProteinFolding

Experiments and tooling around AlphaFold/ColabFold-based protein structure prediction — running predictions on real proteins, visualizing the results in 3D, and animating the folding process for a presentation.

## What's in here

- **`AI_Protein.ipynb`, `AIProteinFoldingV2.ipynb`** — notebooks driving AlphaFold/ColabFold structure predictions.
- **`Display.ipynb`** — renders predicted `.pdb` structures in 3D (via `py3Dmol`) for proteins in `output/` (HIV, Insulin, SARS-CoV-2 Spike, HRV-A, and others).
- **`add_cell.py`, `modify_cell.py`, `restore_cell.py`, `fix_and_modify.py`, `update_label_static.py`** — small helper scripts for programmatically editing `Display.ipynb`'s cells.
- **`Manim/`** — Manim animations visualizing amino acid arrangement and the folding process.
- **`TestImplementation/`** — scratch work on feature extraction from sequence alignments (`.a3m`).
- **`alphafold-decoded/`** — a vendored copy of [AlphaFold Decoded](https://github.com/kilianmandon/alphafold-decoded), an educational from-scratch AlphaFold implementation, kept locally as a learning reference.
- **`Images/`** — diagrams and presentation assets.

## Setup

This repo doesn't track large binaries (model weights, datasets, prediction outputs, videos — see `.gitignore`). To run the notebooks you'll need to provide these locally:

- **`params/`** — AlphaFold model weight files (`params_model_*.npz`), downloaded per the [AlphaFold](https://github.com/google-deepmind/alphafold) / [ColabFold](https://github.com/sokrypton/ColabFold) setup instructions.
- **`data/MNIST/`** — only needed if you're running the unrelated MNIST exercise notebooks.
- **`alphafold`, `colabfold`** — symlinks expecting local `alphafold`/`colabfold` package installs; repoint them to your own environment's `dist-packages` path.

For the AlphaFold-from-scratch tutorials, see `alphafold-decoded/README.md`.
