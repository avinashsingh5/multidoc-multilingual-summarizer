import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyBmCItd0IA2leLOtaQ6ULcoKXYjc4Q3-R8")

model = genai.GenerativeModel("gemini-2.0-flash")

def generate_summary_with_gemini(text: str, language: str = "English") -> str:
    try:
        prompt = f"""
        Summarize the following text in {language}.

        Text:
        {text}
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[ERROR] Could not generate summary: {str(e)}"
