import os
import json
import urllib.request

country = "italy"
base_map_url = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson"

cities_data = [
    {"code": "ROM", "name_ko": "로마", "lat": 41.9028, "lon": 12.4964, "desc": "콜로세움과 바티칸을 품고 있는 영원한 제국 이탈리아의 수도예요."},
    {"code": "MIL", "name_ko": "밀라노", "lat": 45.4642, "lon": 9.1900, "desc": "화려한 두오모 성당이 있는 세계적인 패션과 경제의 중심지예요."},
    {"code": "VCE", "name_ko": "베네치아", "lat": 45.4408, "lon": 12.3155, "desc": "아름다운 운하 위로 곤돌라가 떠다니는 낭만적인 물의 도시예요."},
    {"code": "FLR", "name_ko": "피렌체", "lat": 43.7696, "lon": 11.2558, "desc": "르네상스 예술이 찬란하게 피어난 우피치 미술관이 있는 낭만의 도시예요."},
    {"code": "NAP", "name_ko": "나폴리", "lat": 40.8518, "lon": 14.2681, "desc": "세계 3대 미항이자 쫄깃한 마르게리타 피자의 본고장이에요."},
    {"code": "GOA", "name_ko": "제노바", "lat": 44.4056, "lon": 8.9463, "desc": "콜럼버스의 고향이자 과거 지중해 무역을 호령했던 거대한 항구 도시예요."},
    {"code": "TRN", "name_ko": "토리노", "lat": 45.0703, "lon": 7.6869, "desc": "알프스 산맥 아래에 위치한 초콜릿과 피아트 자동차로 유명한 도시예요."},
    {"code": "BLQ", "name_ko": "볼로냐", "lat": 44.4949, "lon": 11.3426, "desc": "유럽에서 가장 오래된 대학이 있으며, 미식의 수도로 불리는 붉은 도시예요."},
    {"code": "VRN", "name_ko": "베로나", "lat": 45.4384, "lon": 10.9916, "desc": "로미오와 줄리엣의 아름다운 사랑 이야기가 숨 쉬는 낭만적인 도시예요."},
    {"code": "PMO", "name_ko": "팔레르모", "lat": 38.1157, "lon": 13.3615, "desc": "지중해 최대의 섬인 시칠리아의 다채로운 역사를 간직한 중심지예요."},
    {"code": "CTA", "name_ko": "카타니아", "lat": 37.5079, "lon": 15.0830, "desc": "웅장하게 연기를 뿜어내는 에트나 화산 아래에 자리 잡은 시칠리아 제2의 도시예요."},
    {"code": "CAG", "name_ko": "칼리아리", "lat": 39.2238, "lon": 9.1116, "desc": "에메랄드빛 바다를 자랑하는 아름다운 사르데냐 섬의 관문이에요."},
    {"code": "BRI", "name_ko": "바리", "lat": 41.1171, "lon": 16.8719, "desc": "이탈리아 남동부 풀리아주의 눈부신 해안선과 풍부한 올리브의 도시예요."},
    {"code": "PSA", "name_ko": "피사", "lat": 43.7228, "lon": 10.4017, "desc": "세상에서 가장 유명한 기울어진 종탑, '피사의 사탑'이 있는 곳이에요."},
    {"code": "SAY", "name_ko": "시에나", "lat": 43.3188, "lon": 11.3308, "desc": "독특한 부채꼴 광장 캄포에서 열리는 역동적인 말 경주 '팔리오'로 유명한 도시예요."}
]

os.makedirs(f"countries/{country}", exist_ok=True)

print("Downloading base map for Italy...")
urllib.request.urlretrieve(base_map_url, f"countries/{country}/regions.json")

print("Generating data for Italy...")
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

var_name = "ITALY_CITIES_DESCRIPTIONS"
desc_content = f"var {var_name} = {{\n" + ",\n".join(descriptions) + f"\n}};\n\nif (typeof REGION_DESCRIPTIONS !== 'undefined') {{\n    Object.assign(REGION_DESCRIPTIONS, {var_name});\n}} else {{\n    var REGION_DESCRIPTIONS = {var_name};\n}}\n"

with open(f"countries/{country}/descriptions.js", "w", encoding="utf-8") as f:
    f.write(desc_content)

print("Done preparing Italy data.")
