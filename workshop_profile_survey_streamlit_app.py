import streamlit as st
import pandas as pd
import os

# 페이지 설정
st.set_page_config(page_title="품질혁신팀 업무 스타일 프로파일링 시스템", layout="wide")

# ==========================================
# [관리자 설정] 🔑 원하는 비밀번호를 여기에 적어주세요!
# ==========================================
ADMIN_PASSWORD = "123!"

# 데이터 저장 파일 경로
DATA_FILE = "survey_results.csv"

# [첨부파일 기반] 유형별 상세 매칭 딕셔너리 데이터베이스
TYPE_DETAILS = {
    "분석형": {
        "특징": "데이터 중심 사고\n정확성 중시\n논리적 판단 선호\n세부 검토 성향\n근거 기반 커뮤니케이션",
        "강점": "원인 분석 능력 우수\n리스크 검토 능력\n객관적 판단 가능\n오류 발견 능력 우수\n품질 안정화 강점",
        "주의점": "의사결정이 느려질 수 있음\n완벽주의 성향 가능\n유연성이 부족해 보일 수 있음\n지나친 검토 가능\n감정 표현 부족 가능",
        "추천역할": "원인 분석\n품질 데이터 관리\n품질 지표 관리\n검사 기준 관리\nAudit 대응",
        "협업팁": "충분한 데이터 제공\n근거 중심 설명\n변경 사항 사전 공유\n명확한 기준 제시\n충분한 검토 시간 제공",
        "스트레스": "근거 없이 의사결정이 진행될 때\n갑작스럽게 기준이나 일정이 변경될 때\n충분한 검토 없이 빠른 실행만 요구받을 때"
    },
    "실행형": {
        "특징": "빠른 실행 선호\n결과 중심 사고\n목표 달성 지향\n즉각 대응 성향\n의사결정 속도 빠름",
        "강점": "추진력 우수\n문제 해결 속도 빠름\n실행력이 강함\n긴급 상황 대응 우수\n리더십 강점",
        "주의점": "성급한 판단 가능\n세부 검토 부족 가능\n직설적 표현 가능\n과정 관리 부족 가능\n타인 의견 누락 가능",
        "추천역할": "개선활동 추진\n긴급 대응\n프로젝트 리딩\n일정 관리\n현장 개선 추진",
        "협업팁": "핵심만 빠르게 전달\n우선순위와 목표 명확화\n결론 및 Action 중심으로 소통\n유연한 실행 환경 제공\n즉각적인 피드백과 성과 인정",
        "스트레스": "의사결정이 지나치게 느릴 때\n회의만 길고 실행이 없을 때\n절차와 규칙 때문에 실행이 지연될 때"
    },
    "조율형": {
        "특징": "인간관계 중시\n원활한 소통 선호\n공감 및 배려 성향\n협업 및 팀워크 강조\n유연한 태도 소유",
        "강점": "커뮤니케이션 우수\n팀 분위기 활성화\n갈등 조율 능력\n고객 및 타부서 소통 강점\n친화력 및 협조성 우수",
        "주의점": "거절을 어려워함\n관계 중심 판단 가능\n갈등 회피 성향 가능\n주관적 의견 치우침 가능\n업무 집중도 분산 가능",
        "추천역할": "고객 대응\n협업 조정\n커뮤니케이션 담당\n팀워크 강화 활동\nVOC 대응",
        "협업팁": "공감형 커뮤니케이션\n존중과 배려 표현\n대화 중심 설명\n의견 경청 및 수렴\n개인적 친밀감 형성",
        "스트레스": "팀원 간 갈등이나 비난이 발생할 때\n독단적이고 일방적인 지시를 받을 때\n소통 없이 단독 업무를 강요받을 때"
    },
    "관리형": {
        "특징": "체계와 절차 중시\n계획적 업무 수행\n규칙 및 기준 준수\n안정성 및 신뢰성 선호\n논리적이고 체계적",
        "강점": "품질 기준 관리 우수\n체계적 프로세스 운영\n일정 및 마감 준수\n위험 예방 및 안정성\n문서화 및 표준화 강점",
        "주의점": "변화 대응 느릴 수 있음\n융통성 부족 가능\n지나친 보수성 가능\n의사결정 속도 저하 가능\n새로운 시도 부담 가능",
        "추천역할": "품질 시스템 관리\nISO 관리\nAudit 대응\n표준서 관리\n품질 문서 체계 운영",
        "협업팁": "충분한 설명 제공\n기준과 절차 명확화\n변경점 사전 공유\n단계별 설명 제공\n충분한 근거 제공",
        "스트레스": "기준 없는 업무 변경\n데이터 및 문서 누락\n충분한 검토 없이 진행 강요받을 때"
    },
    "혼합형": {
        "특징": "두 가지 성향의 균형적 결합\n상황에 따른 유연한 대처\n종합적인 업무 접근 능력",
        "강점": "다양한 관점 수용 가능\n분석과 실행 혹은 조율의 상호보완\n다양한 부서와의 협업 능력 우수",
        "주의점": "상황에 따라 의사결정 혼선 가능\n스스로 내적 갈등이나 피로 가중 가능",
        "추천역할": "개선 프로젝트 리더 / TF 운영\n부서 간 협업 프로젝트 담당\n종합 품질 기획 업무",
        "협업팁": "상황별 핵심 역할 명확화\n동일 점수 유형의 특성을 상호 보완적으로 활용하도록 유도",
        "스트레스": "상반된 업무 방식을 동시에 완벽하게 요구받을 때"
    }
}

