import os
import re
from google import genai
from google.genai import types
from pydantic import ValidationError
from .models import AnalysisResult

def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def heuristic_fallback(content: str) -> AnalysisResult:
    """A 'Zero-API' forensic engine that uses pattern matching for manipulation detection."""
    
    # Red Flag Patterns
    patterns = {
        "FAKE_URGENCY": [r"limited time", r"only \d+ spots", r"ending soon", r"don't wait", r"last chance"],
        "FINANCIAL_EXPLOITATION": [r"\$\d+,000", r"passive income", r"financial freedom", r"make money fast", r"automated income"],
        "AUTHORITY_SIMULATION": [r"proprietary algorithm", r"expert secrets", r"insider knowledge", r"proven system"],
        "EMOTIONAL_BAIT": [r"tired of your job", r"stop struggling", r"the secret they don't want you to know"],
    }
    
    detected = []
    score_penalty = 0
    
    for tactic, regexes in patterns.items():
        for reg in regexes:
            if re.search(reg, content, re.IGNORECASE):
                detected.append(tactic.replace("_", " "))
                score_penalty += 25
                break
                
    manipulation_score = min(score_penalty, 98)
    credibility_score = 100 - manipulation_score
    
    risk = "LOW"
    if manipulation_score > 75: risk = "CRITICAL"
    elif manipulation_score > 50: risk = "HIGH"
    elif manipulation_score > 25: risk = "MEDIUM"
    
    if not detected:
        detected = ["NO LINGUISTIC SCAM SIGNATURES DETECTED"]
        
    return AnalysisResult(
        credibility_score=credibility_score,
        manipulation_score=manipulation_score,
        tactics_detected=detected,
        risk_classification=risk,
        reasoning=f"FORENSIC HEURISTIC SCAN COMPLETE. Detection identified {len(detected)} manipulation vector(s). Analysis suggests a {risk} risk profile based on high-frequency linguistic scam signatures common in social engineering scripts.",
        ai_generated_probability=50 # Neutral default
    )

def analyze_content(content: str) -> AnalysisResult:
    """Analyzes the provided text using Gemini or falls back to heuristic engine."""
    client = get_client()
    
    if not client:
        # ZERO-API FALLBACK
        return heuristic_fallback(content)
    
    prompt = f"""
    You are LieLens, an advanced digital forensic tool.
    Analyze the following internet content for manipulation, fake urgency, and scam patterns.
    Content: \"\"\"{content}\"\"\"
    Return a structured AnalysisResult JSON.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash', # Fixed model name
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AnalysisResult,
                temperature=0.2,
            ),
        )
        return AnalysisResult.model_validate_json(response.text)
    except Exception as e:
        print(f"API FAILURE: {e}. SWITCHING TO HEURISTIC ENGINE.")
        return heuristic_fallback(content)
