import streamlit as st
import pandas as pd
import io
import os

# 1. 페이지 설정 (최상단 고정)
st.set_page_config(page_title="품질혁신팀 업무 스타일 프로파일링 시스템", layout="wide")

# ==========================================
# 🔑 [관리자 설정]
# ==========================================
ADMIN_PASSWORD = "123!"

# 💾 엑셀 백업 파일명 지정
BACKUP_FILE_NAME = "quality_innovation_team_workstyle_matrix.xlsx"

# ==========================================
# 📦 [데이터베이스] 유형별 상세 매칭 데이터 (첨부파일 기반 완벽 반영)
# ==========================================
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

# 📋 [질문지 데이터베이스] 기존 30문항 완벽 유지
QUESTIONS = [
    {"no": 1, "q": "문제가 발생했을 때 가장 먼저 하는 행동은?", "A": "데이터를 확인한다", "B": "우선 빠르게 조치한다", "C": "관련자들과 소통한다", "D": "절차와 이력을 확인한다"},
    {"no": 2, "q": "업무를 받을 때 선호하는 방식은?", "A": "근거와 배경 포함 설명", "B": "핵심만 빠르게 전달", "C": "대화 중심 설명", "D": "문서 및 절차 기준 설명"},
    {"no": 3, "q": "회의에서 나는 주로?", "A": "논리와 데이터를 제시한다", "B": "결론을 빠르게 정리한다", "C": "분위기를 조율한다", "D": "회의 내용을 기록한다"},
    {"no": 4, "q": "업무 스트레스를 가장 많이 받는 상황은?", "A": "데이터 부족", "B": "결정 지연", "C": "갈등 상황", "D": "기준 없는 변경"},
    {"no": 5, "q": "고객 클레임 발생 시 나는?", "A": "원인 데이터를 분석한다", "B": "즉시 대응책을 추진한다", "C": "고객과 소통을 우선한다", "D": "이력과 절차를 정리한다"},
    {"no": 6, "q": "업무 진행 시 가장 중요하게 생각하는 것은?", "A": "정확성", "B": "속도", "C": "협업", "D": "체계성"},
    {"no": 7, "q": "보고를 할 때 나는?", "A": "근거 자료를 충분히 준비한다", "B": "핵심 결과 중심으로 설명한다", "C": "상대 반응을 보며 설명한다", "D": "문서 형식을 맞춰 정리한다"},
    {"no": 8, "q": "팀 프로젝트에서 가장 잘 맞는 역할은?", "A": "분석 담당", "B": "실행 담당", "C": "소통 담당", "D": "일정/문서 관리 담당"},
    {"no": 9, "q": "변경 사항이 발생하면 나는?", "A": "영향성을 검토한다", "B": "우선 실행 가능 여부를 본다", "C": "관련 부서와 공유한다", "D": "변경 이력을 관리한다"},
    {"no": 10, "q": "협업 시 중요하게 생각하는 것은?", "A": "정확한 정보 공유", "B": "빠른 진행", "C": "원활한 관계", "D": "역할과 기준 명확화"},
    {"no": 11, "q": "내가 가장 자신 있는 업무는?", "A": "데이터 분석", "B": "문제 해결 추진", "C": "커뮤니케이션", "D": "문서 관리"},
    {"no": 12, "q": "업무 우선순위를 정할 때 나는?", "A": "리스크를 분석한다", "B": "긴급도를 우선한다", "C": "팀 상황을 고려한다", "D": "계획과 절차를 따른다"},
    {"no": 13, "q": "갑작스러운 일정 변경이 생기면?", "A": "영향 분석부터 한다", "B": "바로 대응한다", "C": "주변과 조율한다", "D": "계획을 재정리한다"},
    {"no": 14, "q": "문제가 반복 발생하면 나는?", "A": "데이터 추세를 분석한다", "B": "개선 활동을 추진한다", "C": "관련자 의견을 수집한다", "D": "표준화를 검토한다"},
    {"no": 15, "q": "가장 성취감을 느끼는 순간은?", "A": "문제 원인을 밝혔을 때", "B": "결과를 만들었을 때", "C": "팀워크가 좋아졌을 때", "D": "체계가 안정화됐을 때"},
    {"no": 16, "q": "업무를 시작할 때 나는?", "A": "충분히 검토 후 시작한다", "B": "일단 실행하면서 조정한다", "C": "주변과 협의 후 시작한다", "D": "계획을 세우고 시작한다"},
    {"no": 17, "q": "회의 분위기가 길어지면 나는?", "A": "논점을 정리한다", "B": "결론을 촉구한다", "C": "분위기를 부드럽게 만든다", "D": "회의 내용을 정리한다"},
    {"no": 18, "q": "업무 실수가 발생하면 나는?", "A": "원인을 먼저 분석한다", "B": "우선 해결부터 한다", "C": "관계 영향을 신경쓴다", "D": "프로세스를 수정한다"},
    {"no": 19, "q": "협업 시 가장 답답한 상황은?", "A": "근거 없는 주장", "B": "지나치게 느린 실행", "C": "독단적인 업무 처리", "D": "무계획적인 진행"},
    {"no": 20, "q": "새로운 업무 프로세스를 도입할 때 나는?", "A": "효과성을 철저히 검증한다", "B": "우선 적용 후 보완한다", "C": "팀원들의 공감을 얻는다", "D": "매뉴얼과 가이드를 만든다"},
    {"no": 21, "q": "동료가 나에게 요청할 때 가장 선호하는 방식은?", "A": "명확한 데이터 제시", "B": "결론만 빠르게 요청", "C": "상황에 대한 감정적 공감", "D": "공식적인 절차 준수"},
    {"no": 22, "q": "피드백을 줄 때 나는 주로?", "A": "객관적인 사실과 수치 제시", "B": "개선 방향 위주로 단도직입적 전달", "C": "상대방 격려 및 소통 중심", "D": "정해진 기준과 프로세스 기반 조언"},
    {"no": 23, "q": "업무 계획을 수립할 때 중요하게 생각하는 것은?", "A": "발생 가능한 리스크 분석", "B": "즉시 실행 가능한 Action Plan", "C": "협업 부서와의 역할 조율", "D": "타임라인과 표준 절차 준수"},
    {"no": 24, "q": "부서 간 갈등이 발생했을 때 해결 방식은?", "A": "갈등 원인 데이터를 객관적으로 규명", "B": "빠르게 미팅을 소집하여 결론 도출", "C": "각 부서의 입장 청취 및 관계 조율", "D": "기존 R&R 및 가이드라인 기준으로 판정"},
    {"no": 25, "q": "품질 Audit을 준비할 때 나의 강점은?", "A": "지적 예상 문제점 사전 분석", "B": "현장 지적사항 즉각 개선 조치", "C": "심사원과의 유연한 소통 및 대응", "D": "정형화된 문서 체계 및 표준서 정비"},
    {"no": 26, "q": "선호하는 회의 스타일은?", "A": "준비된 자료를 기반으로 한 분석 회의", "B": "빠르게 의사결정만 내리는 짧은 회의", "C": "자유롭게 의견을 개진하는 아이디어 회의", "D": "정해진 아젠다와 절차대로 진행되는 정기 회의"},
    {"no": 27, "q": "업무 지시를 내리거나 받을 때 핵심은?", "A": "왜(Why) 해야 하는지에 대한 명확한 근거", "B": "언제까지(When) 무엇을(What) 해야 하는지 결과", "C": "누구와(Who) 협업하여 시너지를 낼 것인지", "D": "어떻게(How) 정해진 절차대로 수행할 것인지"},
    {"no": 28, "q": "어려운 과제에 직면했을 때 나의 태도는?", "A": "과거 사례와 데이터를 철저히 스터디한다", "B": "다양한 시도를 빠르게 실행해 본다", "C": "주변 전문가나 동료들에게 조언을 구한다", "D": "기존 매뉴얼의 근본 원칙을 다시 검토한다"},
    {"no": 29, "q": "내가 팀에 기여하는 가장 큰 가치는?", "A": "논리적 리스크 예방 및 품질 안정화", "B": "강한 추진력을 통한 목표 조기 달성", "C": "원활한 소통을 통한 팀 시너지 창출", "D": "체계적인 표준 구축을 통한 프로세스 정립"},
    {"no": 30, "q": "동료들이 평가하는 나의 일하는 모습은?", "A": "스마트하고 꼼꼼하며 실수가 없는 사람", "B": "행동이 빠르고 시원시원하며 추진력 있는 사람", "C": "친절하고 소통이 잘 되며 협업하기 좋은 사람", "D": "체계적이고 계획적이며 신뢰할 수 있는 사람"}
]

