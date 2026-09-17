import json

notebook_path = "/Users/adityadude/Documents/Python/ProteinFolding/Display.ipynb"

with open(notebook_path, 'r') as f:
    nb = json.load(f)

# Get the last cell
last_cell = nb['cells'][-1]
source = last_cell['source']

new_source = []
for line in source:
    # Remove the 3D label line
    if "view.addLabel" in line:
        continue
    # Keep other lines
    new_source.append(line)

# Add HTML label code at the end
# Check if imports are needed
imports_added = False
for line in new_source:
    if "from IPython.display import" in line and "HTML" in line:
        imports_added = True

html_code = [
    "\n",
    "from IPython.display import HTML, display\n",
    "display(HTML('<div style=\"text-align:center; font-family:Arial; font-weight:bold; font-size:24px; margin-top:10px;\">SARS-CoV-2 Spike Protein</div>'))"
]

new_source.extend(html_code)

last_cell['source'] = new_source

with open(notebook_path, 'w') as f:
    json.dump(nb, f, indent=1)
