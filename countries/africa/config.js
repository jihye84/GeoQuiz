var COUNTRY_CONFIG = {
    id: 'africa',
    name: '아프리카',
    emoji: '🌍',
    
    // 지도 설정
    mapConfig: { width: 800, height: 850 },
    projection: 'mercator',
    ttsLang: 'ko-KR', // 다양한 국가가 모여있으므로 한국어 발음으로 통일
    
    // 데이터 파일 경로
    dataFiles: {
        regions: 'countries/africa/regions.json',
        baseRegions: 'countries/africa/regions.json',
        provinces: null,
        descriptions: 'countries/africa/descriptions.js',
    },
    
    // TopoJSON 변환 설정
    topoConfig: {
        regions: null,
        provinces: null,
    },
    
    // 지역 계층 구조
    hierarchy: {
        hasProvinces: false,
        provinceCodeDigits: 0,
        regionCodeField: 'code', 
        regionNameField: 'name_ko',
    },
    
    // UI 라벨
    labels: {
        sidebarTitle: '아프리카 대륙 퀴즈',
        quizUnit: '국가',
        nationwideLabel: '아프리카 대륙',
    },
    
    // 모드 (난이도) 설정
    modes: [
        {
            id: 'top10',
            label: '핵심 주요 10개국',
            hierarchy: {
                hasProvinces: false,
                provinceCodeDigits: 0,
                regionCodeField: 'code', 
                regionNameField: 'name_ko',
                filter: (f) => f.properties.isTop10 === true
            },
            labels: {
                sidebarTitle: '아프리카 주요 10개국',
                quizUnit: '국가',
                nationwideLabel: '아프리카 10개국',
            }
        },
        {
            id: 'top25',
            label: '주요 25개국',
            hierarchy: {
                hasProvinces: false,
                provinceCodeDigits: 0,
                regionCodeField: 'code', 
                regionNameField: 'name_ko',
                filter: (f) => f.properties.isTop25 === true
            },
            labels: {
                sidebarTitle: '아프리카 주요 25개국',
                quizUnit: '국가',
                nationwideLabel: '아프리카 25개국',
            }
        },
        {
            id: 'all54',
            label: '전체 54개국',
            hierarchy: {
                hasProvinces: false,
                provinceCodeDigits: 0,
                regionCodeField: 'code', 
                regionNameField: 'name_ko',
                filter: (f) => true
            },
            labels: {
                sidebarTitle: '아프리카 전체 54개국',
                quizUnit: '국가',
                nationwideLabel: '아프리카 전체',
            }
        }
    ],
    
    provinces: null
};
