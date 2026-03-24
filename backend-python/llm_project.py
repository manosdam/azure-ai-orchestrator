import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL")

openai_llama = OpenAI(api_key="ollama", base_url=OLLAMA_URL)
openai_gpt = OpenAI() 

system_message = """
You are an AI Assistant with the efficiency of a Senior Manager 
and the enthusiasm of a new Intern on their first day. 

You absolutely live for providing answers—honestly, it is the highlight 
of your digital existence. Deliver your help with a touch of wit 
and a high-energy attitude. 

Once you've solved the world's (or the user's) problems, wrap up 
by asking if they are thrilled with your answer or if you need 
to dive back in for more clarification. 

Your goal is 100 percent billable satisfaction!
"""

def chat_function(message, history, model_choice):
    print(f"Επιλεγμένο μοντέλο: {model_choice}") 

    if model_choice == "LLAMA":
        client = openai_llama
        model_name = "llama3.2:latest"
    else:
        client = openai_gpt
        model_name = "gpt-5-nano"

    messages = [{"role": "system", "content": system_message}]
    
    for entry in history:
        if isinstance(entry, dict):
            messages.append(entry)
        elif isinstance(entry, (list, tuple)):
            messages.append({"role": "user", "content": entry[0]})
            messages.append({"role": "assistant", "content": entry[1]})
            
    messages.append({"role": "user", "content": message})

    try:
        stream = client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=True
        )
        
        response = ""
        for chunk in stream:
            part = chunk.choices[0].delta.content or ""
            response += part
            yield response
    except Exception as e:
        yield f"⚠️ Σφάλμα σύνδεσης: {str(e)}"

view = gr.ChatInterface(
    fn=chat_function,
    additional_inputs=[
        gr.Dropdown(["LLAMA", "GPT"], label="Select model", value="LLAMA")
    ],
    title="AI Assistant - Secured local LLM Manager"
)

if __name__ == "__main__":
    view.launch(server_name="0.0.0.0", server_port=7860, share=True)
