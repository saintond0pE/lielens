import os
from google import genai
from google.genai import types
from pydantic import ValidationError
from .models import AnalysisResult

def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    return genai.Client(api_key=api_key)

def analyze_content(content: str) -> AnalysisResult:
    """Analyzes the provided text using Gemini and returns a structured AnalysisResult."""
    client = get_client()
    
    prompt = f"""
    You are LieLens, an advanced digital forensic tool designed to act as an internet credibility and manipulation analysis system.
    Analyze the following internet content for manipulation, fake urgency, scam patterns, emotional pressure, unrealistic claims, fake authority behavior, engagement farming, and suspicious marketing tactics.
    
    Content to analyze:
    \"\"\"
    {content}
    \"\"\"
    
    Provide your analysis by populating the required JSON structure. Ensure the reasoning is written from the perspective of an analytical, serious intelligence engine.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AnalysisResult,
                temperature=0.2,
            ),
        )
        # Parse the JSON response
        result = AnalysisResult.model_validate_json(response.text)
        return result
    except ValidationError as e:
        raise RuntimeError(f"Failed to parse AI response: {e}")
    except Exception as e:
        raise RuntimeError(f"API Error: {e}")
