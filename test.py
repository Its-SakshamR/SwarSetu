from google import genai
import os

# Replace with your actual key
os.environ["GEMINI_API_KEY"] = "AIzaSyDNLSsvavhI8jwG-BMemK8tdlECXzPlKFA"

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def translate_song_lyrics(english_para):
    # This prompt tells the AI to prioritize the 'vibe' over literal meaning
    system_instruction = (
        "You are a professional Bollywood songwriter. Translate the following English "
        "song lyrics into Hindi. Requirements: \n"
        "1. Maintain a rhyme scheme.\n"
        "2. Ensure the rhythm matches so it can be sung to some tune.\n"
        "3. Capture the 'feel' and emotion, even if it requires taking the poetic license\n"
        "4. Provide the Hindi script and the Romanized (Hinglish) version."
        "Just give the translated lyrics without any explanations or additional text (in romanized)."
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config={
            "system_instruction": system_instruction,
            "temperature": 0.7, # Higher temperature for creative "soul"
        },
        contents=english_para
    )

    return response.text

# Example: A paragraph from "Perfect" by Ed Sheeran
lyrics = """
song lyrics here
"""

print(f"--- Original English ---\n{lyrics}\n")
print("--- Hindi Musical Translation ---")
print(translate_song_lyrics(lyrics))