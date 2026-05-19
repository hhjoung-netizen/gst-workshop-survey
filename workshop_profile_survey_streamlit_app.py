import streamlit as st
import pandas as pd
import os

# 페이지 설정
st.set_page_config(page_title="팀 역량 및 협업 설문 시스템", layout="wide")

# 데이터 저장 파일 경로
DATA_FILE = "survey_results.csv"

# [누락 없는 30개 전체 설문 문항 구성] 
# 유형별로 각 5~6문항씩 총 30문항을 셋팅했습니다. 문항 텍스트는 필요시 따옴표 내부만 수정하시면 됩니다.
SURVEY_QUESTIONS = [
    # 1. 소통 (Communication) - 6문항
    {"유형": "소통", "문항": "우리 팀은 업무 관련 정보와 지식을 서로 투명하고 신속하게 공유합니까?"},
    {"유형": "소통", "문항": "팀원들은 동료의 의견을 경청하며, 비난 없이 건설적인 피드백을 주고받습니까?"},
    {"유형": "소통", "문항": "팀 내에서 자신의 의견이나 제안을 자유롭고 솔직하게 표현할 수 있습니까?"},
    {"유형": "소통", "문항": "업무 지시나 요청 사항이 모호하지 않고 명확하게 전달됩니까?"},
    {"유형": "소통", "문항": "회의는 목적이 명확하며, 모든 참석자가 적극적으로 의견을 개진하는 분위기입니까?"},
    {"유형": "소통", "문항": "감정적인 대립을 지양하고 업무 중심의 이성적인 소통이 이루어지고 있습니까?"},

    # 2. 협업 (Collaboration) - 6문항
    {"유형": "협업", "문항": "팀 목표 달성을 위해 개인이나 파트 간의 경계를 넘어 적극적으로 협력합니까?"},
    {"유형": "협업", "문항": "각 팀원의 역할과 책임(R&R)이 명확하게 분담되어 있습니까?"},
    {"유형": "협업", "문항": "동료가 업무 과부하로 어려움을 겪을 때 자발적으로 도와주는 문화가 있습니까?"},
    {"유형": "협업", "문항": "팀원 간의 역량과 전문성을 신뢰하고 업무를 맡깁니까?"},
    {"유형": "협업", "문항": "협업 과정에서 발생하는 결과물이나 성과가 공정하게 공유된다고 생각하십니까?"},
    {"유형": "협업", "문항": "타 부서나 외부 파트너와의 협업이 유기적이고 원활하게 진행됩니까?"},

    # 3. 갈등관리 (Conflict Management) - 6문항
    {"유형": "갈등관리", "문항": "의견 충돌이나 갈등이 발생했을 때 이를 피하지 않고 직시하여 해결하려고 합니까?"},
    {"유형": "갈등관리", "문항": "갈등 해결 과정에서 특정 개인의 일방적인 양보가 아닌 윈-윈(Win-Win) 방안을 모색합니까?"},
    {"유형": "갈등관리", "문항": "팀 내 갈등이 발생했을 때 리더나 제3자가 중재 역할을 적절히 수행합니까?"},
    {"유형": "갈등관리", "문항": "과거의 갈등이나 앙금이 현재의 업무 협업에 악영향을 미치지 않습니까?"},
    {"유형": "갈등관리", "문항": "서로 다른 일하는 방식이나 성향의 차이를 인정하고 존중합니까?"},
    {"유형": "갈등관리", "문항": "실수나 실패를 책망하기보다 원인을 분석하고 함께 대안을 찾는 분위기입니까?"},

    # 4. 리더십 및 방향성 (Leadership) - 6문항
    {"유형": "리더십", "문항": "우리 팀의 단기/장기 목표와 비전이 명확히 제시되고 있습니까?"},
    {"유형": "리더십", "문항": "리더는 의사결정을 합리적이고 타이밍에 맞게 내리고 있습니까?"},
    {"유형": "리더십", "문항": "팀원들의 성장과 역량 개발을 위한 피드백 및 기회가 적절히 제공됩니까?"},
    {"유형": "리더십", "문항": "리더는 팀원들의 애로사항이나 고충을 경청하고 해결하기 위해 노력합니까?"},
    {"유형": "리더십", "문항": "업무 성과에 대한 인정과 보상(칭찬, 격려 포함)이 적절하게 이루어집니까?"},
    {"유형": "리더십", "문항": "리더는 공정하고 일관성 있는 기준에 따라 팀을 운영합니까?"},

    # 5. 조직문화 및 몰입 (Culture & Engagement) - 6문항
    {"유형": "조직문화", "문항": "우리 팀은 새로운 아이디어나 업무 방식을 시도하는 것에 개방적입니까?"},
    {"유형": "조직문화", "문항": "불필요한 보고나 형식적인 절차 없이 효율적으로 일하는 문화가 정착되어 있습니까?"},
    {"유형": "조직문화", "문항": "팀원들은 자신이 하고 있는 업무에 대해 자부심과 책임감을 느낍니까?"},
    {"유형": "조직문화", "문항": "적절한 업무량과 유연성을 통해 일과 삶의 균형(Work-Life Balance)을 유지하고 있습니까?"},
    {"유형": "조직문화", "문항": "팀 내에 심리적 안정감이 형성되어 있어 모르는 것을 편하게 물어볼 수 있습니까?"},
    {"유형": "조직문화", "문항": "현재 우리 팀의 전반적인 사기와 업무 몰입도는 높은 편입니까?"}
]

