import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(
    page_title="업무 스타일 프로파일링 설문",
    layout="centered"
)

st.title("📋 업무 스타일 프로파일링 설문")
st.markdown("""
본 설문은 워크샵 진행을 위한 업무 스타일 프로파일링 목적입니다.  
문항별로 가장 본인과 가까운 답변 1개를 선택해주세요.
""")

# 기본 정보
st.header("기본 정보")
name = st.text_input("이름")
department = st.text_input("부서")
position = st.selectbox(
    "직급",
    ["사원", "대리", "과장", "차장", "부장", "기타"]
)

# 유형 매핑
mapping = {
    "분석": "분석형",
    "실행": "실행형",
    "협업": "협업형",
    "체계": "체계형"
}

questions = [
    {
        "question": "Q1. 문제가 발생했을 때 가장 먼저 하는 행동은?",
        "options": {
            "데이터를 확인한다": "분석",
            "우선 빠르게 조치한다": "실행",
            "관련자들과 소통한다": "협업",
            "절차와 이력을 확인한다": "체계"
        }
    },
    {
        "question": "Q2. 업무를 받을 때 선호하는 방식은?",
        "options": {
            "근거와 배경 포함 설명": "분석",
            "핵심만 빠르게 전달": "실행",
            "대화 중심 설명": "협업",
            "문서 및 절차 기준 설명": "체계"
        }
    },
    {
        "question": "Q3. 회의에서 나는 주로?",
        "options": {
            "논리와 데이터를 제시한다": "분석",
            "결론을 빠르게 정리한다": "실행",
            "분위기를 조율한다": "협업",
            "회의 내용을 기록한다": "체계"
        }
    },
    {
        "question": "Q4. 업무 스트레스를 가장 많이 받는 상황은?",
        "options": {
            "데이터 부족": "분석",
            "결정 지연": "실행",
            "갈등 상황": "협업",
            "기준 없는 변경": "체계"
        }
    },
    {
        "question": "Q5. 선호하는 업무 스타일은?",
        "options": {
            "분석 중심": "분석",
            "실행 중심": "실행",
            "협업 중심": "협업",
            "체계 중심": "체계"
        }
    }
]

responses = {}

st.header("프로파일링 문항")

for idx, q in enumerate(questions):
    answer = st.radio(
        q["question"],
        list(q["options"].keys()),
        key=f"q_{idx}"
    )
    responses[q["question"]] = answer

if st.button("설문 제출"):

    if not name or not department:
        st.error("이름과 부서를 입력해주세요.")

    else:
        score = {
            "분석": 0,
            "실행": 0,
            "협업": 0,
            "체계": 0
        }

        for idx, q in enumerate(questions):
            selected = responses[q["question"]]
            result_type = q["options"][selected]
            score[result_type] += 1

        final_type = max(score, key=score.get)

        result = {
            "제출시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "이름": name,
            "부서": department,
            "직급": position,
            "결과유형": mapping[final_type]
        }

        for q in questions:
            result[q["question"]] = responses[q["question"]]

        file_name = "survey_results.csv"

        df = pd.DataFrame([result])

        if os.path.exists(file_name):
            df.to_csv(file_name, mode='a', header=False, index=False, encoding='utf-8-sig')
        else:
            df.to_csv(file_name, index=False, encoding='utf-8-sig')

        st.success("설문이 제출되었습니다.")

        st.subheader("📊 분석 결과")
        st.write(f"### {mapping[final_type]}")

        st.write("#### 유형별 점수")
        st.write(score)

        st.info("응답 결과는 자동 저장되었습니다.")

st.markdown("---")
st.caption("GST 품질팀 워크샵용 프로파일링 설문")

# 실행 방법 안내
st.sidebar.title("실행 방법")
st.sidebar.markdown("""
### 1. 라이브러리 설치
```bash
pip install streamlit pandas
```

### 2. 실행
```bash
streamlit run app.py
```

### 3. 배포 추천
- Streamlit Cloud
- 사내 서버
- Azure App Service
- Teams 공유

배포 후 생성된 URL을 팀원들에게 공유하면 됩니다.
""")
