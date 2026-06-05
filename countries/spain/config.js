var COUNTRY_CONFIG = {
    id: 'spain',
    name: '스페인',
    emoji: '🇪🇸',
    
    // 지도 설정
    mapConfig: { width: 800, height: 600 },
    projection: 'mercator',
    ttsLang: 'es-ES',
    
    // 데이터 파일 경로
    dataFiles: {
        regions: 'countries/spain/cities.json',
        baseRegions: 'countries/spain/regions.json',
        provinces: null,
        descriptions: 'countries/spain/descriptions.js',
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
        sidebarTitle: '스페인 주요 도시 퀴즈',
        quizUnit: '개 도시',
        nationwideLabel: '스페인 15대 도시',
    },
    
        // 모드 (난이도) 설정
    modes: [
        {
            id: 'top5',
            label: '이지 모드 (핵심 5대 도시)',
            hierarchy: {
                hasProvinces: false,
                provinceCodeDigits: 0,
                regionCodeField: 'code', 
                regionNameField: 'name_ko',
                filter: (f) => f.properties.isTop5 === true
            },
            labels: {
                sidebarTitle: '핵심 5대 도시',
                quizUnit: '개 도시',
                nationwideLabel: '핵심 5대 도시',
            }
        },
        {
            id: 'all',
            label: '전체 모드 (15대 도시)',
            hierarchy: {
                hasProvinces: false,
                provinceCodeDigits: 0,
                regionCodeField: 'code', 
                regionNameField: 'name_ko',
                filter: (f) => f.properties.isQuizRegion === true
            },
            labels: {
                sidebarTitle: '15대 도시',
                quizUnit: '개 도시',
                nationwideLabel: '15대 도시',
            }
        }
    ],

    provinces: null
};