# 데이터 로드 함수
def load_results():
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["일시", "이름", "팀명", "유형", "문항", "점수"])

# 데이터 저장 함수
def save_results(new_rows):
    df = load_results()
    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

# 사이드바 메뉴 네비게이션
st.sidebar.title("📋 프로젝트 메뉴")
menu = st.sidebar.radio("화면 이동", ["📝 설문 참여하기", "📊 관리자 대시보드"])

# --- 화면 1: 설문 참여하기 ---
if menu == "📝 설문 참여하기":
    st.title("📝 팀 성향 및 협업 설문조사")
    st.write("모든 문항(총 30문항)을 읽고 본인의 생각을 솔직하게 점수로 선택해 주세요.")
    st.caption("💡 1점: 전혀 아님 | 2점: 아님 | 3점: 보통 | 4점: 그렇음 | 5점: 매우 그렇음")
    
    st.subheader("👤 참여자 정보 입력")
    col1, col2 = st.columns(2)
    with col1:
        user_name = st.text_input("이름", placeholder="예: 홍길동")
    with col2:
        team_name = st.text_input("소속 팀명", placeholder="예: 개발팀, 인사팀")
        
    st.divider()
    st.subheader("✍️ 설문 문항 (30문항)")
    
    # 응답 저장용 딕셔너리
    user_responses = {}
    
    # 30개 문항 루프 실행
    for idx, item in enumerate(SURVEY_QUESTIONS):
        st.markdown(f"**Q{idx+1}. [{item['유형']}] {item['문항']}**")
        score = st.radio(
            f"점수 선택 (Q{idx+1})", 
            options=[1, 2, 3, 4, 5], 
            index=2, # 기본값 3점(보통)
            horizontal=True, 
            key=f"q_{idx}"
        )
        user_responses[idx] = score
        st.write("") # 간격 띄우기
        
    st.divider()
    
    # 제출 버튼
    if st.button("설문 최종 제출하기", type="primary", use_container_width=True):
        if not user_name.strip() or not team_name.strip():
            st.error("⚠️ 오류: 이름과 소속 팀명을 반드시 입력하셔야 설문을 제출할 수 있습니다.")
        else:
            current_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            new_data_list = []
            
            # 30개 문항에 대한 응답을 행 데이터로 빌드
            for idx, item in enumerate(SURVEY_QUESTIONS):
                new_data_list.append({
                    "일시": current_time,
                    "이름": user_name,
                    "팀명": team_name,
                    "유형": item["유형"],
                    "문항": item["문항"],
                    "점수": user_responses[idx]
                })
            
            save_results(new_data_list)
            st.balloons()
            st.success(f"🎉 성공적으로 제출되었습니다! 감사합니다, {user_name}님.")

