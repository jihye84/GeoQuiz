import json

translation = {
    "Alabama": ("알라배마", "목화 산업이 발달한 미국 남부의 주입니다."),
    "Alaska": ("알래스카", "미국에서 가장 넓고 추운 지역으로, 빙하와 자연이 아름답습니다."),
    "Arizona": ("애리조나", "그랜드 캐니언이 있는 장엄한 사막의 주입니다."),
    "Arkansas": ("아칸소", "다이아몬드 광산과 아름다운 자연으로 유명합니다."),
    "California": ("캘리포니아", "할리우드, 실리콘밸리, 그리고 눈부신 해변이 있는 서부의 중심지입니다."),
    "Colorado": ("콜로라도", "로키 산맥의 웅장한 자연경관이 일품인 곳입니다."),
    "Connecticut": ("코네티컷", "미국에서 가장 오래된 대학 중 하나인 예일 대학교가 있습니다."),
    "Delaware": ("델라웨어", "미국 헌법을 가장 먼저 승인한 첫 번째 주입니다."),
    "Florida": ("플로리다", "디즈니월드와 아름다운 마이애미 해변이 있는 일조량 풍부한 주입니다."),
    "Georgia": ("조지아", "코카콜라와 CNN의 본사가 있는 남부의 중심지입니다."),
    "Hawaii": ("하와이", "태평양에 위치한 아름다운 화산섬이자 최고의 휴양지입니다."),
    "Idaho": ("아이다호", "감자 농사로 유명하며, 아름다운 산악 지형을 자랑합니다."),
    "Illinois": ("일리노이", "바람의 도시 시카고가 있는 중서부의 경제 중심지입니다."),
    "Indiana": ("인디애나", "인디 500 자동차 경주로 유명한 주입니다."),
    "Iowa": ("아이오와", "옥수수 밭이 끝없이 펼쳐진 미국의 곡창 지대입니다."),
    "Kansas": ("캔자스", "소설 '오즈의 마법사'의 배경이 된 평원의 주입니다."),
    "Kentucky": ("켄터키", "말 경주 대회인 켄터키 더비와 프라이드 치킨으로 유명합니다."),
    "Louisiana": ("루이지애나", "재즈의 본고장이자 프랑스 문화가 섞인 독특한 지역입니다."),
    "Maine": ("메인", "맛있는 바닷가재(랍스터)와 험준한 해안선이 유명합니다."),
    "Maryland": ("메릴랜드", "체서피크 만과 해산물이 유명하며 수도 워싱턴 D.C.와 인접해 있습니다."),
    "Massachusetts": ("매사추세츠", "하버드와 MIT가 있는 미국의 학문적 중심지입니다."),
    "Michigan": ("미시간", "거대한 5대호에 둘러싸인 자동차 산업의 심장부입니다."),
    "Minnesota": ("미네소타", "1만 개의 호수가 있는 아름다운 자연의 주입니다."),
    "Mississippi": ("미시시피", "블루스 음악이 탄생한 미시시피 강 유역의 주입니다."),
    "Missouri": ("미주리", "서부 개척의 출발점인 게이트웨이 아치가 있는 곳입니다."),
    "Montana": ("몬태나", "거대한 하늘과 아름다운 국립공원이 있는 로키 산맥의 주입니다."),
    "Nebraska": ("네브래스카", "농업이 발달한 광활한 대평원의 주입니다."),
    "Nevada": ("네바다", "세계적인 엔터테인먼트 도시 라스베이거스가 있는 사막의 주입니다."),
    "New Hampshire": ("뉴햄프셔", "아름다운 가을 단풍으로 유명한 뉴잉글랜드의 주입니다."),
    "New Jersey": ("뉴저지", "뉴욕과 필라델피아 사이에 위치한 '정원의 주'입니다."),
    "New Mexico": ("뉴멕시코", "독특한 사막 기후와 아메리카 원주민 문화가 살아있는 곳입니다."),
    "New York": ("뉴욕", "자유의 여신상과 타임스 스퀘어가 있는 세계적인 경제 문화의 중심지입니다."),
    "North Carolina": ("노스캐롤라이나", "라이트 형제가 최초로 비행에 성공한 곳입니다."),
    "North Dakota": ("노스다코타", "광활한 농경지와 석유 자원이 풍부한 북부의 주입니다."),
    "Ohio": ("오하이오", "많은 미국 대통령을 배출한 항공 우주 산업의 중심지입니다."),
    "Oklahoma": ("오클라호마", "아메리카 원주민의 역사가 깊은 토네이도의 길목에 위치한 주입니다."),
    "Oregon": ("오리건", "울창한 숲과 크레이터 호 국립공원이 있는 친환경적인 주입니다."),
    "Pennsylvania": ("펜실베이니아", "미국 독립선언서가 발표된 역사적인 장소입니다."),
    "Rhode Island": ("로드아일랜드", "미국에서 가장 면적이 작은 주지만 해안선이 아름답습니다."),
    "South Carolina": ("사우스캐롤라이나", "아름다운 해변과 남부의 전통이 살아있는 주입니다."),
    "South Dakota": ("사우스다코타", "큰 바위 얼굴 모양의 러시모어 산 조각상이 유명합니다."),
    "Tennessee": ("테네시", "컨트리 음악의 수도 내슈빌이 있는 음악의 주입니다."),
    "Texas": ("텍사스", "미국 본토에서 가장 크며 카우보이와 우주 산업으로 유명합니다."),
    "Utah": ("유타", "소금 호수와 외계 행성 같은 신비한 국립공원들이 있는 곳입니다."),
    "Vermont": ("버몬트", "달콤한 메이플 시럽과 그린 마운틴으로 유명합니다."),
    "Virginia": ("버지니아", "미국 건국 초기 역사가 살아 숨 쉬는 '대통령의 어머니' 주입니다."),
    "Washington": ("워싱턴", "스타벅스의 고향인 시애틀과 장엄한 레이니어 산이 있습니다."),
    "West Virginia": ("웨스트버지니아", "애팔래치아 산맥에 자리한 아름다운 산악의 주입니다."),
    "Wisconsin": ("위스콘신", "맛있는 치즈와 낙농업으로 유명한 '치즈의 주'입니다."),
    "Wyoming": ("와이오밍", "최초의 국립공원인 옐로스톤 국립공원이 있는 곳입니다."),
    "District of Columbia": ("워싱턴 D.C.", "미국의 수도로, 백악관과 국회의사당이 있습니다.")
}

with open('countries/usa/states.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

descriptions = {}

for feature in data['objects']['states']['geometries']:
    eng_name = feature['properties']['name']
    if eng_name in translation:
        ko_name, desc = translation[eng_name]
        feature['properties']['name_ko'] = ko_name
        feature['properties']['nativeName'] = eng_name
        feature['properties']['code'] = eng_name
        descriptions[eng_name] = desc

with open('countries/usa/states.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

with open('countries/usa/descriptions.js', 'w', encoding='utf-8') as f:
    f.write("var REGION_DESCRIPTIONS = {\n")
    for k, v in descriptions.items():
        f.write(f'    "{k}": "{v}",\n')
    f.write("};\n")
