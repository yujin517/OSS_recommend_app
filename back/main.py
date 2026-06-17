from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class WorkoutRequest(BaseModel):
    goal: str
    target_part: str
    fatigue: int
    workout_time: int
    preference: str


@app.get("/")
def root():
    return {"message": "Workout routine recommendation API is running"}


def get_intensity(fatigue: int):
    if fatigue <= 2:
        return "고강도"
    elif fatigue == 3:
        return "중간 강도"
    else:
        return "저강도"


def get_exercise_count(workout_time: int):
    if workout_time <= 30:
        return 3
    elif workout_time <= 60:
        return 4
    else:
        return 5


def get_goal_guide(goal: str):
    guides = {
        "근력 향상": {
            "style": "무게 중심",
            "rep_range": "5~8회",
            "rest": "90~120초",
            "message": "근력 향상이 목적이므로 반복 횟수는 낮추고 세트 사이 휴식은 충분히 가져가는 방식이 적합합니다."
        },
        "근육량 증가": {
            "style": "자극 중심",
            "rep_range": "8~12회",
            "rest": "60~90초",
            "message": "근육량 증가가 목적이므로 적당한 무게와 반복 횟수로 목표 부위의 자극을 충분히 가져가는 루틴이 적합합니다."
        },
        "다이어트": {
            "style": "짧은 휴식과 활동량 중심",
            "rep_range": "12~15회",
            "rest": "30~60초",
            "message": "다이어트가 목적이므로 휴식 시간을 짧게 가져가고 전체 운동량을 높이는 구성이 적합합니다."
        },
        "체력 향상": {
            "style": "전신 수행 능력 중심",
            "rep_range": "10~15회",
            "rest": "45~75초",
            "message": "체력 향상이 목적이므로 한 부위만 강하게 자극하기보다 지속적으로 움직일 수 있는 구성이 적합합니다."
        },
        "자세 교정/가벼운 운동": {
            "style": "안정성과 자세 중심",
            "rep_range": "10~12회",
            "rest": "60초",
            "message": "가벼운 운동과 자세 안정이 목적이므로 무게보다 정확한 자세와 부상 방지를 우선하는 구성이 적합합니다."
        }
    }
    return guides[goal]


