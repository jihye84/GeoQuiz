var COUNTRY_CONFIG = {
    id: 'uk',
    name: '영국',
    emoji: '🇬🇧',
    
    // 지도 설정
    mapConfig: { width: 700, height: 900 },
    projection: 'mercator',
    ttsLang: 'en-GB',
    
    // 데이터 파일 경로
    dataFiles: {
        regions: 'countries/uk/cities.json',
        baseRegions: 'countries/uk/regions.json',
        provinces: null,
        descriptions: 'countries/uk/descriptions.js',
    },
    
    // TopoJSON 변환 설정 (모두 GeoJSON이므로 null)
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
        sidebarTitle: '영국 주요 도시/명소',
        quizUnit: '개 지역',
        nationwideLabel: '전체 주요 도시',
    },
    
    provinces: null
};