# [30개 전체 문항 데이터]
SURVEY_QUESTIONS = [
    {"no": 1, "문항": "문제가 발생했을 때 가장 먼저 하는 행동은?", "A": "데이터를 확인한다", "B": "우선 빠르게 조치한다", "C": "관련자들과 소통한다", "D": "절차와 이력을 확인한다"},
    {"no": 2, "문항": "업무를 받을 때 선호하는 방식은?", "A": "근거와 배경 포함 설명", "B": "핵심만 빠르게 전달", "C": "대화 중심 설명", "D": "문서 및 절차 기준 설명"},
    {"no": 3, "문항": "회의에서 나는 주로?", "A": "논리와 데이터를 제시한다", "B": "결론을 빠르게 정리한다", "C": "분위기를 조율한다", "D": "회의 내용을 기록한다"},
    {"no": 4, "문항": "업무 스트레스를 가장 많이 받는 상황은?", "A": "데이터 부족", "B": "결정 지연", "C": "갈등 상황", "D": "기준 없는 변경"},
    {"no": 5, "문항": "고객 클레임 발생 시 나는?", "A": "원인 데이터를 분석한다", "B": "즉시 대응책을 추진한다", "C": "고객과 소통을 우선한다", "D": "이력과 절차를 정리한다"},
    {"no": 6, "문항": "업무 진행 시 가장 중요하게 생각하는 것은?", "A": "정확성", "B": "속도", "C": "협업", "D": "체계성"},
    {"no": 7, "문항": "보고를 할 때 나는?", "A": "근거 자료를 충분히 준비한다", "B": "핵심 결과 중심으로 설명한다", "C": "상대 반응을 보며 설명한다", "D": "문서 형식을 맞춰 정리한다"},
    {"no": 8, "문항": "팀 프로젝트에서 가장 잘 맞는 역할은?", "A": "분석 담당", "B": "실행 담당", "C": "소통 담당", "D": "일정/문서 관리 담당"},
    {"no": 9, "문항": "변경 사항이 발생하면 나는?", "A": "영향성을 검토한다", "B": "우선 실행 가능 여부를 본다", "C": "관련 부서와 공유한다", "D": "변경 이력을 관리한다"},
    {"no": 10, "문항": "협업 시 중요하게 생각하는 것은?", "A": "정확한 정보 공유", "B": "빠른 진행", "C": "원활한 관계", "D": "역할과 기준 명확화"},
    {"no": 11, "문항": "내가 가장 자신 있는 업무는?", "A": "데이터 분석", "B": "문제 해결 추진", "C": "커뮤니케이션", "D": "문서 관리"},
    {"no": 12, "문항": "업무 우선순위를 정할 때 나는?", "A": "리스크를 분석한다", "B": "긴급도를 우선한다", "C": "팀 상황을 고려한다", "D": "계획과 절차를 따른다"},
    {"no": 13, "문항": "갑작스러운 일정 변경이 생기면?", "A": "영향 분석부터 한다", "B": "바로 대응한다", "C": "주변과 조율한다", "D": "계획을 재정리한다"},
    {"no": 14, "문항": "문제가 반복 발생하면 나는?", "A": "데이터 추세를 분석한다", "B": "개선 활동을 추진한다", "C": "관련자 의견을 수집한다", "D": "표준화를 검토한다"},
    {"no": 15, "문항": "가장 성취감을 느끼는 순간은?", "A": "문제 원인을 밝혔을 때", "B": "결과를 만들었을 때", "C": "팀워크가 좋아졌을 때", "D": "체계가 안정화됐을 때"},
    {"no": 16, "문항": "업무 시작할 때 나는?", "A": "충분히 검토 후 시작한다", "B": "일단 실행하면서 조정한다", "C": "주변과 협의 후 시작한다", "D": "계획을 세우고 시작한다"},
    {"no": 17, "문항": "회의 분위기가 길어지면 나는?", "A": "논점을 정리한다", "B": "결론을 촉구한다", "C": "분위기를 부드럽게 만든다", "D": "회의 내용을 정리한다"},
    {"no": 18, "문항": "업무 실수가 발생하면 나는?", "A": "원인을 먼저 분석한다", "B": "우선 해결부터 한다", "C": "관계 영향을 신경쓴다", "D": "프로세스를 수정한다"},
    {"no": 19, "문항": "협업 시 가장 답답한 상황은?", "A": "논리적이지 못할 때", "B": "행동이 느릴 때", "C": "독단적으로 행동할 때", "D": "규칙을 안 지킬 때"},
    {"no": 20, "문항": "새로운 업무가 주어지면 나는?", "A": "관련 정보를 수집한다", "B": "일단 시도해 본다", "C": "도움을 줄 사람을 찾는다", "D": "매뉴얼이 있는지 확인한다"},
    {"no": 21, "문항": "피드백을 줄 때 내가 중시하는 것은?", "A": "객관적 사실과 데이터", "B": "개선 방향과 행동 요령", "C": "상대방의 감정과 동기부여", "D": "기준 준수 여부 및 보완점"},
    {"no": 22, "문항": "동료가 평가하는 나의 장점은?", "A": "신중하고 꼼꼼하다", "B": "과감하고 신속하다", "C": "친근하고 협조적이다", "D": "정확하고 체계적이다"},
    {"no": 23, "문항": "업무 마감 기한이 다가오면 나는?", "A": "내용의 완성도를 검토한다", "B": "밤을 새워서라도 끝낸다", "C": "팀원들과 분담하여 해결한다", "D": "일정에 맞춰 단계를 통제한다"},
    {"no": 24, "문항": "의견 충돌이 생겼을 때 나의 대처는?", "A": "논리적 근거로 설득한다", "B": "빠르게 타협점을 찾는다", "C": "상대 의견 경청 후 조율한다", "D": "기존 원칙과 가이드를 따른다"},
    {"no": 25, "문항": "업무 계획을 세울 때 나의 스타일은?", "A": "예상 리스크까지 상세히 기록", "B": "굵직한 목표 중심으로 유연하게", "C": "역할 분담과 소통 계획 위주", "D": "일정별 단계와 산출물 중심"},
    {"no": 26, "문항": "동료의 일하는 방식 중 선호하는 타입은?", "A": "논리적이고 똑똑한 사람", "B": "행동이 빠르고 화끈한 사람", "C": "배려심 있고 소통이 잘되는 사람", "D": "약속을 잘 지키고 철저한 사람"},
    {"no": 27, "문항": "내가 생각하는 이상적인 팀의 모습은?", "A": "전문성이 높은 조직", "B": "성과와 실행력이 높은 조직", "C": "인간미 있고 단합이 잘되는 조직", "D": "질서와 체계가 잡힌 조직"},
    {"no": 28, "문항": "업무 인수인계를 할 때 나는?", "A": "배경과 기술적 노하우까지 설명", "B": "중요 포인트와 긴급 건 위주 설명", "C": "상황별 대면 가이드 및 팁 공유", "D": "매뉴얼과 파일 링크 위주로 정리"},
    {"no": 29, "문항": "회의 준비를 할 때 나는?", "A": "사전 자료를 정밀하게 분석", "B": "회의용 핵심 어젠다만 준비", "C": "참석자 조율 및 사전 의견 수집", "D": "회의 순서 및 양식 사전 세팅"},
    {"no": 30, "문항": "조직에서 나의 핵심 가치는 무엇인가?", "A": "문제의 본질과 원인 규명", "B": "돌파구를 찾고 성과 창출", "C": "조직 내 신뢰와 협업 시너지", "D": "안정적인 시스템 구축 및 유지"}
]