EXERCISE_DB = {
    "가슴": {
        "free": [
            {
                "name": "벤치프레스",
                "tip": "어깨를 과하게 들지 말고 견갑을 고정한 상태에서 바를 가슴 중앙 쪽으로 내리세요.",
                "keyword": "벤치프레스 자세"
            },
            {
                "name": "인클라인 덤벨 프레스",
                "tip": "팔꿈치가 너무 벌어지지 않게 하고 덤벨을 밀 때 가슴 위쪽 자극을 느끼세요.",
                "keyword": "인클라인 덤벨 프레스 자세"
            },
            {
                "name": "덤벨 플라이",
                "tip": "팔을 완전히 펴기보다 살짝 굽힌 상태로 가슴을 열고 닫는 느낌으로 진행하세요.",
                "keyword": "덤벨 플라이 자세"
            }
        ],
        "machine": [
            {
                "name": "체스트 프레스 머신",
                "tip": "등을 패드에 붙이고 손목이 꺾이지 않도록 손잡이를 밀어주세요.",
                "keyword": "체스트 프레스 머신 자세"
            },
            {
                "name": "펙덱 플라이",
                "tip": "팔 힘보다 가슴을 모은다는 느낌으로 천천히 수축하세요.",
                "keyword": "펙덱 플라이 자세"
            },
            {
                "name": "스미스머신 인클라인 프레스",
                "tip": "바가 가슴 위쪽으로 내려오도록 벤치 각도를 조절하세요.",
                "keyword": "스미스머신 인클라인 프레스 자세"
            }
        ],
        "bodyweight": [
            {
                "name": "푸쉬업",
                "tip": "몸이 일직선이 되도록 유지하고 가슴이 바닥에 가까워질 때까지 내려가세요.",
                "keyword": "푸쉬업 자세"
            },
            {
                "name": "인클라인 푸쉬업",
                "tip": "손을 높은 곳에 두고 진행하여 부담을 낮추고 자세를 안정적으로 유지하세요.",
                "keyword": "인클라인 푸쉬업 자세"
            },
            {
                "name": "니 푸쉬업",
                "tip": "무릎을 바닥에 대고 진행하며 허리가 꺾이지 않게 주의하세요.",
                "keyword": "니 푸쉬업 자세"
            }
        ]
    },
    "등": {
        "free": [
            {
                "name": "바벨 로우",
                "tip": "허리를 둥글게 말지 말고 바를 배꼽 쪽으로 당기며 등을 조이세요.",
                "keyword": "바벨 로우 자세"
            },
            {
                "name": "덤벨 로우",
                "tip": "팔로만 당기지 말고 팔꿈치를 뒤로 보낸다는 느낌으로 당기세요.",
                "keyword": "덤벨 로우 자세"
            },
            {
                "name": "루마니안 데드리프트",
                "tip": "무릎을 살짝 굽히고 엉덩이를 뒤로 빼며 햄스트링과 등 후면 긴장을 유지하세요.",
                "keyword": "루마니안 데드리프트 자세"
            }
        ],
        "machine": [
            {
                "name": "랫풀다운",
                "tip": "어깨를 으쓱하지 말고 가슴을 세운 상태에서 바를 쇄골 쪽으로 당기세요.",
                "keyword": "랫풀다운 자세"
            },
            {
                "name": "시티드 로우",
                "tip": "허리를 세우고 팔꿈치를 몸 뒤로 보낸다는 느낌으로 당기세요.",
                "keyword": "시티드 로우 자세"
            },
            {
                "name": "어시스트 풀업 머신",
                "tip": "반동을 줄이고 등으로 몸을 끌어올린다는 느낌으로 진행하세요.",
                "keyword": "어시스트 풀업 머신 자세"
            }
        ],
        "bodyweight": [
            {
                "name": "밴드 로우",
                "tip": "밴드를 당길 때 어깨가 올라가지 않도록 주의하세요.",
                "keyword": "밴드 로우 자세"
            },
            {
                "name": "슈퍼맨 자세",
                "tip": "허리를 과하게 꺾지 말고 등과 엉덩이에 힘을 주며 상체를 들어올리세요.",
                "keyword": "슈퍼맨 운동 자세"
            },
            {
                "name": "인버티드 로우",
                "tip": "몸을 일직선으로 유지하고 가슴을 바 쪽으로 당기세요.",
                "keyword": "인버티드 로우 자세"
            }
        ]
    },
    "하체": {
        "free": [
            {
                "name": "스쿼트",
                "tip": "무릎이 안쪽으로 모이지 않게 하고 발바닥 전체로 바닥을 밀어주세요.",
                "keyword": "스쿼트 자세"
            },
            {
                "name": "런지",
                "tip": "앞쪽 무릎이 과하게 앞으로 쏠리지 않도록 중심을 잡으세요.",
                "keyword": "런지 자세"
            },
            {
                "name": "덤벨 루마니안 데드리프트",
                "tip": "허리를 말지 않고 엉덩이를 뒤로 빼며 천천히 내려가세요.",
                "keyword": "덤벨 루마니안 데드리프트 자세"
            }
        ],
        "machine": [
            {
                "name": "레그프레스",
                "tip": "무릎을 완전히 잠그지 말고 발판을 밀 때 허리가 뜨지 않게 주의하세요.",
                "keyword": "레그프레스 자세"
            },
            {
                "name": "레그 익스텐션",
                "tip": "반동을 줄이고 허벅지 앞쪽에 힘을 주며 천천히 올리세요.",
                "keyword": "레그 익스텐션 자세"
            },
            {
                "name": "레그 컬",
                "tip": "허리가 들리지 않게 고정하고 햄스트링으로 당기는 느낌을 유지하세요.",
                "keyword": "레그 컬 자세"
            }
        ],
        "bodyweight": [
            {
                "name": "맨몸 스쿼트",
                "tip": "상체를 너무 숙이지 말고 무릎과 발끝 방향을 맞추세요.",
                "keyword": "맨몸 스쿼트 자세"
            },
            {
                "name": "글루트 브릿지",
                "tip": "허리보다 엉덩이에 힘을 주며 골반을 들어올리세요.",
                "keyword": "글루트 브릿지 자세"
            },
            {
                "name": "스텝업",
                "tip": "올라갈 때 앞쪽 다리로 바닥을 밀어 올라가세요.",
                "keyword": "스텝업 운동 자세"
            }
        ]
    },
    "어깨": {
        "free": [
            {
                "name": "덤벨 숄더 프레스",
                "tip": "허리를 과하게 젖히지 말고 덤벨을 귀 옆에서 위로 밀어주세요.",
                "keyword": "덤벨 숄더 프레스 자세"
            },
            {
                "name": "사이드 레터럴 레이즈",
                "tip": "승모근이 과하게 개입되지 않도록 어깨를 내리고 팔을 옆으로 들어올리세요.",
                "keyword": "사이드 레터럴 레이즈 자세"
            },
            {
                "name": "리어 델트 플라이",
                "tip": "등보다 어깨 뒤쪽에 자극이 가도록 팔꿈치를 살짝 굽혀 진행하세요.",
                "keyword": "리어 델트 플라이 자세"
            }
        ],
        "machine": [
            {
                "name": "숄더 프레스 머신",
                "tip": "손잡이를 밀 때 허리가 뜨지 않도록 등받이에 등을 붙이세요.",
                "keyword": "숄더 프레스 머신 자세"
            },
            {
                "name": "케이블 레터럴 레이즈",
                "tip": "케이블 장력을 유지하면서 천천히 들어올리고 내려오세요.",
                "keyword": "케이블 레터럴 레이즈 자세"
            },
            {
                "name": "리버스 펙덱 플라이",
                "tip": "어깨 뒤쪽으로 팔을 벌린다는 느낌으로 천천히 진행하세요.",
                "keyword": "리버스 펙덱 플라이 자세"
            }
        ],
        "bodyweight": [
            {
                "name": "파이크 푸쉬업",
                "tip": "엉덩이를 높게 들고 머리가 바닥 쪽으로 내려가도록 진행하세요.",
                "keyword": "파이크 푸쉬업 자세"
            },
            {
                "name": "암 서클",
                "tip": "가볍게 어깨 관절을 풀어주며 통증이 없는 범위에서 진행하세요.",
                "keyword": "암 서클 운동"
            },
            {
                "name": "월 슬라이드",
                "tip": "등과 팔을 벽에 최대한 붙인 상태로 천천히 위아래로 움직이세요.",
                "keyword": "월 슬라이드 자세"
            }
        ]
    },
    "전신": {
        "free": [
            {
                "name": "덤벨 스쿼트 투 프레스",
                "tip": "스쿼트 후 일어나는 힘을 이용해 덤벨을 위로 밀어주세요.",
                "keyword": "덤벨 스쿼트 투 프레스 자세"
            },
            {
                "name": "케틀벨 스윙",
                "tip": "팔로 들어올리기보다 엉덩이를 접었다 펴는 힘으로 움직이세요.",
                "keyword": "케틀벨 스윙 자세"
            },
            {
                "name": "파머스 워크",
                "tip": "어깨를 내리고 복부에 힘을 준 상태로 안정적으로 걸으세요.",
                "keyword": "파머스 워크 자세"
            }
        ],
        "machine": [
            {
                "name": "로잉 머신",
                "tip": "다리로 밀고, 몸통을 세운 뒤 팔로 당기는 순서를 유지하세요.",
                "keyword": "로잉 머신 자세"
            },
            {
                "name": "트레드밀 인터벌",
                "tip": "무리한 속도보다 지속 가능한 속도로 걷기와 가벼운 뛰기를 반복하세요.",
                "keyword": "트레드밀 인터벌 운동"
            },
            {
                "name": "스텝밀",
                "tip": "손잡이에 체중을 과하게 싣지 말고 하체로 계단을 밟으세요.",
                "keyword": "스텝밀 자세"
            }
        ],
        "bodyweight": [
            {
                "name": "버피 테스트",
                "tip": "허리가 꺾이지 않도록 복부에 힘을 주고 피로하면 점프를 생략하세요.",
                "keyword": "버피 테스트 자세"
            },
            {
                "name": "마운틴 클라이머",
                "tip": "플랭크 자세를 유지하고 무릎을 가슴 쪽으로 번갈아 당기세요.",
                "keyword": "마운틴 클라이머 자세"
            },
            {
                "name": "플랭크",
                "tip": "허리가 처지지 않도록 복부와 엉덩이에 힘을 주세요.",
                "keyword": "플랭크 자세"
            }
        ]
    }
}