# --- 화면 2: 관리자 대시보드 ---
elif menu == "📊 관리자 대시보드":
    st.title("📊 팀 설문 결과 통합 분석 대시보드")
    
    df_res = load_results()
    
    if df_res.empty:
        st.warning("📥 수집된 설문 데이터가 없습니다. 먼저 [설문 참여하기] 탭에서 설문을 진행해 주세요.")
    else:
        # 0. 상단 KPI 요약
        total_p = df_res["이름"].nunique()
        total_t = df_res["팀명"].nunique()
        
        kpi1, kpi2 = st.columns(2)
        kpi1.metric("총 설문 응답자 수", f"{total_p} 명")
        kpi2.metric("진단 참여 팀 수", f"{total_t} 개 팀")
        st.divider()
        
        # 1. 5대 유형별 평균 점수 차트
        st.subheader("💡 1. 5대 역량 유형별 평균 점수")
        type_avg = df_res.groupby("유형")["점수"].mean().reset_index()
        # 가독성을 위해 점수순으로 정렬
        type_avg = type_avg.sort_values(by="점수", ascending=False)
        st.bar_chart(data=type_avg, x="유형", y="점수", use_container_width=True)
        
        # 2. 팀 강점 및 약점 분석 (Top 3 / Bottom 3 문항 추출)
        st.subheader("💪 2. 팀 내부 강점 및 ⚠️ 잠재적 약점 요인 (문항별)")
        q_avg = df_res.groupby(["유형", "문항"])["점수"].mean().reset_index().sort_values(by="점수", ascending=False)
        
        c1, c2 = st.columns(2)
        with c1:
            st.success("🔥 우리 팀의 주요 강점 (평균 상위 3개 항목)")
            for i, row in q_avg.head(3).iterrows():
                st.write(f"- **[{row['유형']}]** {row['문항']} \n  👉 **평균 {row['점수']:.2f}점**")
        with c2:
            st.error("🚨 우리 팀의 관리 필요 약점 (평균 하위 3개 항목)")
            # 하위 항목은 역순으로 보여줌
            for i, row in q_avg.tail(3).iloc[::-1].iterrows():
                st.write(f"- **[{row['유형']}]** {row['문항']} \n  👉 **평균 {row['점수']:.2f}점**")
                
        st.divider()
        
        # 3. 협업 리스크 진단 (부정 평가 비율 점검)
        st.subheader("⚡ 3. 협업 리스크 관리 요인")
        risk_threshold = 2.5
        low_scores = df_res[df_res["점수"] <= risk_threshold]
        
        if not low_scores.empty:
            st.warning(f"⚠️ 전체 답변 중 부정적 평가({risk_threshold}점 이하)를 받은 리스크 항목이 총 {len(low_scores)}건 발견되었습니다.")
            risk_summary = low_scores.groupby("유형").size().reset_index(name="리스크 감지 건수(문항 수)").sort_values(by="리스크 감지 건수(문항 수)", ascending=False)
            st.dataframe(risk_summary, use_container_width=True, hide_index=True)
        else:
            st.info("🎉 안심 항목: 모든 문항과 유형에서 협업 리스크가 감지되지 않았으며 점수가 안정적입니다.")
            
        st.divider()
        
        # 4. 로 데이터 테이블 및 내보내기 기능
        st.subheader("📋 4. 팀원별 설문 상세 raw data")
        st.dataframe(df_res, use_container_width=True)
        
        # 엑셀 깨짐 방지를 위한 utf-8-sig 인코딩 적용
        csv_data = df_res.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="📥 전체 결과 CSV 파일 다운로드", 
            data=csv_data, 
            file_name="team_survey_total_results.csv", 
            mime="text/csv"
        )
