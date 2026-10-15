import requests
import streamlit as st
from dotenv import load_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model



st.title("YOU GOOD?")
# st.title("만나서 반갑습니다 :sunglasses:")

st.badge("환율")

# st.title("_Streamlit_ is :blue[cool] :sunglasses:")
# st.title("Dashboard", icon=":material/dashboard:")


page_1 = st.Page("page_1.py")
page_2 = st.Page("page_2.py")

pages = st.navigation([page_1, page_2], position = "top")

pages.run()