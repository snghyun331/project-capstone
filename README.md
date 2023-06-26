# earlypay_capstone_project
운영 데이터 검색 및 분석 플랫폼 구축 

## 프로젝트 소개 

Elastic Stack을 기반으로 platform_sales 데이터를 이용해서 구축한 카드 내역 데이터 처리 플랫폼입니다. 

## 프로젝트 목표 

검색 엔진을 Elastic Stack을 기반으로 하여 target data 대상으로 data 분석이 가능한 infra/platform구축하여 실시간으로 수집, 저장, 분석, 시각화 자료를 제공

## 개발 기간 
- 23.03.06 - 23.06.19

## 기술스택
- Python 3.9.13
- Elastic search 7.17.0
- Kibana 7.17.0
- Flask 2.3.2

## Flask 배포

빈칸

## 기능 설명 / 순서  
### 기능 구상도 

![KakaoTalk_20230609_233221354](https://github.com/snghyun331/project-capstone/assets/108854903/5be55558-a4a1-4c74-8fdf-648ebb34d17a)

### 주요기능 

1. Data Insert : Database에 저장되어 있는 platform_sales 데이터를 elastic search index에 Insert한다.
2. Data Searching : elastic search의 특성으로 indexing을 통하여 정리해 놓은 data들을 Flask API를 통해 빠르게 검색하여 출력함
3. Data analysis : 이상 거래 탐지로 채권 운용의 리스크를 줄이기 위해서 platform_sales 데이터를 분석함
4. Data Visualization : 검색된 자료들을 kibana 프로그램을 사용하여 사용자가 시각적으로 자료를 분석할 수 있도록 시각 자료를 생성해 출력함

![image](https://github.com/snghyun331/project-capstone/assets/108854903/eaa81eb2-da9c-4673-b8f8-f2fe11280f96)


### 순서 

초기세팅

1. DB로부터 platform_sales 데이터를 Elasticsearch에 삽입 (외부)
- Elasticsearch에 삽입되기 전, 데이터에 대해서 이상 거래 데이터확인 

2. Elasticsearch에 저장된 데이터를 기반으로 구한 일일 객단가 계산, 삽입 (서버)

3. 계산된 일일 객단가로 **자정마다** 주간 객단가 계산, 삽입 (서버)
- 기능1의 기능4의 이상 데이터 확인을 위해 기능 수행

초기세팅 이후

4. DB의 최신 데이터를 **6시간 주기**로 Elasticsearch에 삽입 (외부)
- Elasticsearch에 삽입되기 전, 데이터에 대해서 이상 거래 데이터확인 

5. 최신화 데이터 일일 객단가를 **자정마다** 계산, 삽입 실행한다. (서버)

6. 최신화 데이터로 계산한 일일 객단가로 **자정마다** 주간 객단가 계산, 삽입 (서버)
- 기능1 과 기능4의 이상 데이터 확인을 위해 기능 수행
  
7. Kibana로 객단가 데이터 시각화 


### 프로젝트 산출물
**MySQL 운영 DB의 특정 데이터를 6시간마다 엘라스틱 서치에 동기화 (Crontab 이용, 외부에서 실행)**
![Untitled](https://github.com/snghyun331/project-capstone/assets/108854903/45d77614-b05a-4895-a020-944e139b11ee)

**최신화 데이터에 대한 일일 객단가를 자정마다 계산 및 동기화(서버에서 실행)**
![Untitled](https://github.com/snghyun331/project-capstone/assets/108854903/75210a9a-4441-47ce-928d-c63ffff70576)

**최신화 데이터로 계산한 일일 객단가를 활용하여, 자정마다 주간 객단가를 계산한 후 동기화 (서버에서 실행)**
![Untitled2](https://github.com/snghyun331/project-capstone/assets/108854903/2a4fc683-6760-4ddf-9f2e-a0b50910cd31)

**정상거래 정보에 대한 시각화 대시보드 생성**
![Untitled](https://github.com/snghyun331/project-capstone/assets/108854903/59538962-b0f8-469f-96d5-40c801cb9c40)

**이상거래 정보에 대한 시각화 대시보드 생성**
![Untitled](https://github.com/snghyun331/project-capstone/assets/108854903/0eaac6c0-4a59-4a9d-acc1-538281e9bdaa)

**flask를 이용해 엘라스틱 서치 데이터 조회(store_id가 50인 가게의 주객단가 정보 출력)**
![Untitled](https://github.com/snghyun331/project-capstone/assets/108854903/b2da6d6d-1472-4df4-9bd6-50ea9dbfbd10)

**flask를 이용해 엘라스틱 서치 데이터 조회(date가 2021-12-21인 모든 가게의 일일 객단가 정보 출력)**
![Untitled](https://github.com/snghyun331/project-capstone/assets/108854903/8b1c9fe8-eab6-484b-9d1c-0c23972cbf1b)





