
# Reads in materials from all json files in data folder and creates single dictionary with no repeat entries

import os
import json

all_materials_dict = {}

materials_files = [
    pos_json for pos_json in os.listdir("data") if pos_json.endswith(".json")
]

for filename in materials_files:
    with open(os.path.join("data", filename), "r") as f:
        new_data = json.load(f)
        all_materials_dict.update(new_data)