# ==========================================
# 💾 [모드 체크 및 데이터 동기화 로직]
# ==========================================
# GitHub에 엑셀 파일이 업로드되어 있는지 확인
IS_PERMANENT_MODE = os.path.exists(BACKUP_FILE_NAME)

if "survey_db" not in st.session_state:
    if IS_PERMANENT_MODE:
        # 🔗 [영구 보존 모드] GitHub에 올린 엑셀에서 데이터를 영구 고정 로드
        st.session_state.survey_db = pd.read_excel(BACKUP_FILE_NAME).to_dict(orient="records")
    else:
        # 🧪 [실시간 설문 모드] 서버 메모리에 임시 축적
        st.session_state.survey_db = []

# ==========================================
# 🖥️ [화면 레이아웃 구성]
# ==========================================
tabs = st.tabs(["📋 팀원 설문 응답창", "📊 품질혁신팀 통합 대시보드"])

# ------------------------------------------
# 탭 1: 팀원 설문 응답창
# ------------------------------------------
with tabs[0]:
    if IS_PERMANENT_MODE:
        st.info("🔒 워크샵 데이터 백업 파일이 반영되어 '영구 보존 모드'로 작동 중입니다. 설문 제출이 마감되었습니다.")
    else:
        st.title("📋 품질혁신팀 업무 스타일 프로파일링 진단")
        st.write("본 진단은 인사 평가가 아닌 워크샵 협업 증진 목적으로 사용됩니다. 편안하게 답변해 주세요.")
        st.divider()
        
        # 주관식 인적사항 입력 (기존 로직 유지)
        st.subheader("👤 기본 인적사항 입력")
        c1, c2 = st.columns(2)
        with c1:
            u_name = st.text_input("이름을 입력해 주세요", key="survey_name").strip()
        with c2:
            u_part = st.selectbox("소속 파트를 선택해 주세요", ["품질관리파트", "품질기획파트"], key="survey_part")
            
        st.divider()
        st.subheader("✍️ 30문항 진단 스타트")
        
        # 30문항 라디오 버튼 동적 생성
        user_answers = {}
        for item in QUESTIONS:
            st.markdown(f"**🔹 문항 {item['no']}. {item['q']}**")
            ans = st.radio(
                f"선택지_{item['no']}",
                options=["A", "B", "C", "D"],
                format_func=lambda x: f"({x}) {item[x]}",
                label_visibility="collapsed",
                key=f"q_{item['no']}"
            )
            user_answers[item['no']] = ans
            st.write("") # 간격 조정
            
        # 설문 제출 버튼 클릭 시 로직
        if st.button("🚀 프로파일링 결과 제출하기", use_container_width=True):
            if not u_name:
                st.error("❌ 이름을 입력하셔야 제출이 가능합니다.")
            else:
                # 점수 집계 계산
                counts = {"분석형": 0, "실행형": 0, "조율형": 0, "관리형": 0}
                for no, ans in user_answers.items():
                    if ans == "A": counts["분석형"] += 1
                    elif ans == "B": counts["실행형"] += 1
                    elif ans == "C": counts["조율형"] += 1
                    elif ans == "D": counts["관리형"] += 1
                    
                # 유형 판정 알고리즘
                max_val = max(counts.values())
                highest_types = [k for k, v in counts.items() if v == max_val]
                
                if len(highest_types) >= 3:
                    final_type = "재설문 필요"
                elif len(highest_types) == 2:
                    final_type = f"{highest_types[0]}+{highest_types[1]}"
                else:
                    final_type = highest_types[0]
                    
                lookup_type = "혼합형" if len(highest_types) == 2 else highest_types[0]
                details = TYPE_DETAILS.get(lookup_type, TYPE_DETAILS["혼합형"])
                
                # 결과 데이터 적재
                new_row = {
                    "이름": u_name, "팀명": "품질혁신팀", "파트명": u_part, "최종유형": final_type,
                    "핵심 특징": details["특징"], "강점": details["강점"], "주의점": details["주의점"],
                    "추천 역할": details["추천역할"], "협업 팁": details["협업팁"], "스트레스 요인": details["스트레스"],
                    "분석형_개수": counts["분석형"], "실행형_개수": counts["실행형"], "조율형_개수": counts["조율형"], "관리형_개수": counts["관리형"]
                }
                
                # 중복 이름 제거 후 삽입
                st.session_state.survey_db = [r for r in st.session_state.survey_db if r["이름"] != u_name]
                st.session_state.survey_db.append(new_row)
                
                st.balloons()
                st.success(f"🎉 {u_name}님의 설문이 정상 제출되었습니다! 상단 '통합 대시보드' 탭에서 결과를 확인하세요.")

