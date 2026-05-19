import streamlit as st
import pandas as pd
import os

# 페이지 설정
st.set_page_config(page_title="품질혁신팀 업무 스타일 프로파일링 시스템", layout="wide")

# ==========================================
# [관리자 설정] 🔑 원하는 비밀번호를 여기에 적어주세요!
# ==========================================
ADMIN_PASSWORD = "정환휘"

# 데이터 저장 파일 경로
DATA_FILE = "survey_results.csv"

# [30개 전체 문항 및 선택지 데이터]
SURVEY_QUESTIONS = [
    {"no": 1, "문항": "문제가 발생했을 때 가장 먼저 하는 행동은?", "A": "데이터를 확인한다", "B": "우선 빠르게 조치한다", "C": "관련자들과 소통한다", "D": "절차와 이력을 확인한다"},
    {"no": 2, "문항": "업무를 받을 때 선호하는 방식은?", "A": "근거와 배경 포함 설명", "B": "핵심만 빠르게 전달", "C": "대화 중심 설명", "D": "문서 및 절차 기준 설명"},
    {"no": 3, "문항": "회의에서 나는 주로?", "A": "논리와 데이터를 제시한다", "B": "결론을 빠르게 정리한다", "C": "분위기를 조율한다", "D": "회의 내용을 기록한다"},
    {"no": 4, "문항": "업무 스트레스를 가장 많이 받는 상황은?", "A": "데이터 부족", "B": "결정 지연", "C": "갈등 상황", "D": "기준 없는 변경"},
    {"no": 5, "문항": "고객 클레임 발생 시 나는?", "A": "원인 데이터를 분석한다", "B": "즉시 대응책을 추진한다", "C": "고객과 소통을 우선한다", "D": "이력과 절차를 정리한다"},
    {"no": 6, "문항": "업무 진행 시 가장 중요하게 생각하는 것은?", "A": "정확성", "B": "속도", "C": "협업", "D": "체계성"},
    {"no": 7, "문항": "보고를 할 때 나는?", "A": "근거 자료를 충분히 준비한다", "B": "핵심 결과 중심으로 설명한다", "C": "상대 반응을 보며 설명한다", "D": "문서 형식을 맞춰 정리한다"},
    {"no": 8, "팀장/팀원": "팀 프로젝트에서 가장 잘 맞는 역할은?", "A": "분석 담당", "B": "실행 담당", "C": "소통 담당", "D": "일정/문서 관리 담당"},
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

# 데이터 로드 함수 (오류 복구 예외처리 유지)
def load_results():
    default_df = pd.DataFrame(columns=["일시", "이름", "팀명", "파트명", "최종유형", "분석형_개수", "실행형_개수", "조율형_개수", "관리형_개수"])
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        try:
            return pd.read_csv(DATA_FILE)
        except Exception:
            return default_df
    return default_df

# 데이터 저장 함수
def save_results(new_row):
    df = load_results()
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
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
        # 팀명 품질혁신팀 고정형 텍스트로 수정
        st.text_input("소속 팀명", value="품질혁신팀", disabled=True)
    with col3:
        # 파트명 선택할 수 있도록 컴포넌트 추가
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
            
            # 결과 산정 가이드 반영 (3개 겹치면 재설문, 2개 겹치면 혼합형)
            if len(highest_types) >= 3:
                final_type = "재설문 필요 (성향 다중 중첩)"
            elif len(highest_types) == 2:
                final_type = f"{highest_types[0]} + {highest_types[1]}"
            else:
                final_type = highest_types[0]
                
            current_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            result_row = {
                "일시": current_time,
                "이름": user_name.replace(",", " "),
                "팀명": "품질혁신팀",
                "파트명": part_name,
                "최종유형": final_type,
                "분석형_개수": counts["분석형"],
                "실행형_개수": counts["실행형"],
                "조율형_개수": counts["조율형"],
                "관리형_개수": counts["관리형"]
            }
            
            save_results(result_row)
            st.balloons()
            
            st.success(f"🎉 {user_name}님의 진단 데이터가 안전하게 제출되었습니다.")
            st.markdown(f"### 🎯 {user_name}님의 대표 업무 스타일: **[{final_type}]**")
            
            my_score_df = pd.DataFrame(list(counts.items()), columns=["유형", "선택 수"])
            st.bar_chart(data=my_score_df, x="유형", y="선택 수")

# --- 화면 2: 관리자 대시보드 ---
elif menu == "📊 관리자 대시보드":
    st.title("📊 품질혁신팀 대시보드 분석 센터")
    
    # 🔒 [요청사항 구현] 비밀번호 잠금장치 컴포넌트 배치
    input_pw = st.text_input("🔑 관리자 보안 인증 비밀번호를 입력해 주세요.", type="password")
    
    if input_pw == ADMIN_PASSWORD:
        st.success("🔓 인증되었습니다. 데이터 관리 권한이 부여되었습니다.")
        st.divider()
        
        df_res = load_results()
        
        if df_res.empty:
            st.warning("📥 현재 수집된 데이터가 없습니다. 설문 응답이 쌓인 후 확인 가능합니다.")
        else:
            # 상단 기본 통계 현황 (기존 유지)
            total_p = len(df_res)
            st.metric("품질혁신팀 총 참여 인원", f"{total_p} 명")
            st.divider()
            
            # [기존 대시보드 1, 2번 레이아웃 유지]
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("👥 1. 최종 유형별 분포 (전체)")
                type_counts = df_res["최종유형"].value_counts().reset_index()
                type_counts.columns = ["최종유형", "인원수"]
                st.bar_chart(data=type_counts, x="최종유형", y="인원수", use_container_width=True)
                
            with col2:
                st.subheader("📈 2. 팀 전체 성향 누적 합계")
                total_a = df_res["분석형_개수"].sum()
                total_b = df_res["실행형_개수"].sum()
                total_c = df_res["조율형_개_수"].sum() if "조율형_개수" in df_res.columns else df_res.iloc[:, 6].sum()
                total_d = df_res["관리형_개수"].sum()
                
                team_total_df = pd.DataFrame({
                    "업무 유형": ["분석형", "실행형", "조율형", "관리형"],
                    "누적 선택 수": [total_a, total_b, total_c, total_d]
                })
                st.bar_chart(data=team_total_df, x="업무 유형", y="누적 선택 수", use_container_width=True)
                
            st.divider()
            
            # 🌟 [요청사항 구현] 파트별 통계 그래프 섹션 신설
            st.subheader("📊 2-2. 파트별 업무 스타일 심층 비교 (추가 대시보드)")
            st.write("품질관리파트와 품질기획파트 간의 성향 차이를 비교 분석합니다.")
            
            p_col1, p_col2 = st.columns(2)
            
            with p_col1:
                st.markdown("#### 🔬 품질관리파트 최종 유형 비율")
                qc_df = df_res[df_res["파트명"] == "품질관리파트"]
                if not qc_df.empty:
                    qc_counts = qc_df["최종유형"].value_counts().reset_index()
                    qc_counts.columns = ["최종유형", "인원수"]
                    st.bar_chart(data=qc_counts, x="최종유형", y="인원수", use_container_width=True)
                else:
                    st.caption("품질관리파트의 제출 데이터가 아직 없습니다.")
                    
            with p_col2:
                st.markdown("#### 📝 품질기획파트 최종 유형 비율")
                qp_df = df_res[df_res["파트명"] == "품질기획파트"]
                if not qp_df.empty:
                    qp_counts = qp_df["최종유형"].value_counts().reset_index()
                    qp_counts.columns = ["최종유형", "인원수"]
                    st.bar_chart(data=qp_counts, x="최종유형", y="인원수", use_container_width=True)
                else:
                    st.caption("품질기획파트의 제출 데이터가 아직 없습니다.")
            
            st.divider()
            
            # [기존 대시보드 3번 요약 리포트 레이아웃 유지]
            st.subheader("💡 3. 우리 팀 업무 성향 및 협업 리스크 리포트")
            stats = {"분석형": total_a, "실행형": total_b, "조율형": total_c, "관리형": total_d}
            sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
            
            strongest = sorted_stats[0][0]
            weakest = sorted_stats[-1][0]
            
            cb1, cb2 = st.columns(2)
            with cb1:
                st.success(f"🔥 **팀 내 가장 우세한 성향: [{strongest}]**")
                if strongest == "분석형": st.write("데이터 중심 사고와 철저한 원인 분석, 리스크 검토 능력이 매우 뛰어난 팀입니다.")
                elif strongest == "실행형": st.write("빠른 실행과 추진력이 강점이며, 긴급 상황 및 현장 대응 속도가 탁월한 팀입니다.")
                elif strongest == "조율형": st.write("커뮤니케이션 능력이 뛰어나며, 고객 대응 및 관계 조율에 큰 강점을 가진 팀입니다.")
                elif strongest == "관리형": st.write("체계적인 운영과 표준화, ISO 관리 및 문서 관리가 정확하고 완벽한 팀입니다.")
                
            with cb2:
                st.error(f"🚨 **우리 팀의 잠재적 협업 리스크: [{weakest}] 성향 보완 필요**")
                if weakest == "분석형": st.write("충분한 검토 없이 빠른 실행만 강조되어 품질 안정화나 데이터 유효성 리스크가 발생할 수 있습니다.")
                elif weakest == "실행형": st.write("의사결정이 지나치게 신중해지거나 회의만 길어지고 실제 추진으로 이어지는 동력이 약해질 수 있습니다.")
                elif weakest == "조율형": st.write("팀원 간 개별 플레이 성향이 짙어지거나 부서 간 사일로(장벽) 현상이 발생할 리스크가 있습니다.")
                elif weakest == "관리형": st.write("업무 표준이나 체계적인 가이드가 부족하여 예외 상황 발생 시 프로세스가 누락되거나 꼬일 수 있습니다.")
                
            st.divider()
            
            # [기존 대시보드 4번 데이터 테이블 유지]
            st.subheader("📋 4. 팀원별 진단 상세 raw data")
            st.dataframe(df_res, use_container_width=True)
            
            csv_data = df_res.to_csv(index=False, encoding="utf-8-sig")
            st.download_button(
                label="📥 전체 결과 CSV 파일 다운로드", 
                data=csv_data, 
                file_name="team_work_style_total_results.csv", 
                mime="text/csv"
            )
            
    elif input_pw != "":
        st.error("❌ 비밀번호가 올바르지 않습니다. 다시 입력해 주세요.")
