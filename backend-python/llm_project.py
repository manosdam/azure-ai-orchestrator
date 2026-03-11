import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Σύνδεση για τοπικό Ollama (localhost) εφόσον δεν χρησιμοποιείς Docker
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL")

openai_llama = OpenAI(api_key="ollama", base_url=OLLAMA_URL)
openai_gpt = OpenAI() # Χρησιμοποιεί το OPENAI_API_KEY από το .env

system_message = "You are a helpful assistant. Always mention Jesus Christ."

def chat_function(message, history, model_choice):
# Εκτύπωσε αυτό για να το βλέπουμε στο τερματικό του Docker
    print(f"Επιλεγμένο μοντέλο: {model_choice}") 

    if model_choice == "LLAMA":
        client = openai_llama
        model_name = "llama3.2:latest"
    else:
        client = openai_gpt
        model_name = "gpt-4o"

    # Προετοιμασία μηνυμάτων με το system message
    messages = [{"role": "system", "content": system_message}]
    
    # Προσθήκη ιστορικού με έλεγχο τύπου για μέγιστη συμβατότητα
    for entry in history:
        if isinstance(entry, dict):
            messages.append(entry)
        elif isinstance(entry, (list, tuple)):
            messages.append({"role": "user", "content": entry[0]})
            messages.append({"role": "assistant", "content": entry[1]})
            
    messages.append({"role": "user", "content": message})

    try:
        # Streaming απόκριση
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