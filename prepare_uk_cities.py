import json

cities_data = [
    {"code": "LON", "name_ko": "런던", "lat": 51.5074, "lon": -0.1278, "desc": "빅 벤, 타워 브릿지 등 수많은 랜드마크가 있는 영국의 수도예요."},
    {"code": "EDI", "name_ko": "에든버러", "lat": 55.9533, "lon": -3.1883, "desc": "산 위에 우뚝 솟은 에든버러 성과 중세 거리가 아릅다운 스코틀랜드의 수도예요."},
    {"code": "MAN", "name_ko": "맨체스터", "lat": 53.4808, "lon": -2.2426, "desc": "산업혁명의 중심지이자 세계적인 두 축구팀의 연고지예요."},
    {"code": "LIV", "name_ko": "리버풀", "lat": 53.4084, "lon": -2.9916, "desc": "전설적인 밴드 비틀즈가 탄생한 매력적인 항구 도시예요."},
    {"code": "GLA", "name_ko": "글래스고", "lat": 55.8642, "lon": -4.2518, "desc": "켈빈그로브 미술관 등 풍부한 문화를 자랑하는 스코틀랜드 최대의 경제 도시예요."},
    {"code": "CDF", "name_ko": "카디프", "lat": 51.4816, "lon": -3.1791, "desc": "웨일스의 중심지로, 카디프 성과 활기찬 항구가 있는 수도예요."},
    {"code": "BFS", "name_ko": "벨파스트", "lat": 54.5973, "lon": -5.9301, "desc": "비운의 여객선 타이타닉이 건조된 곳이자 북아일랜드의 수도예요."},
    {"code": "OXF", "name_ko": "옥스퍼드", "lat": 51.7520, "lon": -1.2577, "desc": "아름다운 첨탑의 도시이자 영어권에서 가장 오래된 명문 대학이 있는 곳이에요."},
    {"code": "CAM", "name_ko": "케임브리지", "lat": 52.2053, "lon": 0.1218, "desc": "수많은 노벨상 수상자를 배출한 케임브리지 대학교가 있는 조용한 도시예요."},
    {"code": "BHX", "name_ko": "버밍엄", "lat": 52.4862, "lon": -1.8904, "desc": "수많은 운하를 가진 잉글랜드 중부의 대표적인 제2의 도시예요."},
    {"code": "YOR", "name_ko": "요크", "lat": 53.9590, "lon": -1.0815, "desc": "웅장한 고딕 성당인 요크 민스터와 바이킹의 역사를 간직한 중세 도시예요."},
    {"code": "STH", "name_ko": "스톤헨지", "lat": 51.1789, "lon": -1.8262, "desc": "누가, 왜 지었는지 아직도 미스터리인 세계적인 고대 거석 유적지예요."},
    {"code": "BTH", "name_ko": "바스", "lat": 51.3758, "lon": -2.3599, "desc": "2천 년 전 고대 로마인들이 만든 대형 공중 목욕탕 유적이 보존된 아름다운 도시예요."},
    {"code": "SHF", "name_ko": "셰필드", "lat": 53.3811, "lon": -1.4701, "desc": "과거 세계 최고 품질의 철강을 생산했던 강인하고 푸른 철강 도시예요."},
    {"code": "BRS", "name_ko": "브리스틀", "lat": 51.4545, "lon": -2.5879, "desc": "유명한 거리 예술가 뱅크시의 고향이자 영국의 주요 무역 항구 도시예요."}
]

features = []
descriptions = []

for city in cities_data:
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [city["lon"], city["lat"]]
        },
        "properties": {
            "code": city["code"],
            "name_ko": city["name_ko"],
            "isQuizRegion": True
        }
    }
    features.append(feature)
    
    desc_str = f'    "{city["code"]}": "{city["desc"]}"'
    descriptions.append(desc_str)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

with open("countries/uk/cities.json", "w", encoding="utf-8") as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)

desc_file_content = "var UK_CITIES_DESCRIPTIONS = {\n" + ",\n".join(descriptions) + "\n};\n\nif (typeof REGION_DESCRIPTIONS !== 'undefined') {\n    Object.assign(REGION_DESCRIPTIONS, UK_CITIES_DESCRIPTIONS);\n} else {\n    var REGION_DESCRIPTIONS = UK_CITIES_DESCRIPTIONS;\n}\n"

with open("countries/uk/descriptions.js", "w", encoding="utf-8") as f:
    f.write(desc_file_content)

print("Generated countries/uk/cities.json and descriptions.js")
