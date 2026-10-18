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
        quizUnit: '도시',
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
                quizUnit: '도시',
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
                quizUnit: '도시',
                nationwideLabel: '15대 도시',
            }
        }
    ],

    // 이름을 골랐는데 그 도시가 지금 화면 밖에 있으면 지도를 축소하며 보여 줄 힌트
    zoomOutHints: {
        LPA: '🔍 라스팔마스는 본토에서 멀리 떨어진 섬에 있어요! 지도를 넓게 볼게요',
    },

    provinces: null
};
