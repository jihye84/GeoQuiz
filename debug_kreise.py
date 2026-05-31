import json

with open('countries/germany/kreise.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

names = []
for feature in data['features']:
    names.append(f"{feature['properties'].get('NAME_3', '')} ({feature['properties'].get('TYPE_3', '')})")

with open('all_kreise.txt', 'w', encoding='utf-8') as f:
    for n in sorted(names):
        f.write(n + '\n')
