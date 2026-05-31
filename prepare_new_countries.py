import os
import json
import urllib.request

# URLs for base maps
BASE_MAPS = {
    "japan": "https://raw.githubusercontent.com/dataofjapan/land/master/japan.geojson",
    "china": "https://raw.githubusercontent.com/longwosion/geojson-map-china/master/china.json",
    "france": "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson"
}

# City Data
CITIES = {
    "japan": [
        {"code": "TYO", "name_ko": "도쿄", "lat": 35.6895, "lon": 139.6917, "desc": "일본의 정치, 경제, 문화의 중심지이자 최대의 메트로폴리스예요."},
        {"code": "OSA", "name_ko": "오사카", "lat": 34.6937, "lon": 135.5023, "desc": "‘천하의 부엌’이라 불리는 활기찬 상업 도시이자 맛집의 천국이에요."},
        {"code": "KYO", "name_ko": "교토", "lat": 35.0116, "lon": 135.7681, "desc": "천 년간 일본의 수도였으며, 수많은 사찰과 신사가 보존된 역사 도시예요."},
        {"code": "CTS", "name_ko": "삿포로", "lat": 43.0618, "lon": 141.3545, "desc": "눈 축제와 신선한 해산물, 맥주로 유명한 홋카이도의 중심 도시예요."},
        {"code": "FUK", "name_ko": "후쿠오카", "lat": 33.5902, "lon": 130.4017, "desc": "돈코츠 라멘의 본고장이자 규슈 지방의 활기찬 관문 도시예요."},
        {"code": "NGO", "name_ko": "나고야", "lat": 35.1815, "lon": 136.9066, "desc": "도요타 자동차 등 세계적인 제조업이 발달한 산업의 중심지예요."},
        {"code": "YOK", "name_ko": "요코하마", "lat": 35.4437, "lon": 139.6380, "desc": "이국적인 차이나타운과 야경이 아름다운 매력적인 항구 도시예요."},
        {"code": "UKB", "name_ko": "고베", "lat": 34.6901, "lon": 135.1955, "desc": "질 좋은 소고기와 세련된 서양식 건축물로 유명한 항구 도시예요."},
        {"code": "SDJ", "name_ko": "센다이", "lat": 38.2682, "lon": 140.8694, "desc": "‘숲의 도시’라 불리는 도호쿠 지방 최대의 도시예요."},
        {"code": "HIJ", "name_ko": "히로시마", "lat": 34.3853, "lon": 132.4553, "desc": "평화 기념 공원과 떠 있는 토리이로 유명한 미야지마가 있는 곳이에요."},
        {"code": "OKA", "name_ko": "나하", "lat": 26.2124, "lon": 127.6809, "desc": "푸른 바다와 고유의 류큐 문화를 간직한 오키나와의 중심지예요."},
        {"code": "NGS", "name_ko": "나가사키", "lat": 32.7503, "lon": 129.8777, "desc": "짬뽕과 카스텔라, 그리고 서양과 교류했던 낭만적인 역사가 있는 항구예요."},
        {"code": "KMQ", "name_ko": "가나자와", "lat": 36.5613, "lon": 136.6562, "desc": "아름다운 일본식 정원 겐로쿠엔과 금박 공예가 유명한 도시예요."},
        {"code": "NRA", "name_ko": "나라", "lat": 34.6851, "lon": 135.8048, "desc": "거리 곳곳에서 사슴을 만날 수 있는 고대 일본의 첫 번째 수도예요."},
        {"code": "KIJ", "name_ko": "니가타", "lat": 37.9161, "lon": 139.0364, "desc": "일본 최고의 쌀과 아름다운 설경으로 유명한 동해 연안의 도시예요."},
        {"code": "FSZ", "name_ko": "시즈오카", "lat": 34.9756, "lon": 138.3828, "desc": "웅장한 후지산을 감상하며 품질 좋은 녹차를 맛볼 수 있는 곳이에요."},
        {"code": "KOJ", "name_ko": "가고시마", "lat": 31.5966, "lon": 130.5571, "desc": "여전히 연기를 뿜어내는 화산인 사쿠라지마를 품고 있는 최남단 도시예요."},
        {"code": "MYJ", "name_ko": "마쓰야마", "lat": 33.8392, "lon": 132.7653, "desc": "일본에서 가장 오래된 온천인 도고 온천과 아름다운 성이 있는 곳이에요."},
        {"code": "TAK", "name_ko": "다카마쓰", "lat": 34.3401, "lon": 134.0434, "desc": "쫄깃한 우동의 본고장이자 시코쿠로 들어가는 관문 도시예요."},
        {"code": "HKD", "name_ko": "하코다테", "lat": 41.7687, "lon": 140.7288, "desc": "별 모양의 요새와 눈부신 백만 불짜리 야경을 자랑하는 홋카이도의 항구예요."}
    ],
    "china": [
        {"code": "PEK", "name_ko": "베이징", "lat": 39.9042, "lon": 116.4074, "desc": "자금성과 만리장성을 품고 있는 중국의 위대한 수도예요."},
        {"code": "PVG", "name_ko": "상하이", "lat": 31.2304, "lon": 121.4737, "desc": "동방명주와 화려한 와이탄 야경이 빛나는 아시아 최대의 금융 도시예요."},
        {"code": "CAN", "name_ko": "광저우", "lat": 23.1291, "lon": 113.2644, "desc": "딤섬과 맛있는 요리의 본고장이자 남부 무역의 오랜 중심지예요."},
        {"code": "SZX", "name_ko": "선전", "lat": 22.5431, "lon": 114.0579, "desc": "거대한 IT 기업들이 밀집해 있는 중국의 실리콘밸리예요."},
        {"code": "CTU", "name_ko": "청두", "lat": 30.5728, "lon": 104.0668, "desc": "귀여운 판다의 고향이자 매콤한 마라 맛을 자랑하는 쓰촨성의 성도예요."},
        {"code": "CKG", "name_ko": "충칭", "lat": 29.5630, "lon": 106.5516, "desc": "깎아지른 절벽에 빽빽한 고층 빌딩이 솟아오른 웅장한 내륙 최대의 도시예요."},
        {"code": "XIY", "name_ko": "시안", "lat": 34.3416, "lon": 108.9398, "desc": "진시황릉의 병마용과 실크로드의 출발점인 수천 년 역사의 고도예요."},
        {"code": "HGH", "name_ko": "항저우", "lat": 30.2741, "lon": 120.1551, "desc": "아름다운 서호 호수와 알리바바 본사가 있는 시와 낭만의 도시예요."},
        {"code": "WUH", "name_ko": "우한", "lat": 30.5928, "lon": 114.3055, "desc": "거대한 창장 강이 가로지르는 교통과 물류의 요충지예요."},
        {"code": "NKG", "name_ko": "난징", "lat": 32.0603, "lon": 118.7969, "desc": "명나라의 수도였으며 깊고 슬픈 근대사를 간직한 유서 깊은 도시예요."},
        {"code": "TSN", "name_ko": "톈진", "lat": 39.0842, "lon": 117.2010, "desc": "서양식 건축물과 관람차가 아름다운 베이징의 관문 항구 도시예요."},
        {"code": "TAO", "name_ko": "칭다오", "lat": 36.0671, "lon": 120.3826, "desc": "독일풍의 붉은 지붕과 맛있는 칭다오 맥주로 유명한 아름다운 해변 도시예요."},
        {"code": "XMN", "name_ko": "샤먼", "lat": 24.4798, "lon": 118.0894, "desc": "바다 위의 피아노 섬이라 불리는 구랑위가 있는 이국적인 항구예요."},
        {"code": "DLC", "name_ko": "다롄", "lat": 38.9140, "lon": 121.6148, "desc": "한국과 가깝고 해산물이 풍부한 중국 동북 지방의 가장 세련된 도시예요."},
        {"code": "HRB", "name_ko": "하얼빈", "lat": 45.8038, "lon": 126.5350, "desc": "매년 겨울 거대한 얼음 조각 축제가 열리는 동북 지방의 추운 도시예요."},
        {"code": "CSX", "name_ko": "창사", "lat": 28.2282, "lon": 112.9388, "desc": "매운 후난 요리와 번화한 야시장으로 유명한 마오쩌둥의 고향이에요."},
        {"code": "CGO", "name_ko": "정저우", "lat": 34.7466, "lon": 113.6253, "desc": "무술의 요람 소림사가 위치한 중국 문명의 발상지 황허강 연안의 도시예요."},
        {"code": "KMG", "name_ko": "쿤밍", "lat": 25.0453, "lon": 102.7100, "desc": "일 년 내내 따뜻한 기후와 꽃이 가득하여 ‘봄의 도시’라 불리는 곳이에요."},
        {"code": "URC", "name_ko": "우루무치", "lat": 43.8256, "lon": 87.6168, "desc": "실크로드의 중심이자 바다에서 가장 멀리 떨어져 있는 이슬람 문화권 도시예요."},
        {"code": "LXA", "name_ko": "라싸", "lat": 29.6500, "lon": 91.1167, "desc": "해발 3,600미터 고원에 자리 잡은 웅장한 포탈라궁과 불교의 성지예요."}
    ],
    "france": [
        {"code": "PAR", "name_ko": "파리", "lat": 48.8566, "lon": 2.3522, "desc": "에펠탑과 루브르 박물관이 있는 낭만과 예술의 세계적인 중심지예요."},
        {"code": "MRS", "name_ko": "마르세유", "lat": 43.2965, "lon": 5.3698, "desc": "따뜻한 지중해의 붉은 지붕과 활기찬 분위기를 가진 프랑스 최대 항구 도시예요."},
        {"code": "LYS", "name_ko": "리옹", "lat": 45.7640, "lon": 4.8357, "desc": "프랑스 미식의 수도이자 르네상스 시대의 구시가지가 잘 보존된 도시예요."},
        {"code": "TLS", "name_ko": "툴루즈", "lat": 43.6047, "lon": 1.4442, "desc": "장미빛 벽돌 건물들로 가득한 아름다운 도시이자 유럽 항공 우주 산업의 중심지예요."},
        {"code": "NCE", "name_ko": "니스", "lat": 43.7102, "lon": 7.2620, "desc": "빛나는 햇살과 자갈 해변이 끝없이 펼쳐진 프랑스 남부 최고의 휴양지예요."},
        {"code": "NTE", "name_ko": "낭트", "lat": 47.2184, "lon": -1.5536, "desc": "기계 코끼리 테마파크와 옛 브르타뉴 공국의 성이 있는 창의적인 도시예요."},
        {"code": "SXB", "name_ko": "스트라스부르", "lat": 48.5734, "lon": 7.7521, "desc": "독일 국경과 맞닿아 있어 두 문화가 섞인 환상적인 크리스마스 마켓의 도시예요."},
        {"code": "MPL", "name_ko": "몽펠리에", "lat": 43.6108, "lon": 3.8767, "desc": "유럽에서 가장 오래된 의과 대학이 있는 젊고 활기찬 대학 도시예요."},
        {"code": "BOD", "name_ko": "보르도", "lat": 44.8378, "lon": -0.5792, "desc": "세계 최고의 와인이 생산되는 아름다운 물의 거울(Miroir d'eau)이 있는 도시예요."},
        {"code": "LIL", "name_ko": "릴", "lat": 50.6292, "lon": 3.0573, "desc": "벨기에 국경과 가까워 플랑드르 양식의 건축과 독특한 문화가 있는 상업 도시예요."},
        {"code": "RNS", "name_ko": "렌", "lat": 48.1173, "lon": -1.6778, "desc": "중세 목조 건축물이 매력적인 브르타뉴 지방의 고풍스러운 수도예요."},
        {"code": "RHE", "name_ko": "랭스", "lat": 49.2583, "lon": 4.0317, "desc": "역대 프랑스 왕들이 대관식을 올린 웅장한 대성당과 샴페인의 고향이에요."},
        {"code": "LEH", "name_ko": "르아브르", "lat": 49.4944, "lon": 0.1079, "desc": "인상파 미술이 탄생한 곳이자, 2차 대전 후 독특하게 재건된 항구 도시예요."},
        {"code": "EBU", "name_ko": "생테티엔", "lat": 45.4397, "lon": 4.3872, "desc": "과거 광공업과 무기 제조로 번성했던 디자인과 창의 산업의 중심지예요."},
        {"code": "TLN", "name_ko": "툴롱", "lat": 43.1242, "lon": 5.9280, "desc": "지중해의 햇살을 받는 아름다운 항구이자 프랑스 해군의 핵심 기지예요."},
        {"code": "GNB", "name_ko": "그르노블", "lat": 45.1885, "lon": 5.7245, "desc": "프랑스 알프스의 수도로 불리며 동계 스포츠와 첨단 과학 연구가 발달한 도시예요."},
        {"code": "DIJ", "name_ko": "디종", "lat": 47.3220, "lon": 5.0415, "desc": "세계적인 피노 누아 와인의 산지인 부르고뉴 지방의 중심이자 머스터드로 유명한 곳이에요."},
        {"code": "ANE", "name_ko": "앙제", "lat": 47.4723, "lon": -0.5516, "desc": "요새와 요한계시록을 담은 거대한 태피스트리로 유명한 루아르 계곡의 도시예요."},
        {"code": "FNI", "name_ko": "님", "lat": 43.8367, "lon": 4.3601, "desc": "거대한 고대 원형 경기장이 완벽하게 보존되어 '프랑스의 로마'라 불리는 도시예요."},
        {"code": "AVN", "name_ko": "아비뇽", "lat": 43.9493, "lon": 4.8055, "desc": "과거 교황이 머물렀던 웅장한 교황청과 춤바람 나는 끊어진 다리가 있는 도시예요."}
    ]
}

