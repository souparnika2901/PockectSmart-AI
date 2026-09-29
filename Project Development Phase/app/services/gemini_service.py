import json,re
from app.config import settings
try:
    from google import genai
    from google.genai import types
except ImportError:
    genai=None; types=None
SYSTEM='''You are PocketSmart AI, a practical budget planning assistant.
Return ONLY valid JSON. Never invent exact live prices or claim live availability.
Use the supplied demo marketplace catalog as the only source for product prices/platforms.
Respect the user's total budget. Keep recommendations concise.
Required keys: summary, allocation, tips, recommendations.
Each recommendation must have name, category, platform, estimated_price, currency, reason, url.
'''
def extract_json(text):
    text=re.sub(r"^```(?:json)?\s*","",text.strip(),flags=re.I)
    text=re.sub(r"\s*```$","",text)
    a,b=text.find("{"),text.rfind("}")
    if a<0 or b<0: raise ValueError("Model did not return JSON.")
    return json.loads(text[a:b+1])
def generate(prompt, image_bytes=None, mime_type=None):
    if genai is None:
        raise RuntimeError("Google GenAI library is not installed")

    if not settings.gemini_api_key:
        raise RuntimeError("Gemini API key is empty")

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    contents = [prompt]

    if image_bytes and mime_type:
        contents.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type
            )
        )

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM,
            temperature=0.35,
            max_output_tokens=2500,
            response_mime_type="application/json"
        )
    )

    return extract_json(response.text), "gemini"