import json

translation = {
    "Baden-Württemberg": ("바덴뷔르템베르크", "자동차 산업의 중심지이자 아름다운 검은 숲(슈바르츠발트)이 있는 주입니다."),
    "Bayern": ("바이에른", "뮌헨이 주도이며 옥토버페스트와 알프스 산맥으로 유명한 아름다운 주입니다."),
    "Berlin": ("베를린", "독일의 수도이자 역사적인 브란덴부르크 문이 있는 세계적인 문화 도시입니다."),
    "Brandenburg": ("브란덴부르크", "베를린을 둘러싸고 있으며 수많은 호수와 아름다운 궁전들이 있는 주입니다."),
    "Bremen": ("브레멘", "그림 형제의 동화 '브레멘 음악대'로 유명한 역사적인 항구 도시입니다."),
    "Hamburg": ("함부르크", "수많은 다리와 운하가 있는 독일 최대의 항구 도시입니다."),
    "Hessen": ("헤센", "금융 중심지 프랑크푸르트와 울창한 숲이 있는 경제적으로 풍요로운 주입니다."),
    "Mecklenburg-Vorpommern": ("메클렌부르크포어포메른", "발트해 연안의 아름다운 해변과 섬들이 있는 휴양지입니다."),
    "Niedersachsen": ("니더작센", "폭스바겐의 본사가 있는 거대한 평원과 해안을 품은 주입니다."),
    "Nordrhein-Westfalen": ("노르트라인베스트팔렌", "라인강을 따라 발달한 독일 인구 최대의 융성한 산업 지대입니다."),
    "Rheinland-Pfalz": ("라인란트팔츠", "라인강의 기적을 상징하는 강과 포도밭, 고성들이 가득한 주입니다."),
    "Saarland": ("자를란트", "프랑스와 국경을 접하고 있으며 광산과 산업 유산이 풍부한 작은 주입니다."),
    "Sachsen": ("작센", "드레스덴과 라이프치히 등 문화와 예술이 살아 숨쉬는 역사적인 주입니다."),
    "Sachsen-Anhalt": ("작센안할트", "종교개혁자 마틴 루터의 발자취와 수많은 유네스코 유산이 있는 곳입니다."),
    "Schleswig-Holstein": ("슐레스비히홀슈타인", "북해와 발트해를 모두 품고 있는 독일 최북단의 아름다운 주입니다."),
    "Thüringen": ("튀링겐", "독일의 심장부에 위치한 '녹색 심장'으로 불리는 숲이 우거진 주입니다.")
}

with open('countries/germany/regions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

descriptions = {}

for feature in data['features']:
    eng_name = feature['properties']['name']
    if eng_name in translation:
        ko_name, desc = translation[eng_name]
    else:
        ko_name = eng_name
        desc = f"{eng_name}, 독일의 아름다운 지역 중 하나입니다."
        
    feature['properties']['name_ko'] = ko_name
    feature['properties']['nativeName'] = eng_name
    feature['properties']['code'] = eng_name
    descriptions[eng_name] = desc

with open('countries/germany/regions.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

with open('countries/germany/descriptions.js', 'w', encoding='utf-8') as f:
    f.write("var REGION_DESCRIPTIONS = {\n")
    for k, v in descriptions.items():
        safe_v = v.replace('"', '\\"')
        f.write(f'    "{k}": "{safe_v}",\n')
    f.write("};\n")
