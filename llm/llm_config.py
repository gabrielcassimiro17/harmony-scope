from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import os
import streamlit as st


def initialize_google_llm(model="gemini-pro"):
    return ChatGoogleGenerativeAI(
        model=model,
        convert_system_message_to_human=True,
        google_api_key=os.getenv("GOOGLE_API_KEY") or st.secrets["GOOGLE_API_KEY"],
    )


def initialize_openai_llm(model="gpt-4-turbo-preview"):
    return ChatOpenAI(model=model)
