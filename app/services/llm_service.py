import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_resume(text: str):
    prompt = f"""
    You are an AI HR assistant.

    Return ONLY valid JSON in this format:

    {{
      "ats_score": number,
      "skills": ["skill1", "skill2"],
      "missing_skills": ["skill1"],
      "interview_questions": ["q1", "q2"],
      "improvements": ["i1", "i2"]
    }}

    Resume:
    {text}
    """

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text