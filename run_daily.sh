export LOG_FILE="/home/earlypay/src/project-capstone/daily_updates.log"

# 현재 날짜와 시간을 로그 파일에 기록
echo "===============================" >> "$LOG_FILE"
echo "Date: $(date)" >> "$LOG_FILE"
echo "===============================" >> "$LOG_FILE"

# update_aov.py 실행 (표준 출력과 에러 출력을 로그 파일에 추가)
python /home/earlypay/src/project-capstone/update/update_aov.py >> "$LOG_FILE" 2>&1

# update_week_aov.py 실행 (표준 출력과 에러 출력을 로그 파일에 추가)
python /home/earlypay/src/project-capstone/update/update_week_aov.py >> "$LOG_FILE" 2>&1
