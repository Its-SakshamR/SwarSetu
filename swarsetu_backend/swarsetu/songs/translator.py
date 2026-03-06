from google import genai
import os

os.environ["GEMINI_API_KEY"] = "AIzaSyDNLSsvavhI8jwG-BMemK8tdlECXzPlKFA"

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def translate_song_lyrics(text):

    system_instruction = (
        "You are a professional Bollywood songwriter. Translate the following English "
        "song lyrics into Hindi. Maintain rhyme, rhythm, and emotional tone. "
        "Provide both Hindi script and Romanized (Hinglish). "
        "Return only the lyrics."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config={
            "system_instruction": system_instruction,
            "temperature": 0.7
        },
        contents=text
    )

    return response.text