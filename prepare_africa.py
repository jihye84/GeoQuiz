import os
import json
import urllib.request

base_map_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/africa.geojson"

# All 56 entities in the geojson
AFRICA_DATA = {
    "Egypt": {"ko": "이집트", "top10": True, "top25": True, "desc": "피라미드와 스핑크스, 그리고 세계에서 가장 긴 나일강이 흐르는 신비로운 고대 문명의 나라예요."},
    "South Africa": {"ko": "남아프리카 공화국", "top10": True, "top25": True, "desc": "아프리카 최남단에 위치하며 야생동물과 넬슨 만델라로 유명한 무지개 국가예요."},
    "Ethiopia": {"ko": "에티오피아", "top10": True, "top25": True, "desc": "아프리카에서 유일하게 식민 지배를 이겨낸 역사를 자랑하며 커피가 처음 발견된 나라예요."},
    "Kenya": {"ko": "케냐", "top10": True, "top25": True, "desc": "끝없이 펼쳐진 초원 사바나에서 사자와 코끼리가 뛰어노는 동물의 왕국이에요."},
    "Nigeria": {"ko": "나이지리아", "top10": True, "top25": True, "desc": "아프리카에서 인구가 가장 많으며 풍부한 석유 자원을 가진 서아프리카의 거인이에요."},
    "Morocco": {"ko": "모로코", "top10": True, "top25": True, "desc": "사하라 사막과 지중해가 만나며 붉은 도시 마라케시로 유명한 아름다운 나라예요."},
    "Madagascar": {"ko": "마다가스카르", "top10": True, "top25": True, "desc": "아프리카 대륙 옆에 있는 거대한 섬으로 바오밥나무와 귀여운 여우원숭이의 고향이에요."},
    "Tanzania": {"ko": "탄자니아", "top10": True, "top25": True, "desc": "아프리카 최고봉 킬리만자로 산과 거대한 세렝게티 국립공원이 있는 자연의 보고예요."},
    "Senegal": {"ko": "세네갈", "top10": True, "top25": True, "desc": "서아프리카의 가장 서쪽에 위치하며 다카르 랠리와 음악으로 유명한 매력적인 나라예요."},
    "Ghana": {"ko": "가나", "top10": True, "top25": True, "desc": "아프리카 최초로 독립을 이뤄냈으며 맛있는 초콜릿의 원료인 카카오가 많이 나는 나라예요."},
    
    "Algeria": {"ko": "알제리", "top10": False, "top25": True, "desc": "국토의 대부분이 사하라 사막으로 덮여 있는 아프리카 대륙에서 가장 면적이 넓은 나라예요."},
    "Angola": {"ko": "앙골라", "top10": False, "top25": True, "desc": "석유와 다이아몬드 자원이 풍부하며 역동적으로 성장하고 있는 남서부 아프리카의 나라예요."},
    "Cameroon": {"ko": "카메룬", "top10": False, "top25": True, "desc": "다양한 자연 환경을 모두 갖추고 있어 '축소된 아프리카'라고 불리는 축구 강국이에요."},
    "Ivory Coast": {"ko": "코트디부아르", "top10": False, "top25": True, "desc": "이름 자체가 '상아 해안'을 뜻하며 세계 1위의 카카오 생산국으로 유명해요."},
    "DR Congo": {"ko": "민주콩고", "top10": False, "top25": True, "desc": "아프리카 대륙의 심장부에 위치하며 거대한 열대우림과 풍부한 지하자원을 가진 나라예요."},
    "Libya": {"ko": "리비아", "top10": False, "top25": True, "desc": "지중해와 맞닿아 있으며 사하라 사막 아래 방대한 석유가 묻혀 있는 북아프리카 국가예요."},
    "Tunisia": {"ko": "튀니지", "top10": False, "top25": True, "desc": "고대 카르타고의 유적이 남아있으며 지중해의 아름다운 해변을 자랑하는 나라예요."},
    "Uganda": {"ko": "우간다", "top10": False, "top25": True, "desc": "아프리카 최대의 호수인 빅토리아 호수를 품고 있어 '아프리카의 진주'라 불려요."},
    "Rwanda": {"ko": "르완다", "top10": False, "top25": True, "desc": "아픈 역사를 딛고 '천 개의 언덕'이라는 별명처럼 깨끗하고 아름답게 발전하고 있는 나라예요."},
    "Somalia": {"ko": "소말리아", "top10": False, "top25": True, "desc": "아프리카 대륙에서 가장 긴 해안선을 가지고 있는 '아프리카의 뿔' 모양의 나라예요."},
    "Mozambique": {"ko": "모잠비크", "top10": False, "top25": True, "desc": "인도양과 마주하는 긴 해안선을 따라 아름다운 산호초와 해변이 펼쳐진 나라예요."},
    "Zimbabwe": {"ko": "짐바브웨", "top10": False, "top25": True, "desc": "세계 3대 폭포 중 하나인 거대한 빅토리아 폭포의 장엄한 풍경을 만날 수 있는 곳이에요."},
    "Zambia": {"ko": "잠비아", "top10": False, "top25": True, "desc": "구리 자원이 풍부하며 짐바브웨와 함께 아름다운 빅토리아 폭포를 나누어 가진 나라예요."},
    "Sudan": {"ko": "수단", "top10": False, "top25": True, "desc": "청나일강과 백나일강이 만나 이집트로 흘러가는 길목에 위치한 넓은 영토의 나라예요."},
    "Mali": {"ko": "말리", "top10": False, "top25": True, "desc": "사하라 사막 남쪽에 위치하며 황금의 제국이었던 옛 말리 제국의 찬란한 역사를 가진 나라예요."},
    
    # 54 All Others
    "Benin": {"ko": "베냉", "top10": False, "top25": False, "desc": "서아프리카에 위치한 전통 종교인 부두교의 발상지로 알려진 나라예요."},
    "Botswana": {"ko": "보츠와나", "top10": False, "top25": False, "desc": "거대한 칼라하리 사막과 코끼리 떼가 모이는 오카방고 삼각주가 있는 평화로운 나라예요."},
    "Burkina Faso": {"ko": "부르키나파소", "top10": False, "top25": False, "desc": "'정직한 사람들의 땅'이라는 뜻의 아름다운 이름을 가진 서아프리카의 내륙 국가예요."},
    "Burundi": {"ko": "부룬디", "top10": False, "top25": False, "desc": "동아프리카의 거대한 탕가니카 호수와 맞닿아 있는 작지만 아름다운 산악 국가예요."},
    "Cape Verde": {"ko": "카보베르데", "top10": False, "top25": False, "desc": "대서양에 떠 있는 10개의 화산섬으로 이루어져 아름다운 해변과 독특한 음악이 있는 나라예요."},
    "Central African Republic": {"ko": "중앙아프리카 공화국", "top10": False, "top25": False, "desc": "이름처럼 아프리카 대륙의 정중앙에 위치하며 다양한 야생동물이 서식하는 나라예요."},
    "Chad": {"ko": "차드", "top10": False, "top25": False, "desc": "사하라 사막 남부에 위치하며 과거 거대한 호수였던 차드 호수가 있는 건조한 나라예요."},
    "Comoros": {"ko": "코모로", "top10": False, "top25": False, "desc": "인도양에 떠 있는 화산섬들로 이루어져 아름다운 자연을 간직한 작은 섬나라예요."},
    "Congo": {"ko": "콩고 공화국", "top10": False, "top25": False, "desc": "민주콩고와 마주보고 있으며 열대우림과 넓은 콩고강이 흐르는 서부 아프리카 국가예요."},
    "Djibouti": {"ko": "지부티", "top10": False, "top25": False, "desc": "홍해와 아덴만이 만나는 전략적 요충지에 위치한 뜨겁고 화산 지형이 발달한 나라예요."},
    "Equatorial Guinea": {"ko": "적도 기니", "top10": False, "top25": False, "desc": "아프리카에서 유일하게 스페인어를 공용어로 사용하는 풍요로운 자원을 가진 나라예요."},
    "Eritrea": {"ko": "에리트레아", "top10": False, "top25": False, "desc": "에티오피아에서 독립했으며 아름다운 홍해 해안선과 이탈리아식 건축물이 남아있는 곳이에요."},
    "Gabon": {"ko": "가봉", "top10": False, "top25": False, "desc": "울창한 열대우림이 국토의 대부분을 덮고 있어 다양한 동식물이 평화롭게 살아가는 나라예요."},
    "Gambia": {"ko": "감비아", "top10": False, "top25": False, "desc": "아프리카 본토에서 가장 작은 나라이며, 감비아 강을 따라 세네갈에 둘러싸인 독특한 형태를 가졌어요."},
    "Guinea": {"ko": "기니", "top10": False, "top25": False, "desc": "서아프리카의 주요 강들이 발원하는 곳이며 철광석과 알루미늄 자원이 풍부한 나라예요."},
    "Guinea-Bissau": {"ko": "기니비사우", "top10": False, "top25": False, "desc": "서아프리카 연안에 위치하며 많은 섬들로 이루어진 독특한 생태계를 가진 나라예요."},
    "Lesotho": {"ko": "레소토", "top10": False, "top25": False, "desc": "남아프리카 공화국에 완전히 둘러싸여 있는 '하늘의 왕국'이라 불리는 고산 국가예요."},
    "Liberia": {"ko": "라이베리아", "top10": False, "top25": False, "desc": "미국에서 해방된 흑인 노예들이 세운 나라로 아프리카 최초의 근대 공화국이에요."},
    "Malawi": {"ko": "말라위", "top10": False, "top25": False, "desc": "국토의 큰 부분을 차지하는 말라위 호수가 다채로운 물고기들로 가득한 아름다운 나라예요."},
    "Mauritania": {"ko": "모리타니", "top10": False, "top25": False, "desc": "국토의 대부분이 모래로 덮여 있는 광활한 사하라 사막의 서쪽 끝을 차지한 나라예요."},
    "Mauritius": {"ko": "모리셔스", "top10": False, "top25": False, "desc": "인도양의 아름다운 산호초로 둘러싸여 '인도양의 진주'라 불리는 세계적인 휴양지예요."},
    "Namibia": {"ko": "나미비아", "top10": False, "top25": False, "desc": "사막과 바다가 만나는 경이로운 붉은 모래언덕 나미브 사막이 있는 아름다운 나라예요."},
    "Niger": {"ko": "니제르", "top10": False, "top25": False, "desc": "거대한 사하라 사막을 품고 유유히 흐르는 니제르 강을 따라 사람들이 살아가는 내륙 국가예요."},
    "Sao Tome and Principe": {"ko": "상투메 프린시페", "top10": False, "top25": False, "desc": "기니만에 떠 있는 두 개의 화산섬으로 이루어진 울창한 숲과 카카오의 나라예요."},
    "Seychelles": {"ko": "세이셸", "top10": False, "top25": False, "desc": "인도양에 위치한 115개의 아름다운 화산섬들로 이루어진 지상 낙원 같은 나라예요."},
    "Sierra Leone": {"ko": "시에라리온", "top10": False, "top25": False, "desc": "'사자 산'이라는 뜻을 가졌으며, 아픈 역사를 극복하고 평화를 되찾아가는 서아프리카의 나라예요."},
    "South Sudan": {"ko": "남수단", "top10": False, "top25": False, "desc": "세계에서 가장 최근인 2011년에 독립한 나라로 다양한 부족들이 어울려 사는 땅이에요."},
    "Swaziland": {"ko": "에스와티니", "top10": False, "top25": False, "desc": "(구 스와질란드) 남아프리카에 위치한 작고 평화로운 전통 왕정이 유지되고 있는 나라예요."},
    "Togo": {"ko": "토고", "top10": False, "top25": False, "desc": "서아프리카 기니만에 위치한 작고 길쭉한 형태의 나라로 무역이 활발한 항구를 가지고 있어요."},
    "Western Sahara": {"ko": "서사하라", "top10": False, "top25": False, "desc": "아프리카 북서부 해안에 위치하며 끝없는 모래 평원이 대서양과 마주하는 넓은 지역이에요."},
    "La Reunion": {"ko": "레위니옹 (프랑스령)", "top10": False, "top25": False, "desc": "마다가스카르 옆 인도양에 위치하며 웅장한 활화산이 장관을 이루는 프랑스령 섬이에요."}
}

