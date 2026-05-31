var COUNTRY_CONFIG = {
    id: 'china',
    name: '중국',
    emoji: '🇨🇳',
    
    // 지도 설정
    mapConfig: { width: 900, height: 700 },
    projection: 'mercator',
    ttsLang: 'zh-CN',
    
    // 데이터 파일 경로
    dataFiles: {
        regions: 'countries/china/cities.json',
        baseRegions: 'countries/china/regions.json',
        provinces: null,
        descriptions: 'countries/china/descriptions.js',
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
        sidebarTitle: '중국 주요 도시 퀴즈',
        quizUnit: '개 도시',
        nationwideLabel: '중국 20대 도시',
    },
    
    provinces: null
};
