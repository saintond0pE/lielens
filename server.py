import os
import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import time

from core.analyzer import analyze_content

# Configure logging for a "Forensic" feel
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | [LIELENS-ENGINE] | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("lielens")

load_dotenv()

app = FastAPI(
    title="LIELENS Forensic Engine",
    description="Digital intelligence analysis for internet credibility."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class AnalyzeRequest(BaseModel):
    content: str

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Forensic-Time"] = str(process_time)
    return response

@app.get("/api/status")
async def status():
    return {
        "status": "online",
        "engine": "v2.0-forensic",
        "timestamp": time.time(),
        "providers": ["Puter-Cloud", "Local-Gemini"]
    }

@app.post("/api/analyze")
async def analyze(request: AnalyzeRequest):
    logger.info(f"Target acquisition initiated. Content length: {len(request.content)} chars")
    try:
        start_time = time.time()
        result = analyze_content(request.content)
        duration = time.time() - start_time
        logger.info(f"Analysis complete in {duration:.2f}s. Credibility Score: {result.credibility_score}%")
        return {"status": "success", "data": result.model_dump()}
    except Exception as e:
        logger.error(f"SYSTEM FAILURE during analysis: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Forensic Engine Failure: " + str(e)}
        )

@app.get("/")
async def root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    logger.info("Initializing LIELENS Forensic Engine on port 8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")
