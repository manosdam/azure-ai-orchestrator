from openai import OpenAI
from dotenv import load_dotenv
import os
import glob
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


MODEL = "gpt-5-nano"
db_path = os.path.join("..", "vector_db")
load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key:
    print(f"OpenAI API Key exists")
else:
    print("OpenAI API Key not set")

folders = glob.glob("../file-repository/knowledge-base/*")
documents=[]
for folder in folders:
    doc_type = os.path.basename(folder)
    loader = DirectoryLoader(folder, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
    folder_docs = loader.load()
    for doc in folder_docs:
        doc.metadata["doc_type"] = doc_type
        documents.append(doc)
#print(documents[1])

text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
chunks = text_splitter.split_documents(documents)
#print(f"Divided into {len(chunks)} chunks")
#print(f"First chunk:\n\n{chunks[0]}")

embeddings = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
#embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

if os.path.exists(db_path):
    print(f"Cleaning up existing database at {db_path}...")
    vectorstore = Chroma(persist_directory=db_path, embedding_function=embeddings)  
    vectorstore.delete_collection()

vectorstore = Chroma.from_documents(documents= chunks, embedding= embeddings, persist_directory= db_path)
#print(f"Vectorstore created with {vectorstore._collection.count()} documents")

