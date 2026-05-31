var COUNTRY_CONFIG = {
    id: 'france',
    name: '프랑스',
    emoji: '🇫🇷',
    
    // 지도 설정
    mapConfig: { width: 700, height: 700 },
    projection: 'mercator',
    ttsLang: 'fr-FR',
    
    // 데이터 파일 경로
    dataFiles: {
        regions: 'countries/france/cities.json',
        baseRegions: 'countries/france/regions.json',
        provinces: null,
        descriptions: 'countries/france/descriptions.js',
    },
    
    // TopoJSON 변환 설정 (모두 GeoJSON)
    topoConfig: {
        regions: null,
        baseRegions: null,
        provinces: null,
    },
    
    // 지역 계층 구조
    hierarchy: {
        hasProvinces: false,
        provinceCodeDigits: 0,
        regionCodeField: 'code', 
        regionNameField: 'name_ko',
        filter: (f) => f.properties.isQuizRegion === true
    },
    
    // UI 라벨
    labels: {
        sidebarTitle: '프랑스 주요 도시 퀴즈',
        quizUnit: '개 도시',
        nationwideLabel: '프랑스 20대 도시',
    },
    
    provinces: null
};