# ------------------------------------------
# 탭 2: 품질혁신팀 통합 대시보드
# ------------------------------------------
with tabs[1]:
    st.title("📊 품질혁신팀 대시보드 분석 센터")
    
    # 보안 패스워드 입력
    input_pw = st.text_input("🔑 관리자 보안 인증 비밀번호", type="password")
    
    if input_pw == ADMIN_PASSWORD:
        if IS_PERMANENT_MODE:
            st.success("🔓 영구 고정 데이터 백업 파일이 활성화되었습니다. (서버 리부트 시에도 휘발되지 않음)")
        else:
            st.warning("⚠️ 현재 '실시간 설문 수집 모드'입니다. 워크샵 완료 직후 최하단에서 반드시 엑셀을 백업받아 GitHub에 올리셔야 데이터가 고정됩니다.")
            
        st.divider()
        
        # 데이터프레임 변환
        df_res = pd.DataFrame(st.session_state.survey_db)
        
        if df_res.empty:
            st.info("📥 아직 제출된 설문 결과 데이터가 없습니다. 팀원들이 설문을 마치면 통계가 실시간으로 가동됩니다.")
        else:
            # 1. 상단 총 참여 인원 스코어카드
            total_p = len(df_res)
            st.metric("품질혁신팀 총 참여 인원", f"{total_p} 명")
            st.divider()
            
            # 2. 메인 시각화 차트 영역
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
            
            # 3. 파트별 데이터 비교 심층 시각화 
            st.subheader("📊 2-2. 파트별 업무 스타일 심층 비교")
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                st.markdown("#### 🔬 품질관리파트 분포")
                qc_df = df_res[df_res["파트명"] == "품질관리파트"]
                if not qc_df.empty:
                    qc_counts = qc_df["최종유형"].value_counts().reset_index()
                    qc_counts.columns = ["최종유형", "인원수"]
                    st.bar_chart(data=qc_counts, x="최종유형", y="인원수", use_container_width=True)
                else:
                    st.caption("아직 품질관리파트의 데이터가 없습니다.")
            with p_col2:
                st.markdown("#### 📝 품질기획파트 분포")
                qp_df = df_res[df_res["파트명"] == "품질기획파트"]
                if not qp_df.empty:
                    qp_counts = qp_df["최종유형"].value_counts().reset_index()
                    qp_counts.columns = ["최종유형", "인원수"]
                    st.bar_chart(data=qp_counts, x="최종유형", y="인원수", use_container_width=True)
                else:
                    st.caption("아직 품질기획파트의 데이터가 없습니다.")
            
            st.divider()
            
            # 4. 종합 컨설팅 진단 문장 리포트 추출
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
            
            # 5. 마스터 데이터 프레임 표출
            st.subheader("📋 4. 팀원별 프로파일링 통합 상세 데이터베이스")
            st.dataframe(df_res, use_container_width=True)
            
            # 6. 다운로드 처리 엔진 부착
            def to_excel(df):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='프로파일링_마스터')
                return output.getvalue()
                
            try:
                excel_data = to_excel(df_res)
                st.download_button(
                    label="📥 전체 프로파일링 결과 마스터 엑셀(.xlsx) 다운로드",
                    data=excel_data,
                    file_name=BACKUP_FILE_NAME,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                st.caption("📌 실시간 모드일 때 위 버튼을 눌러 저장한 엑셀을 GitHub에 올리면 해당 데이터로 고정됩니다.")
            except Exception as e:
                st.error(f"엑셀 다운로드 파일 빌드 실패: {e}")
                
    elif input_pw != "":
        st.error("❌ 비밀번호가 올바르지 않습니다.")
