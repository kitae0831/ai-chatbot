import streamlit as st # streamlit 임포트
from openai import OpenAI # OpenAI 입포트

openai_api_key = st.secrets["OPENAI_API_KEY"]  # streamlit/.streamlit/secrets.toml 파일에 정의된 OPENAI_API_KEY 활용
client = OpenAI(api_key=openai_api_key) # OpenAI API 클라이언트 생성

st.title("내 가상친구 챗봇") # 제목 표시
st.divider() # 가로선 구분자 표시

if "messages" not in st.session_state: # session_state에 messages가 없으면 빈 리스트 생성
    st.session_state.messages = []
else: 
    for message in st.session_state.messages: # session_state에 messages가 있으면 모든 메시지를 순회
        with st.chat_message(message['role']): # 메시지 컨테이너(내용물을 담을 수 있는 공간)를 생성, message['role'] 값은 'human' 또는 'ai'로 둘 중 무엇이냐에 따라 컨테이너 디자인이 달라짐
            st.write(message['content']) # 메시지 내용 표시

user_input = st.chat_input("메시지를 입력하세요") # 사용자 입력 받기
if user_input:
    with st.chat_message("human"): # 사용자 메시지 컨테이너 생성
        st.write(user_input) # 사용자 메시지 표시
    
    st.session_state.messages.append({"role": "human", "content": user_input}) # 사용자 메시지를 session_state에 추가(사용자가 입력한 메시지의 role은 "human"으로 설정)
    
    completion = client.chat.completions.create( # OpenAI API 클라이언트를 사용하여 챗봇 응답 생성
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "넌 나의 가장 친한 친구야. 그리고 넌 항상 응원해주고 위로해줘. 그리고 항상 편하게 반말을 사용해."},
                {
                    "role": "user",
                    "content": user_input
                }
            ],
        )
    bot_response = completion.choices[0].message.content # 챗봇 응답 추출
    
    with st.chat_message("ai"): # 챗봇 메시지 컨테이너 생성
        st.write(bot_response) # 챗봇 메시지 표시
    
    st.session_state.messages.append({"role": "ai", "content": bot_response}) # 챗봇 응답을 session_state에 추가(챗봇 메시지의 role은 "ai"로 설정)