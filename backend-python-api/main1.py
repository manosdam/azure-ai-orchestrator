from pyexpat import model
from dotenv import load_dotenv
from openai import OpenAI
import os
import gradio as gr

load_dotenv(override=True)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

llama_llm = OpenAI(base_url=OLLAMA_BASE_URL, api_key= "OLLAMA")
gpt_llm = OpenAI()

def chat_function(model_choice, messages, history    ):
    if model_choice == "GPT":
        client = gpt_llm
        model = "llama3.2:latest"
    else:
            client = openai_gpt
            model_name = "gpt-4o-mini"
    





# Setup του Interface χωρίς την παράμετρο 'type' για αποφυγή του TypeError
view = gr.ChatInterface(
    fn=chat_function,
    additional_inputs=[
        gr.Dropdown(["LLAMA", "GPT"], label="Select model", value="LLAMA")
    ],
    title="AI Assistant - Secured local LLM Manager"
)

if __name__ == "__main__":
    view.launch(server_name="0.0.0.0", server_port=7860, share=True)