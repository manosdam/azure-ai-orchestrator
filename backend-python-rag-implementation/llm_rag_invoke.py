from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage,AIMessage
from langchain_huggingface import HuggingFaceEmbeddings
import gradio as gr

MODEL = "gpt-5-nano"
db_path = os.path.join("..", "vector_db")
load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory=db_path, embedding_function=embeddings)
# print(f"Vectorstore contains {vectorstore._collection.count()} documents")

retriever = vectorstore.as_retriever()
llm = ChatOpenAI(temperature=0, model_name=MODEL)

SYSTEM_PROMPT_TEMPLATE = """
You are a knowledgeable, friendly assistant, chatting with a user.
If relevant, use the given context to answer any question.
If you don't know the answer, say so.
Context:
{context}
"""

def answer_question(question: str, history):
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)
    messages = [SystemMessage(content=SYSTEM_PROMPT_TEMPLATE.format(context=context))]

    for message in history:
        if message["role"] == "user":
            messages.append(HumanMessage(content=message["content"]))
        elif message["role"] == "assistant":
            messages.append(AIMessage(content=message["content"]))

    messages.append(HumanMessage(content=question))
    response = llm.invoke(messages)
    return response.content


if __name__ == "__main__":
    gr.ChatInterface(fn=answer_question).launch() # Προσθήκη type="messages"