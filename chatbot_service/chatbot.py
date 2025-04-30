# backend/chatbot.py

from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
from langchain.schema.output_parser import StrOutputParser

def retrieve_response(user_input, chat_history):
    template = """
    You are a helpful assistant. 
    YOU MUST answer the following questions considering the 
    history of the conversation:
    Chat history: {chat_history}
    User question: {user_question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(model="gpt-4", max_tokens=5500)
    chain = prompt | llm | StrOutputParser()
    
    return chain.invoke({
        "chat_history": chat_history,
        "user_question": user_input
    })
