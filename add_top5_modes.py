import os
import json
import re

TARGETS = {
    "usa": {"type": "topo", "file": "states.json", "field": "name", "top5": ["California", "New York", "Texas", "Florida", "Washington"]},
    "china": {"type": "geo", "file": "cities.json", "field": "code", "top5": ["PEK", "SHA", "CAN", "SZX", "CKG"]},
    "japan": {"type": "geo", "file": "cities.json", "field": "code", "top5": ["TYO", "OSA", "UKY", "CTS", "FUK"]},
    "france": {"type": "geo", "file": "cities.json", "field": "code", "top5": ["PAR", "MRS", "LYS", "NCE", "BOD"]},
    "germany": {"type": "geo", "file": "cities.json", "field": "code", "top5": ["BER", "MUC", "FRA", "HAM", "CGN"]},
    "uk": {"type": "geo", "file": "cities.json", "field": "code", "top5": ["LON", "MAN", "EDI", "LPL", "GLA"]},
    "spain": {"type": "geo", "file": "cities.json", "field": "code", "top5": ["MAD", "BCN", "VLC", "SVQ", "GRX"]},
    "italy": {"type": "geo", "file": "cities.json", "field": "code", "top5": ["ROM", "MIL", "VCE", "FLR", "NAP"]}
}

for country, info in TARGETS.items():
    filepath = f"countries/{country}/{info['file']}"
    if not os.path.exists(filepath):
        print(f"Skipping {country}, file not found")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if info['type'] == "topo":
        geometries = data['objects']['states']['geometries']
        for geom in geometries:
            val = geom['properties'].get(info['field'])
            geom['properties']['isTop5'] = val in info['top5']
    else:
        features = data['features']
        for feat in features:
            val = feat['properties'].get(info['field'])
            feat['properties']['isTop5'] = val in info['top5']
            
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Updated {country} data.")

    # Now update config.js
    config_path = f"countries/{country}/config.js"
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()

    unit = "개 도시" if country != "usa" else "개 주"
    name_label = "도시" if country != "usa" else "주"
    all_label = "20대" if country in ["china", "japan", "france"] else "15대"
    all_label = "50개" if country == "usa" else all_label
    all_label = "전체" if country == "uk" else all_label

    if country == 'usa':
        top5_str = f"""        {{
            id: 'top5',
            label: '이지 모드 (핵심 5개 주)',
            hierarchy: {{
                hasProvinces: false,
                provinceCodeDigits: 0,
                regionCodeField: 'name', 
                regionNameField: 'name_ko',
                filter: (f) => f.properties.isTop5 === true
            }},
            labels: {{
                sidebarTitle: '미국 핵심 5개 주',
                quizUnit: '주',
                nationwideLabel: '핵심 5개 주',
            }}
        }},
"""
    elif country == 'germany':
        top5_str = f"""        {{
            id: 'top5',
            label: '이지 모드 (핵심 5대 도시)',
            dataFiles: {{
                regions: 'countries/germany/cities.json',
                descriptions: 'countries/germany/cities-descriptions.js',
                provinces: null
            }},
            hierarchy: {{
                hasProvinces: false,
                provinceCodeDigits: 0,
                regionCodeField: 'code', 
                regionNameField: 'name_ko',
                filter: (f) => f.properties.isTop5 === true
            }},
            labels: {{
                sidebarTitle: '독일 핵심 5대 도시',
                quizUnit: '도시',
                nationwideLabel: '핵심 5대 도시',
            }}
        }},
"""
    else:
        top5_str = f"""        {{
            id: 'top5',
            label: '이지 모드 (핵심 5대 {name_label})',
            hierarchy: {{
                hasProvinces: false,
                provinceCodeDigits: 0,
                regionCodeField: 'code', 
                regionNameField: 'name_ko',
                filter: (f) => f.properties.isTop5 === true
            }},
            labels: {{
                sidebarTitle: '핵심 5대 {name_label}',
                quizUnit: '{unit}',
                nationwideLabel: '핵심 5대 {name_label}',
            }}
        }},
        {{
            id: 'all',
            label: '전체 모드 ({all_label} {name_label})',
            hierarchy: {{
                hasProvinces: false,
                provinceCodeDigits: 0,
                regionCodeField: 'code', 
                regionNameField: 'name_ko',
                filter: (f) => f.properties.isQuizRegion === true
            }},
            labels: {{
                sidebarTitle: '{all_label} {name_label}',
                quizUnit: '{unit}',
                nationwideLabel: '{all_label} {name_label}',
            }}
        }}
"""

    if "modes:" in content:
        if "'top5'" not in content:
            # Inject top5 at the beginning of the modes array
            content = content.replace("modes: [\n", "modes: [\n" + top5_str)
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(content)
    else:
        # We need to add the modes array before provinces: null
        modes_block = f"    // 모드 (난이도) 설정\n    modes: [\n{top5_str}    ],\n\n"
        content = content.replace("provinces: null", modes_block + "    provinces: null")
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(content)

    print(f"Updated {country} config.js")
