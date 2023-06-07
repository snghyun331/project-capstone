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

![image01](https://github.com/snghyun331/project-capstone/assets/98893114/509361ac-6183-40b1-9446-146d385c90e1)

### 주요기능 

1. Data Insert : Database에 저장되어 있는 platform_sales 데이터를 elastic search index에 Insert한다.
2. Data Searching : elastic search의 특성으로 indexing을 통하여 정리해 놓은 data들을 Flask API를 통해 빠르게 검색하여 출력함
3. Data analysis : 이상 거래 탐지로 채권 운용의 리스크를 줄이기 위해서 platform_sales 데이터를 분석함
4. Data Visualization : 검색된 자료들을 kibana 프로그램을 사용하여 사용자가 시각적으로 자료를 분석할 수 있도록 시각 자료를 생성해 출력함


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


