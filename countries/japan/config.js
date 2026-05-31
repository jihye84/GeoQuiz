var COUNTRY_CONFIG = {
    id: 'japan',
    name: '일본',
    emoji: '🇯🇵',
    
    // 지도 설정
    mapConfig: { width: 800, height: 800 },
    projection: 'mercator',
    ttsLang: 'ja-JP',
    
    // 데이터 파일 경로
    dataFiles: {
        regions: 'countries/japan/cities.json',
        baseRegions: 'countries/japan/regions.json',
        provinces: null,
        descriptions: 'countries/japan/descriptions.js',
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
        sidebarTitle: '일본 주요 도시 퀴즈',
        quizUnit: '개 도시',
        nationwideLabel: '일본 20대 도시',
    },
    
    provinces: null
};
