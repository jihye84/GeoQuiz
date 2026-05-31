var COUNTRY_CONFIG = {
    id: 'korea',
    name: '대한민국',
    emoji: '🇰🇷',
    
    // 지도 설정
    mapConfig: { width: 700, height: 900 },
    projection: 'mercator',
    ttsLang: 'ko',
    
    // 데이터 파일 경로
    dataFiles: {
        regions: 'countries/korea/regions.json',
        provinces: 'countries/korea/provinces.json',
        descriptions: 'countries/korea/descriptions.js',
    },
    
    // TopoJSON 변환 설정
    topoConfig: {
        regions: null, // already GeoJSON
        provinces: { objectName: 'skorea_provinces_2018_geo' },
    },
    
    // 지역 계층 구조
    hierarchy: {
        hasProvinces: true,
        provinceCodeDigits: 2,
        regionCodeField: 'code',
        regionNameField: 'name',
    },
    
    // UI 라벨
    labels: {
        sidebarTitle: '시도 선택',
        quizUnit: '시군구',
        nationwideLabel: '전국 시도',
    },
    
    // 시도 목록
    provinces: [
        { code: '11', name: '서울특별시', short: '서울', color: '#f87171' },
        { code: '21', name: '부산광역시', short: '부산', color: '#38bdf8' },
        { code: '22', name: '대구광역시', short: '대구', color: '#fb923c' },
        { code: '23', name: '인천광역시', short: '인천', color: '#4ade80' },
        { code: '24', name: '광주광역시', short: '광주', color: '#facc15' },
        { code: '25', name: '대전광역시', short: '대전', color: '#a78bfa' },
        { code: '26', name: '울산광역시', short: '울산', color: '#2dd4bf' },
        { code: '29', name: '세종특별자치시', short: '세종', color: '#f472b6' },
        { code: '31', name: '경기도', short: '경기', color: '#34d399' },
        { code: '32', name: '강원특별자치도', short: '강원', color: '#60a5fa' },
        { code: '33', name: '충청북도', short: '충북', color: '#fbbf24' },
        { code: '34', name: '충청남도', short: '충남', color: '#c084fc' },
        { code: '35', name: '전북특별자치도', short: '전북', color: '#fb7185' },
        { code: '36', name: '전라남도', short: '전남', color: '#22d3ee' },
        { code: '37', name: '경상북도', short: '경북', color: '#818cf8' },
        { code: '38', name: '경상남도', short: '경남', color: '#f59e0b' },
        { code: '39', name: '제주특별자치도', short: '제주', color: '#a3e635' },
    ]
};
