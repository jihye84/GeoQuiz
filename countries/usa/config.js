var COUNTRY_CONFIG = {
    id: 'usa',
    name: '미국',
    emoji: '🇺🇸',
    
    // 지도 설정
    mapConfig: { width: 975, height: 610 },
    projection: 'albersUsa',
    ttsLang: 'en-US',
    
    modes: [
        {
            id: 'states',
            label: '미국 50개 주 퀴즈',
            dataFiles: {
                regions: 'countries/usa/states.json',
                provinces: null,
                descriptions: 'countries/usa/descriptions.js',
            },
            topoConfig: {
                regions: { objectName: 'states' },
                provinces: null,
            },
            hierarchy: {
                hasProvinces: false,
                provinceCodeDigits: 0,
                regionCodeField: 'code',
                regionNameField: 'name_ko',
            },
            labels: {
                sidebarTitle: '미국 주',
                quizUnit: '개 주',
                nationwideLabel: '전체 50개 주',
            },
            provinces: null
        },
        {
            id: 'cities-west',
            label: '미국 서부 주요 도시 퀴즈',
            dataFiles: {
                regions: 'countries/usa/cities.json',
                baseRegions: 'countries/usa/states.json',
                provinces: null,
                descriptions: 'countries/usa/cities-descriptions.js',
            },
            topoConfig: {
                regions: null,
                baseRegions: { objectName: 'states' },
                provinces: null,
            },
            hierarchy: {
                hasProvinces: false,
                provinceCodeDigits: 0,
                regionCodeField: 'code',
                regionNameField: 'name_ko',
                filter: (f) => f.properties.region === 'west'
            },
            labels: {
                sidebarTitle: '미국 서부 도시',
                quizUnit: '개 도시',
                nationwideLabel: '서부 주요 도시',
            },
            provinces: null
        },
        {
            id: 'cities-central',
            label: '미국 중부 주요 도시 퀴즈',
            dataFiles: {
                regions: 'countries/usa/cities.json',
                baseRegions: 'countries/usa/states.json',
                provinces: null,
                descriptions: 'countries/usa/cities-descriptions.js',
            },
            topoConfig: {
                regions: null,
                baseRegions: { objectName: 'states' },
                provinces: null,
            },
            hierarchy: {
                hasProvinces: false,
                provinceCodeDigits: 0,
                regionCodeField: 'code',
                regionNameField: 'name_ko',
                filter: (f) => f.properties.region === 'central'
            },
            labels: {
                sidebarTitle: '미국 중부 도시',
                quizUnit: '개 도시',
                nationwideLabel: '중부 주요 도시',
            },
            provinces: null
        },
        {
            id: 'cities-east',
            label: '미국 동부 주요 도시 퀴즈',
            dataFiles: {
                regions: 'countries/usa/cities.json',
                baseRegions: 'countries/usa/states.json',
                provinces: null,
                descriptions: 'countries/usa/cities-descriptions.js',
            },
            topoConfig: {
                regions: null,
                baseRegions: { objectName: 'states' },
                provinces: null,
            },
            hierarchy: {
                hasProvinces: false,
                provinceCodeDigits: 0,
                regionCodeField: 'code',
                regionNameField: 'name_ko',
                filter: (f) => f.properties.region === 'east'
            },
            labels: {
                sidebarTitle: '미국 동부 도시',
                quizUnit: '개 도시',
                nationwideLabel: '동부 주요 도시',
            },
            provinces: null
        }
    ]
};
