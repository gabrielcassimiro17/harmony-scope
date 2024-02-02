from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI




def initialize_google_llm(model="gemini-pro"):
    return ChatGoogleGenerativeAI(model=model, convert_system_message_to_human=True)

def initialize_openai_llm(model="gpt-4-turbo-preview"):
    return ChatOpenAI(model=model)