# Create dirs
for country in BASE_MAPS.keys():
    os.makedirs(f"countries/{country}", exist_ok=True)

# 1. Download base maps
for country, url in BASE_MAPS.items():
    print(f"Downloading base map for {country}...")
    try:
        urllib.request.urlretrieve(url, f"countries/{country}/regions.json")
    except Exception as e:
        print(f"Error downloading {country}: {e}")

# 2. Generate cities.json and descriptions.js
for country, cities in CITIES.items():
    print(f"Generating data for {country}...")
    features = []
    descriptions = []
    
    for city in cities:
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
        
    # save geojson
    geojson = {"type": "FeatureCollection", "features": features}
    with open(f"countries/{country}/cities.json", "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)
        
    # save descriptions
    var_name = f"{country.upper()}_CITIES_DESCRIPTIONS"
    desc_content = f"var {var_name} = {{\n" + ",\n".join(descriptions) + f"\n}};\n\nif (typeof REGION_DESCRIPTIONS !== 'undefined') {{\n    Object.assign(REGION_DESCRIPTIONS, {var_name});\n}} else {{\n    var REGION_DESCRIPTIONS = {var_name};\n}}\n"
    with open(f"countries/{country}/descriptions.js", "w", encoding="utf-8") as f:
        f.write(desc_content)

print("Done preparing JP, CN, FR data.")