TYPE_MAP = {"A": "분석형", "B": "실행형", "C": "조율형", "D": "관리형"}

# 데이터 컬럼 정의 (상세 프로파일링 항목 추가)
COLUMNS_LIST = [
    "일시", "이름", "팀명", "파트명", "최종유형", 
    "핵심 특징", "강점", "주의점", "추천 역할", "협업 팁", "스트레스 요인",
    "분석형_개수", "실행형_개수", "조율형_개수", "관리형_개수"
]

def load_results():
    default_df = pd.DataFrame(columns=COLUMNS_LIST)
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        try:
            df = pd.read_csv(DATA_FILE)
            # 이전 버전 데이터 구조 대응용 보정
            for col in COLUMNS_LIST:
                if col not in df.columns:
                    df[col] = ""
            return df[COLUMNS_LIST]
        except Exception:
            return default_df
    return default_df

def save_all_results(df):
    df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")

# 메뉴 구성
st.sidebar.title("📋 프로파일링 메뉴")
menu = st.sidebar.radio("화면 이동", ["📝 스타일 진단하기", "📊 관리자 대시보드"])

# --- 화면 1: 스타일 진단하기 ---
if menu == "📝 스타일 진단하기":
    st.title("📝 업무 스타일 프로파일링 (Work Style Profiling)")
    st.write("품질혁신팀 워크샵을 위한 진단 페이지입니다. 문항을 읽고 본인의 평소 스타일을 골라주세요.")
    
    st.subheader("👤 참여자 정보 입력")
    col1, col2, col3 = st.columns(3)
    with col1:
        user_name = st.text_input("이름", placeholder="예: 홍길동")
    with col2:
        st.text_input("소속 팀명", value="품질혁신팀", disabled=True)
    with col3:
        part_name = st.selectbox("소속 파트명", ["품질관리파트", "품질기획파트"])
        
    st.divider()
    st.subheader("✍️ 진단 문항 (총 30문항)")
    
    user_responses = {}
    for item in SURVEY_QUESTIONS:
        idx = item["no"]
        st.markdown(f"**Q{idx}. {item['문항']}**")
        choice = st.radio(
            f"선택 (Q{idx})",
            options=["A", "B", "C", "D"],
            format_func=lambda x: f"({x}) {item[x]}",
            key=f"q_{idx}",
            label_visibility="collapsed"
        )
        user_responses[idx] = choice
        st.write("")
        
    st.divider()
    
    if st.button("진단 결과 제출하기", type="primary", use_container_width=True):
        if not user_name.strip():
            st.error("⚠️ 성함을 정확히 입력해 주세요.")
        else:
            counts = {"분석형": 0, "실행형": 0, "조율형": 0, "관리형": 0}
            for idx, choice in user_responses.items():
                type_name = TYPE_MAP[choice]
                counts[type_name] += 1
                
            max_val = max(counts.values())
            highest_types = [k for k, v in counts.items() if v == max_val]
            
            if len(highest_types) >= 3:
                final_type = "재설문 필요"
                lookup_type = "분석형" # 기본 매칭 방지용 임시 기본값
            elif len(highest_types) == 2:
                final_type = f"{highest_types[0]}+{highest_types[1]}"
                lookup_type = "혼합형"
            else:
                final_type = highest_types[0]
                lookup_type = highest_types[0]
                
            # 데이터 매칭 자동화
            details = TYPE_DETAILS.get(lookup_type, TYPE_DETAILS["혼합형"])
            current_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            
            result_row = {
                "일시": current_time,
                "이름": user_name.replace(",", " "),
                "팀명": "품질혁신팀",
                "파트명": part_name,
                "최종유형": final_type,
                "핵심 특징": details["특징"],
                "강점": details["강점"],
                "주의점": details["주의점"],
                "추천 역할": details["추천역할"],
                "협업 팁": details["협업팁"],
                "스트레스 요인": details["스트레스"],
                "분석형_개수": counts["분석형"],
                "실행형_개수": counts["실행형"],
                "조율형_개수": counts["조율형"],
                "관리형_개수": counts["관리형"]
            }
            
            df = load_results()
            df = pd.concat([df, pd.DataFrame([result_row])], ignore_index=True)
            save_all_results(df)
            
            st.balloons()
            st.success(f"🎉 {user_name}님의 진단 데이터가 안전하게 제출되었습니다.")
            st.markdown(f"### 🎯 {user_name}님의 대표 업무 스타일: **[{final_type}]**")
            
            my_score_df = pd.DataFrame(list(counts.items()), columns=["유형", "선택 수"])
            st.bar_chart(data=my_score_df, x="유형", y="선택 수")

