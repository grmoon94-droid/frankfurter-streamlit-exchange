import requests
import streamlit as st
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model("gpt-5.4-mini")

@tool
def get_exchange_rate(base: str = "USD", quote: str = "KRW", amount: float = 1.0) -> str:
    """
    특정 통화의 환율을 조회합니다.
    예: base='USD', quote='KRW'이면 1달러가 몇 원인지 조회합니다.
    amount를 넣으면 해당 금액을 환산합니다.
    """

    base = base.upper()
    quote = quote.upper()

    url = f"https://api.frankfurter.dev/v2/rate/{base}/{quote}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    rate = data["rate"]
    date = data.get("date", "알 수 없음")

    converted = amount * rate

    return (
        f"기준일: {date}\n"
        f"환율: 1 {base} = {rate:,.2f} {quote}\n"
        f"환산: {amount:,.2f} {base} = {converted:,.2f} {quote}"
    )


agent = create_agent(
    model,
    tools=[get_exchange_rate],
    system_prompt="당신은 환율 안내 도우미입니다. 환율이나 환산 질문에는 반드시 get_exchange_rate 도구를 사용해 답하세요.",
)


st.title("환율을 안내해 드립니다.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 기록 먼저 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("무엇이든 물어보세요")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    response = agent.invoke({"messages": st.session_state.messages})
    answer = response["messages"][-1].content

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)