os.makedirs("countries/africa", exist_ok=True)

print("Downloading Africa GeoJSON...")
req = urllib.request.urlopen(base_map_url)
data = json.loads(req.read())

features = []
descriptions = []

# To ensure unique codes since GeoJSON might not have short codes, we'll use English name as code or ISO.
# But it's easier to just generate a short string code or use the name. Let's use name.
for f in data["features"]:
    name_en = f["properties"].get("name")
    if not name_en:
        continue
        
    info = AFRICA_DATA.get(name_en)
    if not info:
        print(f"Warning: Missing data for {name_en}. Creating default.")
        info = {"ko": name_en, "top10": False, "top25": False, "desc": f"아프리카의 국가 {name_en}입니다."}
    
    # Update properties
    f["properties"]["name_ko"] = info["ko"]
    f["properties"]["isTop10"] = info["top10"]
    f["properties"]["isTop25"] = info["top25"]
    f["properties"]["code"] = name_en.replace(" ", "_").upper()
    
    descriptions.append(f'    "{f["properties"]["code"]}": "{info["desc"]}"')

with open("countries/africa/regions.json", "w", encoding="utf-8") as out_f:
    json.dump(data, out_f, ensure_ascii=False)

var_name = "AFRICA_DESCRIPTIONS"
desc_content = f"var {var_name} = {{\n" + ",\n".join(descriptions) + f"\n}};\n\nif (typeof REGION_DESCRIPTIONS !== 'undefined') {{\n    Object.assign(REGION_DESCRIPTIONS, {var_name});\n}} else {{\n    var REGION_DESCRIPTIONS = {var_name};\n}}\n"

with open("countries/africa/descriptions.js", "w", encoding="utf-8") as f:
    f.write(desc_content)

print("Done preparing Africa data.")
