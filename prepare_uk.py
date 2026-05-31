import json
import os

translation = {
    "Liverpool": ("리버풀", "비틀즈의 고향이자 역사적인 항구 도시입니다."),
    "Manchester": ("맨체스터", "산업혁명의 중심지이자 유명 축구 클럽들이 있는 도시입니다."),
    "Westminster": ("웨스트민스터", "영국 국회의사당과 빅 벤이 있는 정치의 중심지입니다."),
    "Camden": ("캠든", "다양한 문화와 록 음악, 유명한 마켓이 있는 런던의 자치구입니다."),
    "Greenwich": ("그리니치", "본초 자오선이 지나는 기준점과 천문대가 있는 곳입니다."),
    "Birmingham": ("버밍엄", "영국 제2의 도시로 산업과 상업이 크게 발달했습니다."),
    "Leeds": ("리즈", "금융과 상업이 발달한 요크셔 지방의 중심 도시입니다."),
    "Sheffield": ("셰필드", "철강 산업으로 유명한 잉글랜드 북부의 도시입니다."),
    "Bristol, City of": ("브리스톨", "아름다운 항구와 뱅크시의 그래피티로 유명한 문화 도시입니다."),
    "Nottingham": ("노팅엄", "로빈 후드 전설의 배경이 된 매력적인 도시입니다."),
    "Newcastle upon Tyne": ("뉴캐슬", "타인 강의 아름다운 다리들과 활기찬 밤문화로 유명합니다."),
    "Southampton": ("사우샘프턴", "타이타닉호가 출항했던 역사 깊은 항구 도시입니다."),
    "Oxford": ("옥스퍼드", "세계에서 가장 오래된 대학 중 하나가 있는 '첨탑의 도시'입니다."),
    "Cambridge": ("케임브리지", "캠 강을 따라 세워진 아름다운 대학 건물들이 있는 학문 도시입니다."),
    "York": ("요크", "고대 로마와 바이킹의 역사가 고스란히 남아있는 성곽 도시입니다."),
    "Edinburgh, City of": ("에든버러", "아름다운 에든버러 성이 있는 스코틀랜드의 역사적인 수도입니다."),
    "Glasgow City": ("글래스고", "스코틀랜드 최대 도시로 훌륭한 건축물과 예술로 유명합니다."),
    "Cardiff": ("카디프", "아름다운 성과 활기찬 항만이 있는 웨일스의 수도입니다."),
    "Belfast": ("벨파스트", "타이타닉호가 건조된 조선소가 있는 북아일랜드의 수도입니다."),
    "Dartmouth": ("다트머스", "데번 해안의 아름다운 항구 마을입니다."),
    "South Hams": ("사우스햄스", "다트머스가 위치한 잉글랜드 남서부의 아름다운 지역입니다.")
}

with open('countries/uk/regions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

descriptions = {}

for feature in data['features']:
    eng_name = feature['properties']['LAD13NM']
    if eng_name in translation:
        ko_name, desc = translation[eng_name]
    else:
        # 간단한 음역 또는 그대로 유지
        ko_name = eng_name
        desc = f"{eng_name}, 영국의 아름다운 지역 중 하나입니다."
        
    feature['properties']['name_ko'] = ko_name
    feature['properties']['nativeName'] = eng_name
    feature['properties']['code'] = eng_name
    descriptions[eng_name] = desc

with open('countries/uk/regions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

with open('countries/uk/descriptions.js', 'w', encoding='utf-8') as f:
    f.write("var REGION_DESCRIPTIONS = {\n")
    for k, v in descriptions.items():
        # Escape quotes just in case
        safe_v = v.replace('"', '\\"')
        f.write(f'    "{k}": "{safe_v}",\n')
    f.write("};\n")
