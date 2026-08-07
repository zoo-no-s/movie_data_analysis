# 🎥 영화 데이터 수집 및 분석
---
# 프로젝트 설명
---
웹 스크래핑과 API를 활용하여, 영화 데이터 확보 후 분석 진행.

# 데이터 출처
---
## Scrapping
* 출처 : https://cine21.com/
* robots.txt (2026년 8월 7일 기준)
```
User-agent: SemrushBot
Disallow: /
```

## API
* 출처 : http://www.kobis.or.kr/kobisopenapi
* 일일 박스 오피스 : http://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do?serviceId=searchDailyBoxOffice

# 📂 프로젝트 구조
---
* `data` : 데이터 모음
  * `raw` : 수집한 원본 데이터
  * `pre_processed` : 전처리 수행 파일
* `src` : 데이터 수집 및 전처리를 위한 코드 모음
* `notebooks` : 분석 진행 파일