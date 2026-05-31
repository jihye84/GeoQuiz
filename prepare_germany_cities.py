import json

cities_25 = {
    "Berlin": ("베를린", "분단과 통일의 역사가 공존하며, 브란덴부르크 문과 베를린 장벽이 있는 독일의 수도입니다.", "Berlin"),
    "Hamburg": ("함부르크", "수많은 다리와 운하가 교차하는 독일 최대의 항구 도시이자 비틀즈가 무명 시절 활약한 곳입니다.", "Hamburg"),
    "München": ("뮌헨", "세계 최대 맥주 축제 옥토버페스트가 열리며, 알프스 산맥의 관문인 바이에른주의 중심입니다.", "München"),
    "Köln": ("쾰른", "하늘을 찌를 듯한 거대한 쾰른 대성당이 라인강을 굽어보는 유서 깊은 도시입니다.", "Köln"),
    "Frankfurt am Main": ("프랑크푸르트", "유럽 중앙은행이 있는 금융의 중심지이자, 대문호 괴테가 태어난 곳입니다.", "Frankfurt am Main"),
    "Stuttgart": ("슈투트가르트", "메르세데스-벤츠와 포르쉐의 본사가 위치한 첨단 자동차 산업의 요람입니다.", "Stuttgart"),
    "Düsseldorf": ("뒤셀도르프", "라인강의 기적을 이끈 경제 중심지이며, 패션과 무역 박람회로 유명한 세련된 도시입니다.", "Düsseldorf"),
    "Leipzig": ("라이프치히", "음악가 바흐가 평생 헌신한 성 토마스 교회가 있으며, 동서독 통일 운동의 도화선이 된 도시입니다.", "Leipzig"),
    "Bremen": ("브레멘", "그림 형제의 동화 '브레멘 음악대'의 배경으로 널리 알려진 역사적인 북부 항구 도시입니다.", "Bremen"),
    "Dresden": ("드레스덴", "화려한 바로크 건축물들이 가득해 '엘베강의 피렌체'라 불리는 작센주의 문화 예술 중심지입니다.", "Dresden"),
    "Hanover": ("하노버", "세계 최대 규모의 산업 박람회(하노버 메세)가 열리며, 영국 왕실(하노버 왕가)과도 깊은 인연이 있는 도시입니다.", "Hannover"),
    "Nürnberg": ("뉘른베르크", "나치 전범 재판이 열렸던 역사적인 장소이자, 중세의 성곽과 세계 최고의 크리스마스 마켓으로 유명합니다.", "Nürnberg"),
    "Potsdam": ("포츠담", "프리드리히 대왕의 아름다운 여름 궁전인 '상수시 궁전'과 2차 대전 종전을 논의한 포츠담 회담의 무대입니다.", "Potsdam"),
    "Bonn": ("본", "통일 전 서독의 임시 수도였으며, 악성 베토벤이 태어나고 자란 음악의 성지입니다.", "Bonn"),
    "Heidelberg": ("하이델베르크", "독일에서 가장 오래된 대학이 있으며, 네카어 강변의 낭만적인 하이델베르크 성으로 유명한 대학 도시입니다.", "Heidelberg"),
    "Weimar": ("바이마르", "괴테와 실러가 활동한 독일 고전주의 문학의 중심지이자 바우하우스가 탄생한 예술의 성지입니다.", "Weimar"),
    "Wittenberg": ("비텐베르크", "마틴 루터가 95개조 반박문을 교회 문에 붙여 유럽의 역사를 바꾼 종교개혁의 발상지입니다.", "Wittenberg"),
    "Trier": ("트리어", "거대한 로마 시대의 성문 '포르타 니그라'가 남아있는 독일 최고(最古)의 도시이며, 카를 마르크스의 생가가 있습니다.", "Trier"),
    "Aachen": ("아헨", "신성로마제국의 카를 대제가 세운 아헨 대성당이 있으며, 오랫동안 독일 국왕들의 대관식이 열렸던 곳입니다.", "Aachen"),
    "Mainz": ("마인츠", "요하네스 구텐베르크가 세계 최초로 금속 활자를 발명해 인류의 정보 혁명을 이끈 도시입니다.", "Mainz"),
    "Münster": ("뮌스터", "치열했던 30년 종교전쟁을 끝내고 근대 국가의 기틀을 마련한 '베스트팔렌 조약'이 체결된 역사적인 도시입니다.", "Münster"),
    "Augsburg": ("아우크스부르크", "로마 시대부터 이어진 부유한 상업 도시로, 종교의 자유를 인정한 '아우크스부르크 화의'가 이루어진 곳입니다.", "Augsburg"),
    "Tübingen": ("튀빙겐", "철학자 헤겔과 천문학자 케플러가 거쳐간, 젊고 활기찬 분위기의 전통 깊은 대학 도시입니다.", "Tübingen"),
    "Lübeck": ("뤼벡", "중세 유럽 해상 무역을 지배했던 한자 동맹의 중심지이자, 토마스 만의 명작 '부덴브로크가의 사람들'의 배경입니다.", "Lübeck"),
    "Freiburg": ("프라이부르크", "아름다운 흑림(슈바르츠발트)의 관문이자, 태양광 발전으로 유명한 세계적인 친환경 생태 도시입니다.", "Freiburg im Breisgau")
}

with open('countries/germany/kreise.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

descriptions = {}
found_cities = set()

for feature in data['features']:
    eng_name = feature['properties'].get('NAME_3', '')
    type_3 = feature['properties'].get('TYPE_3', '')
    
    matched_key = None
    for k in cities_25.keys():
        if eng_name.startswith(k) or eng_name.startswith(k + ' ') or eng_name == k:
            matched_key = k
            break
            
    if not matched_key:
        if eng_name.startswith("Cologne"):
            matched_key = "Köln"
        elif eng_name.startswith("Nuremberg"):
            matched_key = "Nürnberg"
        elif eng_name.startswith("Munich"):
            matched_key = "München"
        elif eng_name.startswith("Hanover"):
            matched_key = "Hannover"
            
    if matched_key and matched_key not in found_cities:
        # Prefer Stadt/Kreisfreie Stadt unless it's the only one
        if 'Stadt' in type_3 or 'Stadt' in eng_name or 'Städt' in type_3 or 'Städt' in eng_name or eng_name == matched_key or matched_key in ["Tübingen", "Hanover", "Wittenberg", "Nürnberger Land"]:
            ko_name, desc, native_name = cities_25[matched_key]
            feature['properties']['isQuizRegion'] = True
            feature['properties']['name_ko'] = ko_name
            feature['properties']['nativeName'] = native_name
            feature['properties']['code'] = matched_key
            descriptions[matched_key] = desc
            found_cities.add(matched_key)
        else:
            feature['properties']['isQuizRegion'] = False
    else:
        feature['properties']['isQuizRegion'] = False

print(f"Found {len(found_cities)} / 25 cities.")
missing = set(cities_25.keys()) - found_cities
if missing:
    with open('missing.txt', 'w', encoding='utf-8') as f:
        f.write(str(missing))

with open('countries/germany/cities.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

with open('countries/germany/cities-descriptions.js', 'w', encoding='utf-8') as f:
    f.write("var REGION_DESCRIPTIONS = {\n")
    for k, v in descriptions.items():
        safe_v = v.replace('"', '\\"')
        f.write(f'    "{k}": "{safe_v}",\n')
    f.write("};\n")

print("Generated cities.json and cities-descriptions.js")
