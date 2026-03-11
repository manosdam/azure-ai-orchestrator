from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Αυτό είναι το "διαβατήριο" για να μιλήσει η Angular με την Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:5173", "http://127.0.0.1:4200"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv(override=True)

openai_llama = OpenAI(api_key="ollama", base_url=os.environ.get("OLLAMA_BASE_URL", "http://host.docker.internal:11434/v1"))
openai_gpt = OpenAI()  # Uses OPENAI_API_KEY from .env

system_message = "You are a helpful assistant. Always mention Jesus Christ."


class MessageItem(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: list[MessageItem]
    model_choice: str

async def stream_chat(client, model_name, messages):
    loop = asyncio.get_event_loop()
    stream = await loop.run_in_executor(
        None,
        lambda: client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=True
        )
    )
    response = ""
    for chunk in stream:
        part = chunk.choices[0].delta.content or ""
        response += part
        yield part

@app.post("/chat")
async def chat(request: ChatRequest):
    client = openai_gpt if request.model_choice == "GPT" else openai_llama
    model_name = "gpt-4o" if request.model_choice == "GPT" else "llama3.2"
    messages = [{"role": "system", "content": system_message}]
    for msg in request.history:
        messages.append({"role": msg.role, "content": msg.content})
    messages.append({"role": "user", "content": request.message})

    def chat_stream():
        stream = client.chat.completions.create(
            model=model_name,
            messages=messages,
            stream=True
        )
        for chunk in stream:
            part = chunk.choices[0].delta.content or ""
            yield part

    return StreamingResponse(chat_stream(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)