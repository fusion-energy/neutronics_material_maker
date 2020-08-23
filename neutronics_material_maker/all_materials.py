# Reads in materials from all json files in data folder and creates single
# dictionary with no repeat entries

import os
import json
from pathlib import Path

material_dict = {}

for filename in Path(Path(__file__).parent / "data").glob("*.json"):
    with open(os.path.join("data", filename), "r") as f:
        new_data = json.load(f)
        material_dict.update(new_data)

print("Available materials", sorted(list(material_dict.keys())))
