import json

# List of 100+ major US cities with lat, lon, region, and description (in Korean).
# West, Central, East
cities_data = [
    # WEST (Pacific, Mountain, some Southwest)
    {"code": "LAX", "name_ko": "로스앤젤레스", "lat": 34.0522, "lon": -118.2437, "region": "west", "desc": "할리우드와 아름다운 해변이 있는 서부 최대의 도시예요."},
    {"code": "SFO", "name_ko": "샌프란시스코", "lat": 37.7749, "lon": -122.4194, "region": "west", "desc": "금문교와 가파른 언덕, 실리콘밸리가 가까운 첨단 도시예요."},
    {"code": "SEA", "name_ko": "시애틀", "lat": 47.6062, "lon": -122.3321, "region": "west", "desc": "스타벅스의 고향이자 비가 자주 내리는 아름다운 항구 도시예요."},
    {"code": "LAS", "name_ko": "라스베이거스", "lat": 36.1699, "lon": -115.1398, "region": "west", "desc": "사막 한가운데 화려한 호텔과 카지노가 모여 있는 엔터테인먼트의 중심지예요."},
    {"code": "DEN", "name_ko": "덴버", "lat": 39.7392, "lon": -104.9903, "region": "west", "desc": "로키 산맥 기슭에 위치한 아름다운 고산 도시예요."},
    {"code": "PHX", "name_ko": "피닉스", "lat": 33.4484, "lon": -112.0740, "region": "west", "desc": "그랜드 캐니언이 있는 애리조나주의 따뜻한 사막 도시예요."},
    {"code": "SAN", "name_ko": "샌디에이고", "lat": 32.7157, "lon": -117.1611, "region": "west", "desc": "온화한 날씨와 해군 기지로 유명한 캘리포니아 남부의 도시예요."},
    {"code": "PDX", "name_ko": "포틀랜드", "lat": 45.5051, "lon": -122.6750, "region": "west", "desc": "장미의 도시라 불리는 친환경적이고 힙한 분위기의 도시예요."},
    {"code": "SLC", "name_ko": "솔트레이크시티", "lat": 40.7608, "lon": -111.8910, "region": "west", "desc": "동계 올림픽이 열렸던 곳이자 거대한 소금 호수가 있는 도시예요."},
    {"code": "HNL", "name_ko": "호놀룰루", "lat": 21.3069, "lon": -157.8583, "region": "west", "desc": "와이키키 해변이 있는 하와이의 아름다운 휴양 도시예요."},
    {"code": "ANC", "name_ko": "앵커리지", "lat": 61.2181, "lon": -149.9003, "region": "west", "desc": "웅장한 빙하와 대자연을 만날 수 있는 알래스카 최대의 도시예요."},
    {"code": "SJC", "name_ko": "산호세", "lat": 37.3382, "lon": -121.8863, "region": "west", "desc": "수많은 글로벌 IT 기업들이 모여 있는 실리콘밸리의 중심 도시예요."},
    {"code": "SMF", "name_ko": "새크라멘토", "lat": 38.5816, "lon": -121.4944, "region": "west", "desc": "골드러시 시대의 역사를 간직한 캘리포니아주의 주도예요."},
    {"code": "TUS", "name_ko": "투손", "lat": 32.2226, "lon": -110.9747, "region": "west", "desc": "거대한 사구아로 선인장을 볼 수 있는 애리조나의 사막 도시예요."},
    {"code": "ABQ", "name_ko": "앨버커키", "lat": 35.0844, "lon": -106.6504, "region": "west", "desc": "매년 가을 하늘을 수놓는 열기구 축제로 유명한 도시예요."},
    {"code": "BOI", "name_ko": "보이시", "lat": 43.6150, "lon": -116.2023, "region": "west", "desc": "아이다호 감자로 유명한 지역의 살기 좋은 주도예요."},
    {"code": "RNO", "name_ko": "리노", "lat": 39.5296, "lon": -119.8138, "region": "west", "desc": "세상에서 가장 큰 소도시라 불리는 네바다의 카지노 도시예요."},
    {"code": "COS", "name_ko": "콜로라도스프링스", "lat": 38.8339, "lon": -104.8214, "region": "west", "desc": "신들의 정원이라는 웅장한 붉은 바위가 있는 아름다운 도시예요."},
    {"code": "SFE", "name_ko": "산타페", "lat": 35.6870, "lon": -105.9378, "region": "west", "desc": "독특한 아도비 건축물과 예술가들의 갤러리가 많은 도시예요."},
    {"code": "FAT", "name_ko": "프레즈노", "lat": 36.7378, "lon": -119.7871, "region": "west", "desc": "풍부한 일조량으로 과일과 농산물이 많이 나는 캘리포니아 농업 중심지예요."},

    # CENTRAL (Midwest, Texas, Great Plains)
    {"code": "ORD", "name_ko": "시카고", "lat": 41.8781, "lon": -87.6298, "region": "central", "desc": "미시간 호수 옆에 위치한 마천루의 도시이자 바람의 도시예요."},
    {"code": "IAH", "name_ko": "휴스턴", "lat": 29.7604, "lon": -95.3698, "region": "central", "desc": "NASA 우주센터가 있는 텍사스 최대의 도시예요."},
    {"code": "DFW", "name_ko": "댈러스", "lat": 32.7767, "lon": -96.7970, "region": "central", "desc": "미국 남부의 경제 중심지이자 카우보이 문화가 있는 도시예요."},
    {"code": "AUS", "name_ko": "오스틴", "lat": 30.2672, "lon": -97.7431, "region": "central", "desc": "라이브 음악의 세계적 수도이자 테슬라 등 기술 기업이 모인 도시예요."},
    {"code": "SAT", "name_ko": "샌안토니오", "lat": 29.4241, "lon": -98.4936, "region": "central", "desc": "알라모 전투의 역사와 아름다운 리버워크가 있는 도시예요."},
    {"code": "MSP", "name_ko": "미니애폴리스", "lat": 44.9778, "lon": -93.2650, "region": "central", "desc": "수많은 호수와 거대한 쇼핑몰로 유명한 중서부의 도시예요."},
    {"code": "STL", "name_ko": "세인트루이스", "lat": 38.6270, "lon": -90.1994, "region": "central", "desc": "서부 개척의 상징인 거대한 게이트웨이 아치가 있는 도시예요."},
    {"code": "MCI", "name_ko": "캔자스시티", "lat": 39.0997, "lon": -94.5786, "region": "central", "desc": "맛있는 바비큐와 재즈 음악으로 유명한 미주리의 도시예요."},
    {"code": "MSY", "name_ko": "뉴올리언스", "lat": 29.9511, "lon": -90.0715, "region": "central", "desc": "재즈의 발상지이자 매년 마디그라 축제가 열리는 독특한 문화의 도시예요."},
    {"code": "MEM", "name_ko": "멤피스", "lat": 35.1495, "lon": -90.0490, "region": "central", "desc": "엘비스 프레슬리의 고향이자 로큰롤과 블루스의 성지예요."},
    {"code": "BNA", "name_ko": "내슈빌", "lat": 36.1627, "lon": -86.7816, "region": "central", "desc": "미국 컨트리 음악의 중심지이자 활기찬 남부 도시예요."},
    {"code": "IND", "name_ko": "인디애나폴리스", "lat": 39.7684, "lon": -86.1581, "region": "central", "desc": "세계적인 자동차 경주 대회인 인디 500이 열리는 도시예요."},
    {"code": "CLE", "name_ko": "클리블랜드", "lat": 41.4993, "lon": -81.6944, "region": "central", "desc": "로큰롤 명예의 전당이 있는 이리호 연안의 산업 도시예요."},
    {"code": "CVG", "name_ko": "신시내티", "lat": 39.1031, "lon": -84.5120, "region": "central", "desc": "오하이오강을 끼고 발달한 유서 깊은 중서부 무역 도시예요."},
    {"code": "CMH", "name_ko": "콜럼버스", "lat": 39.9612, "lon": -83.0007, "region": "central", "desc": "오하이오주의 주도이자 젊고 활기찬 대학 도시예요."},
    {"code": "MKE", "name_ko": "밀워키", "lat": 43.0389, "lon": -87.9065, "region": "central", "desc": "미시건 호수 연안의 맥주 양조와 치즈로 유명한 도시예요."},
    {"code": "OMA", "name_ko": "오마하", "lat": 41.2565, "lon": -95.9345, "region": "central", "desc": "투자의 귀재 워런 버핏의 고향이자 세계 최고 수준의 동물원이 있는 도시예요."},
    {"code": "OKC", "name_ko": "오클라호마시티", "lat": 35.4676, "lon": -97.5164, "region": "central", "desc": "서부 카우보이 문화와 원주민의 역사가 살아 숨쉬는 도시예요."},
    {"code": "TUL", "name_ko": "털사", "lat": 36.1540, "lon": -95.9928, "region": "central", "desc": "과거 세계의 석유 수도로 불렸던 화려한 아르데코 건축의 도시예요."},
    {"code": "DSM", "name_ko": "디모인", "lat": 41.5868, "lon": -93.6250, "region": "central", "desc": "미국 대선의 첫 번째 코커스가 열리는 정치적 상징성이 큰 도시예요."},

    # EAST (Northeast, South Atlantic)
    {"code": "JFK", "name_ko": "뉴욕", "lat": 40.7128, "lon": -74.0060, "region": "east", "desc": "자유의 여신상과 타임스 스퀘어가 있는 세계 경제와 문화의 중심지예요."},
    {"code": "DCA", "name_ko": "워싱턴 D.C.", "lat": 38.9072, "lon": -77.0369, "region": "east", "desc": "백악관과 수많은 박물관이 있는 미국의 위대한 수도예요."},
    {"code": "BOS", "name_ko": "보스턴", "lat": 42.3601, "lon": -71.0589, "region": "east", "desc": "하버드와 MIT가 있는 교육의 도시이자 미국 독립의 역사가 깊은 곳이에요."},
    {"code": "MIA", "name_ko": "마이애미", "lat": 25.7617, "lon": -80.1918, "region": "east", "desc": "아름다운 해변과 라틴 문화가 가득한 플로리다의 휴양 도시예요."},
    {"code": "ATL", "name_ko": "애틀랜타", "lat": 33.7490, "lon": -84.3880, "region": "east", "desc": "코카콜라와 CNN의 본사가 있는 미국 남부 최대의 경제 중심지예요."},
    {"code": "PHL", "name_ko": "필라델피아", "lat": 39.9526, "lon": -75.1652, "region": "east", "desc": "미국 독립선언서가 발표된 역사적 의미가 가장 깊은 도시예요."},
    {"code": "MCO", "name_ko": "올랜도", "lat": 28.5383, "lon": -81.3792, "region": "east", "desc": "월트 디즈니 월드와 유니버설 스튜디오가 있는 테마파크의 천국이에요."},
    {"code": "CLT", "name_ko": "샬럿", "lat": 35.2271, "lon": -80.8431, "region": "east", "desc": "미국의 주요 은행 본사들이 모여 있는 떠오르는 금융 도시예요."},
    {"code": "PIT", "name_ko": "피츠버그", "lat": 40.4406, "lon": -79.9959, "region": "east", "desc": "과거 철강 도시에서 지금은 로봇과 AI 연구의 중심지로 변신한 곳이에요."},
    {"code": "BWI", "name_ko": "볼티모어", "lat": 39.2904, "lon": -76.6122, "region": "east", "desc": "아름다운 이너 하버와 해산물이 유명한 메릴랜드주의 항구 도시예요."},
    {"code": "RDU", "name_ko": "롤리", "lat": 35.7796, "lon": -78.6382, "region": "east", "desc": "미국의 주요 연구 단지인 리서치 트라이앵글의 중심지예요."},
    {"code": "RIC", "name_ko": "리치먼드", "lat": 37.5407, "lon": -77.4360, "region": "east", "desc": "과거 남부 연합의 수도였던 버지니아주의 유서 깊은 주도예요."},
    {"code": "TPA", "name_ko": "탬파", "lat": 27.9506, "lon": -82.4572, "region": "east", "desc": "플로리다 서부 해안에 위치한 햇살이 아름다운 항구 도시예요."},
    {"code": "CHS", "name_ko": "찰스턴", "lat": 32.7765, "lon": -79.9311, "region": "east", "desc": "미국 남부 특유의 전통과 고풍스러운 저택들이 잘 보존된 도시예요."},
    {"code": "SAV", "name_ko": "서배너", "lat": 32.0809, "lon": -81.0912, "region": "east", "desc": "아름다운 스페인 이끼와 낭만적인 풍경으로 가득한 항구 도시예요."},
    {"code": "PVD", "name_ko": "프로비던스", "lat": 41.8240, "lon": -71.4128, "region": "east", "desc": "아이비리그인 브라운 대학교가 있는 작지만 아름다운 교육 도시예요."},
    {"code": "HFD", "name_ko": "하트퍼드", "lat": 41.7658, "lon": -72.6734, "region": "east", "desc": "수많은 대형 보험회사가 몰려 있어 세계의 보험 수도라 불리는 곳이에요."},
    {"code": "BUF", "name_ko": "버펄로", "lat": 42.8864, "lon": -78.8784, "region": "east", "desc": "나이아가라 폭포와 가깝고 버펄로 윙의 본고장으로 유명한 도시예요."},
    {"code": "JAX", "name_ko": "잭슨빌", "lat": 30.3322, "lon": -81.6557, "region": "east", "desc": "플로리다에서 가장 면적이 넓은 활기찬 해양 도시예요."},
    {"code": "SJU", "name_ko": "산후안", "lat": 18.4655, "lon": -66.1057, "region": "east", "desc": "카리브해의 보석이라 불리는 푸에르토리코의 눈부신 수도예요."}
]

# Generate GeoJSON
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
            "region": city["region"],
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

with open("countries/usa/cities.json", "w", encoding="utf-8") as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)

desc_file_content = "var CITIES_REGION_DESCRIPTIONS = {\n" + ",\n".join(descriptions) + "\n};\n\nif (typeof REGION_DESCRIPTIONS !== 'undefined') {\n    Object.assign(REGION_DESCRIPTIONS, CITIES_REGION_DESCRIPTIONS);\n} else {\n    var REGION_DESCRIPTIONS = CITIES_REGION_DESCRIPTIONS;\n}\n"

with open("countries/usa/cities-descriptions.js", "w", encoding="utf-8") as f:
    f.write(desc_file_content)

print(f"Generated {len(features)} cities into countries/usa/cities.json and cities-descriptions.js")
