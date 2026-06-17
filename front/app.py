import streamlit as st
import requests

st.set_page_config(
    page_title="헬린이 탈출 운동 루틴 추천 앱"
)

st.title("헬린이를 위한 당일 컨디션 맞춤형 운동 루틴 추천 앱")

st.write(
    "오늘의 운동 목적, 타겟 부위, 피로도, 운동 가능 시간을 입력하면 "
    "FastAPI 백엔드가 조건에 맞는 당일 운동 루틴을 추천해줍니다."
)

st.divider()

goal = st.selectbox(
    "오늘의 운동 목적을 선택하세요",
    ["근력 향상", "근육량 증가", "다이어트", "체력 향상", "자세 교정/가벼운 운동"]
)

target_part = st.selectbox(
    "오늘 타겟으로 하고 싶은 운동 부위를 선택하세요",
    ["가슴", "등", "하체", "어깨", "전신"]
)

preference = st.selectbox(
    "선호하는 운동 방식을 선택하세요",
    ["상관없음", "머신 위주", "프리웨이트 위주", "맨몸 운동 위주"]
)

fatigue = st.slider(
    "현재 피로도 점수",
    min_value=1,
    max_value=5,
    value=3,
    help="1점: 팔팔함 / 5점: 매우 피곤함"
)

workout_time = st.number_input(
    "오늘 운동 가능 시간",
    min_value=20,
    max_value=90,
    value=60,
    step=5
)

st.caption("피로도가 높을수록 머신/저강도 중심으로 추천됩니다.")

st.divider()

if st.button("오늘의 운동 루틴 추천받기", use_container_width=True):
    payload = {
        "goal": goal,
        "target_part": target_part,
        "fatigue": fatigue,
        "workout_time": workout_time,
        "preference": preference
    }

    try:
        response = requests.post(
            "http://backend:8000/recommend",
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()

            st.subheader("오늘의 추천 루틴")
            st.success(result["routine_name"])

            summary_col1, summary_col2 = st.columns(2)

            with summary_col1:
                st.metric("운동 강도", result["intensity"])

            with summary_col2:
                st.metric("루틴 유형", result["routine_type"])

            st.write("### 추천 이유")
            st.info(result["recommend_reason"])

            st.write("### 추천 운동 구성")

            for idx, exercise in enumerate(result["exercises"], start=1):
                with st.container(border=True):
                    st.markdown(f"#### {idx}. {exercise['name']}")

                    info_col1, info_col2, info_col3 = st.columns(3)

                    with info_col1:
                        st.write("세트")
                        st.write(f"**{exercise['sets']}**")

                    with info_col2:
                        st.write("반복")
                        st.write(f"**{exercise['reps']}**")

                    with info_col3:
                        st.write("휴식")
                        st.write(f"**{exercise['rest']}**")

                    st.write("자세 팁")
                    st.write(exercise["tip"])

                    st.link_button("자세 참고 검색", exercise["reference_url"])

            st.write("### ※주의사항")
            st.warning(result["warning"])

            with st.expander("입력값 확인"):
                st.json(payload)

            st.caption(result["message"])

        else:
            st.error("FastAPI 요청에 실패했습니다.")
            st.write(f"상태 코드: {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error("백엔드 서버와 연결할 수 없습니다.")
        st.write(e)

st.divider()

st.caption(
    "본 추천은 일반적인 운동 루틴 예시입니다. 개인의 건강 상태, 통증 여부, 운동 경험에 따라 강도를 조절해야 합니다."
)