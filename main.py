from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 점수 변환 테이블
grade_to_point = {
    "A+": 4.5, "A0": 4.0,
    "B+": 3.5, "B0": 3.0,
    "C+": 2.5, "C0": 2.0,
    "D+": 1.5, "D0": 1.0,
    "F": 0.0
}

class Course(BaseModel):
    course_code: str
    course_name: str
    credits: int
    grade: str

class ScoreRequest(BaseModel):
    student_id: str
    name: str
    courses: List[Course]

@app.post("/score")
async def calculate_gpa(data: ScoreRequest):
    total_points = 0.0
    total_credits = 0

    for course in data.courses:
        if course.grade not in grade_to_point:
            raise HTTPException(status_code=400, detail=f"Invalid grade: {course.grade}")
        point = grade_to_point[course.grade]
        total_points += point * course.credits
        total_credits += course.credits

    if total_credits == 0:
        raise HTTPException(status_code=400, detail="No credits provided.")

    gpa = round(total_points / total_credits + 1e-8, 2)  # 소수점 3자리 반올림

    return {
        "student_summary": {
            "student_id": data.student_id,
            "name": data.name,
            "gpa": gpa,
            "total_credits": total_credits
        }
    }

from fastapi.responses import HTMLResponse

@app.get("/score", response_class=HTMLResponse)
async def score_info():
    return """
    <h2>📌 GPA 계산 API 안내</h2>
    <p>이 엔드포인트는 <strong>POST 방식</strong>으로 JSON 데이터를 받아 GPA를 계산합니다.</p>
    <pre>
    {
      "student_id": "2023123456",
      "name": "홍길동",
      "courses": [
        {"course_code": "I040-1", "course_name": "컴퓨터개론", "credits": 3, "grade": "A+"}
      ]
    }
    </pre>
    """

