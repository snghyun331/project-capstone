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

## 설치 방법 
 
1. 저장소를 클론합니다.

```
$ git clone https://github.com/snghyun331/project-capstone.git
```

2. 프로젝트의 디렉토리로 이동합니다. 

```
$ cd project-capstone
```

3. 가상환경을 만듭니다. 
 
```
$ python -m venv (가상환경 폴더명)
```
 
4. 가상환경을 활성화 합니다. 

```
$ .\(가상환경 폴더명)\Scripts\activate
```

5. 필요한 패키지를 설치합니다.

```
$ pip install -r freeze.txt
```

## Flask 배포

빈칸

## 기능 설명 / 순서  
### 주요기능 

1. Data Insert : Database에 저장되어 있는 platform_sales 데이터를 elastic search index에 Insert한다.
2. Data Searching : elastic search의 특성으로 indexing을 통하여 정리해 놓은 data들을 Flask API를 통해 빠르게 검색하여 출력함
3. Data Visualization : 검색된 자료들을 kibana 프로그램을 사용하여 사용자가 시각적으로 자료를 분석할 수 있도록 시각 자료를 생성해 출력함


### 순서 

초기세팅

1. DB로부터 platform_sales 데이터를 Elasticsearch에 삽입 (외부)
- Elasticsearch에 삽입되기 전, 데이터에 대해서 이상거래 데이터확인 

2. Elasticsearch에 저장된 데이터를 기반으로 구한 일일 객단가 계산, 삽입 (서버)

3. 계산된 일일 객단가로 주간 객단가 계산, 삽입 (서버)
- 기능1의 기능4의 이상 데이터 확인을 위해 기능 수행

초기세팅 이후

4. DB의 최신 데이터를 **6시간 주기**로 Elasticsearch에 삽입 (외부)
- Elasticsearch에 삽입되기 전, 데이터에 대해서 이상거래 데이터확인 

5. 최신화 데이터 일일 객단가를 **자정마다** 계산, 삽입 실행한다. (서버)

6. 최신화 데이터로 계산한 일일 객단가로 주간 객단가 계산, 삽입 (서버)
- 기능1 과 기능4의 이상 데이터 확인을 위해 기능 수행
  
7. Kibana로 객단가 데이터 시각화 

## 라이선스 

- Python은 Python 소프트웨어 재단 라이선스를 따릅니다. [Python 소프트웨어 재단 라이선스](https://www.python.org/psf/license/)를 확인하십시오.
- Elasticsearch와 Kibana는 Apache 2.0 라이선스를 따릅니다. [Apache 2.0 라이선스](https://www.apache.org/licenses/LICENSE-2.0)를 확인하십시오.
- Flask는 BSD 라이선스를 따릅니다. [BSD 라이선스](https://github.com/pallets/flask/blob/main/LICENSE.rst)를 확인하십시오.
- MySQL Community Edition은 GNU General Public License (GPL) 버전 2를 따릅니다. [GPLv2 라이선스](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)를 확인하십시오.

