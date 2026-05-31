import os
import json
import urllib.request

country = "spain"
base_map_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/spain-provinces.geojson"

cities_data = [
    {"code": "MAD", "name_ko": "마드리드", "lat": 40.4168, "lon": -3.7038, "desc": "프라도 미술관과 레알 마드리드로 유명한 스페인의 웅장한 수도예요."},
    {"code": "BCN", "name_ko": "바르셀로나", "lat": 41.3851, "lon": 2.1734, "desc": "가우디의 걸작 사그라다 파밀리아가 있는 지중해 최고의 관광 도시예요."},
    {"code": "VLC", "name_ko": "발렌시아", "lat": 39.4699, "lon": -0.3763, "desc": "파에야의 본고장이자 미래지향적인 예술과 과학의 도시가 있는 곳이에요."},
    {"code": "SVQ", "name_ko": "세비야", "lat": 37.3891, "lon": -5.9845, "desc": "정열적인 플라멩코와 투우의 중심지이자 안달루시아의 심장이에요."},
    {"code": "ZAZ", "name_ko": "사라고사", "lat": 41.6488, "lon": -0.8891, "desc": "마드리드와 바르셀로나 사이에 위치한 역사적인 로마 시대 도시예요."},
    {"code": "AGP", "name_ko": "말라가", "lat": 36.7213, "lon": -4.4214, "desc": "천재 화가 피카소의 고향이자 햇살 가득한 코스타 델 솔의 중심이에요."},
    {"code": "MUR", "name_ko": "무르시아", "lat": 37.9922, "lon": -1.1307, "desc": "비옥한 농경지와 따뜻한 기후로 '유럽의 과수원'이라 불리는 도시예요."},
    {"code": "PMI", "name_ko": "팔마", "lat": 39.5696, "lon": 2.6502, "desc": "지중해의 아름다운 마요르카 섬에 위치한 눈부신 휴양 도시예요."},
    {"code": "LPA", "name_ko": "라스팔마스", "lat": 28.1235, "lon": -15.4363, "desc": "아프리카 해안선 근처에 위치한 따뜻하고 평화로운 카나리아 제도의 도시예요."},
    {"code": "BIO", "name_ko": "빌바오", "lat": 43.2630, "lon": -2.9350, "desc": "구겐하임 미술관이 쇠퇴하던 공업 도시를 문화의 도시로 바꾼 기적의 장소예요."},
    {"code": "ALC", "name_ko": "알리칸테", "lat": 38.3452, "lon": -0.4810, "desc": "아름다운 코스타 블랑카(흰 해안)의 푸른 바다와 성곽이 있는 항구예요."},
    {"code": "ODB", "name_ko": "코르도바", "lat": 37.8882, "lon": -4.7794, "desc": "거대한 이슬람 사원인 메스키타가 남아있는 찬란했던 이슬람 문화의 중심지예요."},
    {"code": "GRX", "name_ko": "그라나다", "lat": 37.1773, "lon": -3.5986, "desc": "이슬람 건축의 최고봉 알함브라 궁전이 신비롭게 자리 잡은 안달루시아 도시예요."},
    {"code": "TLD", "name_ko": "톨레도", "lat": 39.8628, "lon": -4.0273, "desc": "마드리드 이전의 옛 수도로, 중세 시대의 모습이 그대로 멈춰있는 마법 같은 도시예요."},
    {"code": "SCQ", "name_ko": "산티아고 데 콤포스텔라", "lat": 42.8782, "lon": -8.5448, "desc": "수많은 순례자들이 걸어가는 '산티아고 순례길'의 장엄한 종착지예요."}
]

os.makedirs(f"countries/{country}", exist_ok=True)

print("Downloading base map for Spain...")
urllib.request.urlretrieve(base_map_url, f"countries/{country}/regions.json")

print("Generating data for Spain...")
features = []
descriptions = []

for city in cities_data:
    features.append({
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
    })
    descriptions.append(f'    "{city["code"]}": "{city["desc"]}"')

geojson = {"type": "FeatureCollection", "features": features}
with open(f"countries/{country}/cities.json", "w", encoding="utf-8") as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)

var_name = "SPAIN_CITIES_DESCRIPTIONS"
desc_content = f"var {var_name} = {{\n" + ",\n".join(descriptions) + f"\n}};\n\nif (typeof REGION_DESCRIPTIONS !== 'undefined') {{\n    Object.assign(REGION_DESCRIPTIONS, {var_name});\n}} else {{\n    var REGION_DESCRIPTIONS = {var_name};\n}}\n"

with open(f"countries/{country}/descriptions.js", "w", encoding="utf-8") as f:
    f.write(desc_content)

print("Done preparing Spain data.")
