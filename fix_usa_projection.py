import urllib.request
import json
import os

# 1. Load existing projected states.json to get properties mapping
existing_path = 'countries/usa/states.json'
with open(existing_path, 'r', encoding='utf-8') as f:
    existing_data = json.load(f)

props_map = {}
for geom in existing_data['objects']['states']['geometries']:
    name = geom['properties'].get('name')
    if name:
        props_map[name] = geom['properties']

# 2. Download unprojected states-10m.json
url = "https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json"
req = urllib.request.urlopen(url)
unprojected_data = json.loads(req.read())

# 3. Merge properties
for geom in unprojected_data['objects']['states']['geometries']:
    name = geom['properties'].get('name')
    if name in props_map:
        # Update with existing properties like name_ko, code
        geom['properties'].update(props_map[name])
    else:
        # Fallback if missing
        geom['properties']['code'] = name
        geom['properties']['name_ko'] = name

# 4. Save unprojected TopoJSON back to states.json
with open(existing_path, 'w', encoding='utf-8') as f:
    json.dump(unprojected_data, f, ensure_ascii=False)

print("Successfully replaced states.json with UNPROJECTED coordinates while keeping name_ko.")
