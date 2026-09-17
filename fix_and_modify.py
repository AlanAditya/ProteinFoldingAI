import json

notebook_path = "/Users/adityadude/Documents/Python/ProteinFolding/Display.ipynb"

with open(notebook_path, 'r') as f:
    nb = json.load(f)

# Remove trailing empty cells
removed_count = 0
while len(nb['cells']) > 0 and (not nb['cells'][-1]['source'] or len(nb['cells'][-1]['source']) == 0):
    nb['cells'].pop()
    removed_count += 1
print(f"Removed {removed_count} empty trailing cells.")

if len(nb['cells']) == 0:
    print("Notebook is empty!")
    exit(1)

# Modify the last cell (which should be the visualization cell)
last_cell = nb['cells'][-1]
source = last_cell['source']

new_source = []
modified = False
for line in source:
    if "view.addLabel" in line:
        # Update styling and position
        # Position: (0, -50, 0)
        # Font size: 24
        # Font: Arial
        # inFront: True (ensure visibility)
        new_line = 'view.addLabel("SARS-CoV-2 Spike Protein", {"position": {"x":0, "y":-50, "z":0}, "backgroundColor": "white", "fontColor": "black", "fontSize": 24, "font": "Arial", "inFront": True})\n'
        new_source.append(new_line)
        modified = True
    else:
        new_source.append(line)

if modified:
    last_cell['source'] = new_source
    print("Modified label in the last cell.")
else:
    print("Could not find view.addLabel in the last cell!")
    # Checking source content
    print("Source content:", source)

with open(notebook_path, 'w') as f:
    json.dump(nb, f, indent=1)
