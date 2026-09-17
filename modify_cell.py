import json

notebook_path = "/Users/adityadude/Documents/Python/ProteinFolding/Display.ipynb"

with open(notebook_path, 'r') as f:
    nb = json.load(f)

# Get the last cell
last_cell = nb['cells'][-1]
source = last_cell['source']

new_source = []
for line in source:
    if "view.addLabel" in line:
        # Update styling and position
        # Position: (0, -50, 0) -> Center bottom (assuming Y rotation)
        # Font size: 24 -> Slightly bigger
        # Font: Arial -> Better font
        # Background: White, Font Color: Black
        new_line = 'view.addLabel("SARS-CoV-2 Spike Protein", {"position": {"x":0, "y":-50, "z":0}, "backgroundColor": "white", "fontColor": "black", "fontSize": 24, "font": "Arial"})\n'
        new_source.append(new_line)
    else:
        new_source.append(line)

last_cell['source'] = new_source

with open(notebook_path, 'w') as f:
    json.dump(nb, f, indent=1)
