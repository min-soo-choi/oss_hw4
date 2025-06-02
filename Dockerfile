# 1. 베이스 이미지
FROM python:3.12-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. requirements.txt 복사 후 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 전체 프로젝트 복사
COPY . .

# 5. 앱 실행 (uvicorn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
