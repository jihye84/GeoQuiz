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
        quizUnit: '지역',
        nationwideLabel: '전체 주요 도시',
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
                quizUnit: '도시',
                nationwideLabel: '핵심 5대 도시',
            }
        },
        {
            id: 'all',
            label: '전체 모드 (전체 도시)',
            hierarchy: {
                hasProvinces: false,
                provinceCodeDigits: 0,
                regionCodeField: 'code', 
                regionNameField: 'name_ko',
                filter: (f) => f.properties.isQuizRegion === true
            },
            labels: {
                sidebarTitle: '전체 도시',
                quizUnit: '도시',
                nationwideLabel: '전체 도시',
            }
        }
    ],

    provinces: null
};
