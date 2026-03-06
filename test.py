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
I could say I've seen this coming for some time
The way you seem to stare right through my eyes
Don't you trust me?
You can tell me anything
I already see right through your disguise

Let me know if I'm reaching
But I can feel this breaking
And I don't want to have to live on edge anymore
I can hear when you're sleeping
You're telling secrets as you're dreaming
I'm so unfazed I hardly feel upset anymore
I don't want no trouble, baby
I just want to say

If this is how it ends, then please do one last thing for me
Kiss me harder
Kiss mе harder
I know what it meant, but we'rе no longer what we need
Miss me harder
Miss me harder

I have to ask, was it him?
Or was it all on me
Or was it all because you listened to your friends?
You'll always be the one that got away
There's no debate
But leaving with questions is the worst kind of pain

Let me know if I'm reaching
But I can feel this breaking
And I don't want to have to live on edge anymore
I can hear when you're sleeping
You're telling secrets as you're dreaming
I'm so unfazed I hardly feel upset anymore
I don't want no trouble, baby
I just want to say

If this is how it ends, then please do one last thing for me
Kiss me harder
Kiss me harder
I know what it meant, but we're no longer what we need
Miss me harder
Miss me harder

Kiss me harder

Let me know if I'm reaching
I can feel this breaking
Let me know if I'm reaching
I pray to God I'm dreaming
"""

print(f"--- Original English ---\n{lyrics}\n")
print("--- Hindi Musical Translation ---")
print(translate_song_lyrics(lyrics))