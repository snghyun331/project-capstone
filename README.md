# earlypay_capstone_project
ELK + Flask 데이터 처리 시스템 구축 

## 프로젝트 소개 
platform_sales 데이터를 이용해서 만든 카드 내역 데이터 처리 시스템입니다. 

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
$ git crone -b folder_cleaned https://github.com/snghyun331/project-capstone.git
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

4. 필요한 패키지를 설치합니다.

```
$ pip freeze > freeze.txt
```

또는

```
$ pip install -r freeze.txt
```

## 기능 설명 

기능 1. Mysql로부터 데이터를 ELK로 가져






















"""
# project-capstone

# [실행순서] 

## 1

### conn.py 
 - 기능 : elasticsearch의 연결

### aov_compare.py
 - 기능 : 데이터의 이상치 검사 
 - 함수 : compare(card_number, amount_sale, store_id, start_date, end_date)
 - 조건 : 주간 객단가의 2배보다 크면서, 데이터의 card_number가 같은 데이터가 amount_sale가 3번 이상 같은 경우 이상치로 간주.

## 2

### es.connection.py 
1. 기능 : DB에서 ELK로 데이터를 이동
2. 함수 : insert_sale(start_date, end_date)
3. 전개 :

 - es = conn.Conn() : 'conn.py' 사용자 정의 모듈로 elasticsearch와 연결 
 - DB에 있는 데이터를 pymysql 라이브러리로 조회 후 'platform_sales' 인덱스의 mappings에 맞게 데이터 지정, data_row 리스트에 추가.
 - cmp.compare() : 'aov_compare.py' 사용자 정의 모듈로 이상치이면 fraud_data 리스트에도 추가.
 - 만약 data_row의 길이가 100 이상이면 데이터를 'platform_sales'인덱스에 추가하고 data_row는 초기화.
 - fraud_data의 길이가 100 이상이면 'platform_fraud_sales' 인덱스에 데이터 추가하고 fraud_data는 초기화.
 - DB에 있는 데이터를 platform_sales 인덱스에 추가 
 - DB에서 데이터를 모두 받아온 후 data_row와 fraud_data에 데이터가 존재한다면 각각의 인덱스에 추가.
  
### daily_aov.py 
1. 기능 : 일일 객단가 계산
2. 함수 : make_AOV(year, month, day), AOV(start_date, end_date)
3. 전개 : 

  make_AOV() 함수
  * 해당 날짜에 존재하는 'platform_sales'의 데이터를 가져와 일일 객단가를 구하기 위한 함수
  * 객단가 = (가게의 총 결제 금액) / (가게의 손님의 수) 
  * 'platform_sales'에서 해당 날짜에 결제된(sold_at) 데이터를 모두 가져온다. 
  * 가져온 데이터로 해당일에 결제된 각각의 가게(store_id)의 일일 객단가를 구하기 위해 store_id 리스트를 만들어 중복이 되지 않게 저장한다. 
  * 해당일에 가게별로 결제한 손님의 수를 구하기 위해 가게(store_id)와 카드 번호(card_number)를 키:값으로 하여 store_id가 같은 값의 갯수를 구하여                         num_customer 딕셔너리에 store_id, len(고객수)를 키:값으로 저장.
  * 가게의 총 결제 금액도 필요하므로, store_id와 가게별 amount_sale의 합계를 키:값으로 정해 total_sales 딕셔너리에 저장
  * store_id, num_customer 딕셔너리, total_sales 딕셔너리를 이용하여 가게별 객단가(aov)를 구해 store_id와 aov를 키:값으로 unit_price 딕셔너리에 저장. 
  * data 딕셔너리를 'platform_sales_per_price' 인덱스와 필드를 같게 만들어 store_id, total_sale, num_customer, unit_price값 저장.
  * data 딕셔너리를 DataFrame으로 만들고(df), 해당 날짜의 데이터를 넣는 'date' 필드 추가. 
  * 만든 df은 AOV에 리턴.
  
  AOV() 함수 
  * 일일 객단가를 구하고 싶은 시작 날짜(start_date)와 끝 날짜(end_date)를 인자로 한다.
  * current_date는 start_date에서 end_date까지의 날짜 데이터를 얻기 위한 변수
  * 이후에 'platform_sales_per_price' 인덱스에 저장하기 편하게 하도록 result_df 데이터프레임을 만들어 둔다.
  * current_date를 년, 월, 일로 나눠 make_AOV()함수의 인자로 사용, 리턴값은 df에 저장 
  * make_AOV() 함수를 실행하고 리턴받은 값 df는 result_df와 합친다. 
  * current_date를 하루 증가시켜 end_date가 될때까지 make_AOV() 실행하고 df는 result_df와 합친다. 
  * 최종적으로 result_df는 start_date부터 end_date까지 일일 객단가를 구한 DataFrame이 된다. 
          
### initial_aov.py 
1. 기능 : daily_aov.py 에서 계산된 일일 객단가 을 ELK로 이동 
2. 함수 : insert_daily_aov(es, aov_df)
3. 전개 : 

  insert_daily_aov() 함수
  *  conn.py의 클래스 선언(es)과 daily_aov.py의 리턴값인 result_df(aov_df)을 인자로 한다.
  *  인덱스 'platform_sales_per_price'에 데이터를 추가하기 위한 함수
  *  aov_df를 한행 씩 data_row 리스트에 추가한다. 
  *  만약 data_row의 길이가 100 이상이면 'platform_sales_per_price'에 data_row의 데이터를 추가한다. 
  *  aov_df의 데이터를 모두 받아온 후 data_row에 데이터가 존재한다면 나머지 데이터도 'platform_sales_per_price'에 추가한다.
 - 이는 매일 한번씩 실행된다. 

### week_aov.py 
1. 기능 : 주간 객단가 계산 
2. 함수 : make_week_AOV(es, date, store_id), Week_AOV(es, start_date, end_date)
3. 전개 : 

  make_week_AOV() 함수
  * 해당 날짜로 부터 7일전까지의 객단가의 평균을 구하기 위한 함수 
  * conn.py의 ELK 연결(es), 날짜(date), 가게(store_id)를 인자로 한다.  
  * 주간 객단가의 평균을 구하기 위해 'platform_sales_per_price' 인덱스를 7일 전까지의 데이터를 가져온다. 
  * store_id가 일치한 객단가 정보를 찾아 7일치의 총 amount_sale의 합(total_sale)과 num_customer의 합(num_customer)을 구한다.
  * 'platform_sales_week_per_price' 인덱스에 저장하기 위해 필드가 일치하는 데이터 프레임(df) 생성
  * total_sale과 num_customer을 이용하여 해당 날짜(date)에 해당 가게(store_id)의 주간 객단가(week_aov)를 구한다. 
  * store_id, date, week_aov를 이용하여 df에 넣을 data 딕셔너리 생성. 
  * 생성한 data 딕셔너리로 df에 행 추가. Week_AOV() 함수에 리턴
  
  Week_AOV() 함수 
  * make_week_AOV() 함수를 실행하기 위한 인자를 생성하는 함수,
  * coon.py의 ELK 연결(es), 시작 날짜(start_date), 끝 날짜(end_date)를 인자로 한다. 하지만 start_date와 end_date는 같은 값으로 한다. 
  * start_date와 end_date를 이용해서 'platform_sales_per_price' 인덱스에서 데이터를 가져온다. 이때 날짜별로 정렬하면서 가져온다. 
  * 'platform_sales_week_per_price' 인덱스에 저장하기 위해 필드에 맞게 데이터 프레임(result_df)생성
  * current_date는 start_date에서 end_date까지의 날짜 데이터를 얻기 위한 변수
  * current_date에 존재하는 일일 객단가 데이터의 가게 코드를 가져와 중복을 제거하고 리스트로 저장한다.(store_id)
  * store_id 리스트의 값을 es, current_date와 함께 make_week_AOV() 함수 실행하고 리턴받은 값을 df 변수에 저장 리턴받은 값 df를 result_df와 합친다. 그리고 이를 store_id 값 전부 실행한다. 
  * 그리고 current_date의 날짜를 하루 추가해 store_id 리스트를 날짜에 맞는 값을 불러와 make_week_AOV() 함수를 실행하여 result_df와 합친다.
  * 최종적으로 result_df는 start_date와 end_date사이에 있는 값들의 주간 객단가의 평균 정보를 저장하게 된다. 

### initial_week_aov.py 
1. 기능 : week_aov.py에서 계산된 주간 객단가 값을 ELK로 이동 
2. 함수 : insert_weekly_aov(es, aov_df):
3. 전개 : 

  insert_weekly_aov()
"""
















