from pydantic import BaseModel, Field
from typing import List

class AnalysisResult(BaseModel):
    credibility_score: int = Field(description="Score from 0 to 100, where 100 is completely credible and 0 is highly deceptive/manipulative.")
    manipulation_score: int = Field(description="Score from 0 to 100, where 100 is highly manipulative and 0 is not manipulative at all.")
    tactics_detected: List[str] = Field(description="A list of specific manipulation tactics detected, e.g., 'Fake Urgency', 'Scam Language', 'Emotional Pressure'. Max 5.")
    risk_classification: str = Field(description="Overall risk level: 'LOW', 'MEDIUM', 'HIGH', or 'CRITICAL'.")
    reasoning: str = Field(description="A detailed but concise paragraph explaining why the content received these scores, acting as the 'Reasoning Engine' output.")
    ai_generated_probability: int = Field(description="Estimated probability (0-100) that the text is AI-generated.")