def choose_category(preference: str, fatigue: int):
    if fatigue >= 4:
        return "machine"

    if preference == "머신 위주":
        return "machine"
    elif preference == "프리웨이트 위주":
        return "free"
    elif preference == "맨몸 운동 위주":
        return "bodyweight"
    else:
        if fatigue <= 2:
            return "free"
        elif fatigue == 3:
            return "machine"
        else:
            return "bodyweight"


def build_exercises(target_part: str, category: str, count: int, guide: dict, fatigue: int):
    base_exercises = EXERCISE_DB[target_part][category]

    selected = []
    for exercise in base_exercises[:count]:
        if fatigue >= 4:
            sets = "2세트"
        elif fatigue == 3:
            sets = "3세트"
        else:
            sets = "3~4세트"

        selected.append({
            "name": exercise["name"],
            "sets": sets,
            "reps": guide["rep_range"],
            "rest": guide["rest"],
            "tip": exercise["tip"],
            "reference_url": f"https://www.youtube.com/results?search_query={exercise['keyword'].replace(' ', '+')}"
        })

    return selected


@app.post("/recommend")
def recommend_workout(data: WorkoutRequest):
    intensity = get_intensity(data.fatigue)
    exercise_count = get_exercise_count(data.workout_time)
    guide = get_goal_guide(data.goal)
    category = choose_category(data.preference, data.fatigue)

    exercises = build_exercises(
        target_part=data.target_part,
        category=category,
        count=exercise_count,
        guide=guide,
        fatigue=data.fatigue
    )

    if category == "free":
        category_text = "프리웨이트 중심"
    elif category == "machine":
        category_text = "머신 중심"
    else:
        category_text = "맨몸 운동 중심"

    routine_name = f"{data.target_part} {data.goal} 루틴"

    recommend_reason = (
        f"오늘의 운동 목적은 '{data.goal}'이고 타겟 부위는 '{data.target_part}'입니다. "
        f"현재 피로도는 {data.fatigue}점이므로 '{intensity}' 루틴으로 설정했습니다. "
        f"운동 가능 시간이 {data.workout_time}분이기 때문에 총 {len(exercises)}개의 운동을 추천합니다. "
        f"{guide['message']}"
    )

    if data.fatigue >= 4:
        warning = "피로도가 높은 상태이므로 무게 욕심을 내기보다 가벼운 중량과 정확한 자세를 우선하세요. 통증이나 어지러움이 있으면 운동을 중단하고 휴식을 권장합니다."
    elif data.workout_time <= 30:
        warning = "운동 시간이 짧기 때문에 준비운동을 생략하지 말고 핵심 운동 위주로 집중해서 진행하세요."
    else:
        warning = "운동 중 통증이 느껴지면 즉시 중단하고 세트 사이 휴식 시간을 충분히 조절하세요."

    return {
        "routine_name": routine_name,
        "intensity": intensity,
        "routine_type": category_text,
        "goal_style": guide["style"],
        "recommend_reason": recommend_reason,
        "exercises": exercises,
        "warning": warning,
        "message": "FastAPI에서 생성한 맞춤형 운동 루틴 추천 결과입니다."
    }