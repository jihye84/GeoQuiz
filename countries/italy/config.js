var COUNTRY_CONFIG = {
    id: 'italy',
    name: '이탈리아',
    emoji: '🇮🇹',
    
    // 지도 설정
    mapConfig: { width: 700, height: 800 },
    projection: 'mercator',
    ttsLang: 'it-IT',
    
    // 데이터 파일 경로
    dataFiles: {
        regions: 'countries/italy/cities.json',
        baseRegions: 'countries/italy/regions.json',
        provinces: null,
        descriptions: 'countries/italy/descriptions.js',
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
        sidebarTitle: '이탈리아 주요 도시 퀴즈',
        quizUnit: '개 도시',
        nationwideLabel: '이탈리아 15대 도시',
    },
    
    provinces: null
};
