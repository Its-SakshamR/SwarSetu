import os
# Force Argos to use the offline SpaCy engine instead of Stanza
os.environ['ARGOS_CHUNK_TYPE'] = 'SPACY'

from django.shortcuts import render
import argostranslate.translate
from django.conf import settings

def home(request):
    original_lyrics = ""
    translated_lyrics = ""
    target_lang = ""
    source_trans = ""

    if request.method == "POST":
        original_lyrics = request.POST.get('lyrics', '')
        target_lang = request.POST.get('language', 'hi')
        source_trans = request.POST.get('engine', 'dic')

        if original_lyrics:
            if source_trans == "api":
                LANGUAGE_CONFIG = {
                    'hi': {
                        'name': 'Hindi',
                        'script': 'Devanagari Hindi script',
                        'instruction': (
                            "You are a professional Bollywood songwriter fluent in Hindi. "
                            "Translate the following English song lyrics into Hindi. Requirements:\n"
                            "1. Maintain a rhyme scheme and rhythm so it can be sung.\n"
                            "2. Capture the feel and emotion — take poetic license where needed.\n"
                            "3. CRITICAL: Respond ONLY in proper Hindi Devanagari script (हिन्दी). "
                            "Do NOT use Roman script, transliteration, or Hinglish. "
                            "Every word must be written in Devanagari characters.\n"
                            "4. No explanations, no English, no romanized text — only the translated lyrics in Devanagari."
                        ),
                    },
                    'bn': {
                        'name': 'Bengali',
                        'script': 'Bengali script',
                        'instruction': (
                            "You are a professional Bengali songwriter and poet. "
                            "Translate the following English song lyrics into Bengali. Requirements:\n"
                            "1. Maintain a rhyme scheme and rhythm so it can be sung.\n"
                            "2. Capture the feel and emotion — take poetic license where needed.\n"
                            "3. CRITICAL: Respond ONLY in proper Bengali Devanagari script (বাংলা). "
                            "Do NOT use Roman script, transliteration, or any English words. "
                            "Every word must be written in Bengali alphabets.\n"
                            "4. No explanations, no English, no romanized text — only the translated lyrics in Bengali."
                        ),
                    },
                }
                
                try:
                    from google import genai as google_genai

                    api_key = settings.GEMINI_API_KEY
                    if not api_key:
                        raise RuntimeError(
                            "GEMINI_API_KEY is not set. "
                            "Set it via the GEMINI_API_KEY environment variable."
                        )

                    client = google_genai.Client(api_key=api_key)
                    config = LANGUAGE_CONFIG[target_lang]

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        config={
                            "system_instruction": config['instruction'],
                            "temperature": 0.7,
                        },
                        contents=original_lyrics,
                    )

                    translated_lyrics = response.text.strip()

                # except ImportError:
                #     raise RuntimeError(
                #         "google-genai package is not installed. "
                #         "Run: pip install google-genai."
                #     )
                except Exception as e:
                    translated_lyrics = f"Translation Error: {str(e)}"
            else:
                try:
                    lines = original_lyrics.split('\n')
                    translated_lines = []
                    
                    for line in lines:
                        if line.strip() == "":
                            translated_lines.append("")
                        else:
                            translated_line = argostranslate.translate.translate(
                                line, 'en', target_lang
                            )
                            translated_lines.append(translated_line)
                            
                    translated_lyrics = '\n'.join(translated_lines)
                    
                except Exception as e:
                    translated_lyrics = f"Translation Error: {str(e)}"

    return render(request, 'translator/index.html', {
        'original_lyrics': original_lyrics,
        'translated_lyrics': translated_lyrics,
        'target_lang': target_lang
    })