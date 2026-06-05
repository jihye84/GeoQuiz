var COUNTRY_CONFIG = {
    id: 'germany',
    name: '독일',
    emoji: '🇩🇪',
    
    // 기본 설정 (모든 모드 공통)
    mapConfig: { width: 700, height: 900 },
    projection: 'mercator',
    ttsLang: 'de-DE',
    
    // 게임 모드 설정
    modes: [
        {
            id: 'top5',
            label: '이지 모드 (핵심 5대 도시)',
            dataFiles: {
                regions: 'countries/germany/cities.json',
                baseRegions: 'countries/germany/regions.json',
                descriptions: 'countries/germany/cities-descriptions.js',
                provinces: null
            },
            topoConfig: {
                regions: null,
                baseRegions: null,
                provinces: null
            },
            hierarchy: {
                hasProvinces: false,
                provinceCodeDigits: 0,
                regionCodeField: 'code', 
                regionNameField: 'name_ko',
                filter: (f) => f.properties.isTop5 === true
            },
            labels: {
                sidebarTitle: '독일 핵심 5대 도시',
                quizUnit: '개 도시',
                nationwideLabel: '핵심 5대 도시',
            }
        },
        {
            id: 'states',
            label: '독일 16개 연방주 퀴즈',
            dataFiles: {
                regions: 'countries/germany/regions.json',
                descriptions: 'countries/germany/descriptions.js',
                provinces: null
            },
            topoConfig: {
                regions: null,
                provinces: null
            },
            hierarchy: {
                hasProvinces: false,
                provinceCodeDigits: 0,
                regionCodeField: 'code',
                regionNameField: 'name_ko',
            },
            labels: {
                sidebarTitle: '독일 연방주',
                quizUnit: '개 주',
                nationwideLabel: '전체 주',
            },
            provinces: null
        },
        {
            id: 'cities',
            label: '독일 25대 주요/역사 도시 퀴즈',
            dataFiles: {
                regions: 'countries/germany/cities.json',
                baseRegions: 'countries/germany/regions.json',
                descriptions: 'countries/germany/cities-descriptions.js',
                provinces: null
            },
            topoConfig: {
                regions: null,
                baseRegions: null,
                provinces: null
            },
            hierarchy: {
                hasProvinces: false,
                provinceCodeDigits: 0,
                regionCodeField: 'code',
                regionNameField: 'name_ko',
                filter: (f) => f.properties.isQuizRegion === true
            },
            labels: {
                sidebarTitle: '독일 주요 도시',
                quizUnit: '개 도시',
                nationwideLabel: '전체 도시',
            },
            provinces: null
        }
    ]
};
