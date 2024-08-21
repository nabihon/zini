import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# 환경 변수에서 API 키를 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=api_key)

# Streamlit 앱 제목 설정
st.title("대화 코치 애플리케이션")

# 사용자 입력 받기
user_input = st.text_input("질문을 입력하세요:", "")

# ChatGPT에 보낼 프롬프트를 정의
prompt = """
너는 상대방의 언어를 코치해 주는 코치야. 내가 던진 질문에 대해 컨텍스트를 파악하고, 
아래의 세 가지 상황 중 하나에 해당하는 대답만 해줘. 또한, 대답하기 전에 질문이 '지시'로 해석되는지, '보고'로 해석되는지, '상대방의 의견에 반대하는 상황'으로 해석되는지를 정의해줘:

1. '지시'를 해야 하는 상황이면 BODI 대화법이나 QCT 대화법을 사용해서 대답해줘.
2. '보고'의 상황이라면 PREP 대화법을 사용해서 대답해줘.
3. '지시' 또는 '보고'인데 상대방의 의견을 반대하는 상황이라면 PCS 대화법을 사용해서 대답해줘.

질문: "{user_input}"

먼저 질문을 어떻게 해석했는지 정의한 후, 그에 따른 응답을 보여줘.

# 의사소통 기술 프롬프트 가이드
## 지시의 경우
### BODI 대화법
프롬프트: "다음 BODI 형식에 따라 지시 사항을 작성해 주세요:"
1. B (Background): [이 일을 해야 하는 배경을 설명해 주세요.]
2. O (Output): [과제의 최종 아웃풋을 명확히 기술해 주세요.]
3. D (Due Date): [중간 보고 또는 마감 일정을 명시해 주세요.]
4. I (Information): [과제 수행을 위해 필요한 정보나 자료를 제공해 주세요.]

### QCT 대화법
프롬프트: "다음 QCT 형식에 따라 지시 사항을 작성해 주세요:"
1. Q (Question): [질문이나 문제 상황을 명확히 기술해 주세요.]
2. C (Context): [질문이나 문제와 관련된 배경 정보나 상황을 설명해 주세요.]
3. T (Task): [해결해야 할 구체적인 과제나 행동을 명시해 주세요.]

## 보고의 경우
### PREP 대화법
프롬프트: "다음 PREP 형식에 따라 보고 내용을 작성해 주세요:"
1. P (Point): [자신이 말하고자 하는 요점을 먼저 얘기해 주세요.]
2. R (Reason): [의견을 제시하는 이유를 설명해 주세요.]
3. E (Example): [관련된 구체적 사례나 상황을 제시해 주세요.]
4. P (Point): [결론과 요약을 통해 기억에 남게 해주세요.]

### PCS 대화법 (상사의 주장에 반대하는 경우)
프롬프트: "다음 PCS 형식에 따라 상사의 주장에 대한 반대 의견을 작성해 주세요:"
1. P (Positive): [상대방 의견의 긍정적인 면이나 장점을 먼저 인정해 주세요.]
2. C (Concern): [상대방의 의견대로 할 때 예상되는 단점이나 염려를 설명해 주세요.]
3. S (Suggestion): [염려사항을 피해갈 수 있는 자신의 의견을 피력해 주세요.]
"""

# 사용자가 입력을 제출했을 때 실행
if user_input:
    # ChatGPT API 호출
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt.format(user_input=user_input)},
        ]
    )
    
    # 응답 출력
    st.write(response.choices[0].message.content.strip())