# --- 화면 2: 관리자 대시보드 ---
elif menu == "📊 관리자 대시보드":
    st.title("📊 품질혁신팀 대시보드 분석 센터")
    input_pw = st.text_input("🔑 관리자 보안 인증 비밀번호를 입력해 주세요.", type="password")
    
    if input_pw == ADMIN_PASSWORD:
        st.success("🔓 인증되었습니다. 데이터 관리 및 제어 권한이 부여되었습니다.")
        st.divider()
        
        # 세션 상태를 이용한 안전한 삭제 상태 추적
        df_res = load_results()
        
        if df_res.empty:
            st.warning("📥 현재 수집된 데이터가 없습니다. 설문 응답이 쌓인 후 확인 가능합니다.")
        else:
            # 🚨 [요청사항 추가] 관리자 데이터 삭제 및 수정 편집기 영역
            st.subheader("🛠️ 데이터 정제 및 테스트 이력 관리 컨트롤러")
            st.info("💡 테스트 제출 건이나 잘못 기입된 데이터 행 번호를 선택하고 아래 버튼을 누르면 실시간 청소가 완료됩니다.")
            
            # 각 행의 식별 정보 제공
            df_res['관리자선택용_ID'] = df_res.index.map(lambda x: f"[{x}번 행] {df_res.loc[x, '이름']} ({df_res.loc[x, '파트명']} / {df_res.loc[x, '최종유형']})")
            
            delete_target = st.selectbox("❌ 삭제할 대상을 선택해 주세요.", df_res['관리자선택용_ID'].tolist())
            
            if st.button("선택한 행 즉시 영구 삭제", type="secondary"):
                target_idx = df_res[df_res['관리자선택용_ID'] == delete_target].index[0]
                df_res = df_res.drop(target_idx).reset_index(drop=True)
                # 불필요 가상열 제거 후 저장
                if '관리자선택용_ID' in df_res.columns:
                    df_res = df_res.drop(columns=['관리자선택용_ID'])
                save_all_results(df_res)
                st.toast("🔥 선택하신 데이터가 파일에서 완벽히 삭제되었습니다!")
                st.rerun() # 화면 동기화 새로고침
                
            if '관리자선택용_ID' in df_res.columns:
                df_res = df_res.drop(columns=['관리자선택용_ID'])
                
            st.divider()

            # 통계 리포트 영역
            total_p = len(df_res)
            st.metric("품질혁신팀 총 참여 인원", f"{total_p} 명")
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("👥 1. 최종 유형별 분포 (전체)")
                type_counts = df_res["최종유형"].value_counts().reset_index()
                type_counts.columns = ["최종유형", "인원수"]
                st.bar_chart(data=type_counts, x="최종유형", y="인원수", use_container_width=True)
                
            with col2:
                st.subheader("📈 2. 팀 전체 성향 누적 합계")
                total_a = pd.to_numeric(df_res["분석형_개수"]).sum()
                total_b = pd.to_numeric(df_res["실행형_개수"]).sum()
                total_c = pd.to_numeric(df_res["조율형_개수"]).sum()
                total_d = pd.to_numeric(df_res["관리형_개수"]).sum()
                
                team_total_df = pd.DataFrame({
                    "업무 유형": ["분석형", "실행형", "조율형", "관리형"],
                    "누적 선택 수": [total_a, total_b, total_c, total_d]
                })
                st.bar_chart(data=team_total_df, x="업무 유형", y="누적 선택 수", use_container_width=True)
                
            st.divider()
            
            # 파트별 비교
            st.subheader("📊 2-2. 파트별 업무 스타일 심층 비교")
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                st.markdown("#### 🔬 품질관리파트 최종 유형 비율")
                qc_df = df_res[df_res["파트명"] == "품질관리파트"]
                if not qc_df.empty:
                    qc_counts = qc_df["최종유형"].value_counts().reset_index()
                    qc_counts.columns = ["최종유형", "인원수"]
                    st.bar_chart(data=qc_counts, x="최종유형", y="인원수", use_container_width=True)
                else: st.caption("품질관리파트의 제출 데이터가 없습니다.")
            with p_col2:
                st.markdown("#### 📝 품질기획파트 최종 유형 비율")
                qp_df = df_res[df_res["파트명"] == "품질기획파트"]
                if not qp_df.empty:
                    qp_counts = qp_df["최종유형"].value_counts().reset_index()
                    qp_counts.columns = ["최종유형", "인원수"]
                    st.bar_chart(data=qp_counts, x="최종유형", y="인원수", use_container_width=True)
                else: st.caption("품질기획파트의 제출 데이터가 없습니다.")
            
            st.divider()
            
            # 종합 리포트 자동 생성
            st.subheader("💡 3. 우리 팀 업무 성향 및 협업 리스크 리포트")
            stats = {"분석형": total_a, "실행형": total_b, "조율형": total_c, "관리형": total_d}
            sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
            strongest = sorted_stats[0][0]
            weakest = sorted_stats[-1][0]
            
            cb1, cb2 = st.columns(2)
            with cb1:
                st.success(f"🔥 **팀 내 가장 우세한 성향: [{strongest}]**")
                if strongest == "분석형": st.write("데이터 중심 사고와 철저한 원인 분석 능력이 뛰어난 팀입니다.")
                elif strongest == "실행형": st.write("빠른 실행과 추진력이 강점이며 현장 대응 속도가 탁월합니다.")
                elif strongest == "조율형": st.write("커뮤니케이션 능력이 우수하며 관계 조율에 강점이 있습니다.")
                elif strongest == "관리형": st.write("체계적인 표준화, 규칙 준수 및 문서 시스템 관리가 정확합니다.")
            with cb2:
                st.error(f"🚨 **우리 팀의 잠재적 리스크: [{weakest}] 성향 보완 필요**")
                if weakest == "분석형": st.write("철저한 데이터 검토가 누락되어 유효성 리스크가 발생할 수 있습니다.")
                elif weakest == "실행형": st.write("의사결정이 지나치게 지연되거나 회의만 길어질 위험이 있습니다.")
                elif weakest == "조율형": st.write("부서 간 장벽이 발생하거나 단독 플레이 성향이 짙어질 수 있습니다.")
                elif weakest == "관리형": st.write("업무 표준 가이드라인이 부재하여 상황별 혼선이 가중될 수 있습니다.")
                
            st.divider()
            
            # 🌟 [보완 요청사항] 보완된 전체 데이터 테이블 출력 및 다운로드
            st.subheader("📋 4. 팀원별 프로파일링 통합 상세 Raw Data")
            st.write("첨부 파일 가이드라인의 모든 정성적 해석 지표(특징, 강점, 주의점, 추천 역할 등)가 통합 반영된 실시간 전사 데이터베이스입니다.")
            st.dataframe(df_res, use_container_width=True)
            
            csv_data = df_res.to_csv(index=False, encoding="utf-8-sig")
            st.download_button(
                label="📥 전체 프로파일링 결과 마스터 엑셀(CSV) 다운로드", 
                data=csv_data, 
                file_name="quality_innovation_team_workstyle_matrix.csv", 
                mime="text/csv"
            )
            
    elif input_pw != "":
        st.error("❌ 비밀번호가 올바르지 않습니다. 다시 입력해 주세요.")
