from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
import google.generativeai as genai
import asyncio
from concurrent.futures import ThreadPoolExecutor

load_dotenv(override=True)

app = FastAPI()

# Initialize LLM clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class QueryRequest(BaseModel):
    query: str

def get_claude_response(query: str) -> str:
    """Get response from Claude"""
    try:
        message = claude_client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": query}
            ]
        )
        return message.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"

def get_chatgpt_response(query: str) -> str:
    """Get response from ChatGPT"""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": query}
            ],
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def get_gemini_response(query: str) -> str:
    """Get response from Gemini"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(query)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

@app.post("/api/query")
async def query_llms(request: QueryRequest):
    """Send query to all three LLMs and return results"""
    query = request.query
    
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # Use ThreadPoolExecutor to run requests in parallel
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor()
    
    try:
        claude_task = loop.run_in_executor(executor, get_claude_response, query)
        chatgpt_task = loop.run_in_executor(executor, get_chatgpt_response, query)
        gemini_task = loop.run_in_executor(executor, get_gemini_response, query)
        
        claude_response, chatgpt_response, gemini_response = await asyncio.gather(
            claude_task, chatgpt_task, gemini_task
        )
        
        return {
            "query": query,
            "claude": claude_response,
            "chatgpt": chatgpt_response,
            "gemini": gemini_response
        }
    finally:
        executor.shutdown(wait=False)

@app.get("/")
async def get_index():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
