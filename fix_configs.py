import os
import re

TARGETS = ["usa", "china", "japan", "france", "germany", "uk", "spain", "italy"]

for country in TARGETS:
    config_path = f"countries/{country}/config.js"
    if not os.path.exists(config_path):
        continue
        
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()

    unit = "개 도시" if country != "usa" else "개 주"
    name_label = "도시" if country != "usa" else "주"
    all_label = "20대" if country in ["china", "japan", "france"] else "15대"
    all_label = "50개" if country == "usa" else all_label
    all_label = "전체" if country in ["uk", "germany"] else all_label

    if country == 'usa':
        top5_str = f"""        {{
            id: 'top5',
            label: '이지 모드 (핵심 5개 주)',
            dataFiles: {{
                regions: 'countries/usa/states.json',
                provinces: null,
                descriptions: 'countries/usa/descriptions.js',
            }},
            topoConfig: {{
                regions: {{ objectName: 'states' }},
                provinces: null,
            }},
            hierarchy: {{
                hasProvinces: false,
                provinceCodeDigits: 0,
                regionCodeField: 'code', 
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
            topoConfig: {{
                regions: null,
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

    if "modes: [" in content:
        if "'top5'" not in content:
            content = content.replace("modes: [\n", "modes: [\n" + top5_str, 1)
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {country} config.js")
    else:
        if "'top5'" not in content:
            modes_block = f"    // 모드 (난이도) 설정\n    modes: [\n{top5_str}    ],\n\n"
            parts = content.rpartition("provinces: null")
            if parts[1]:
                content = parts[0] + modes_block + "    provinces: null" + parts[2]
                with open(config_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {country} config.js")
            else:
                print(f"Could not find 'provinces: null' in {country}")
