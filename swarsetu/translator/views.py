import os
os.environ['ARGOS_CHUNK_TYPE'] = 'SPACY'        
# This is used because the basic translation (offline) was accessing the stanza chunker
# which was accessing internet (Stanza checks github to see if it's the latest version),
# but we wanted to run it offline, so we opted for spacy chunker, which is not only fast
# but also doesn't require internet access.

from django.shortcuts import render
import argostranslate.translate
from django.conf import settings
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

def home(request):
    original_lyrics = ""
    translated_lyrics = ""
    orig_lang = ""
    target_lang = ""
    source_trans = ""
    script_selected = ""
    romanized_lines = []
    romanized_lyrics = ""

    if request.method == "POST":
        original_lyrics = request.POST.get('lyrics', '')
        orig_lang = request.POST.get('orig_lang', 'en')
        target_lang = request.POST.get('target_lang', 'hi')
        script_selected = request.POST.get('script', 'orig')
        source_trans = request.POST.get('engine', 'dic')
        
        if(orig_lang == target_lang):
            return render(request, 'translator/index.html', {
                'source_trans': source_trans,
                'original_lyrics': original_lyrics,
                'translated_lyrics': original_lyrics,
                'orig_lang': orig_lang,
                'target_lang': target_lang,
                'script_selected': script_selected
            })
        
        lang_map = {
            "hi": "Hindi",
            "bn": "Bengali",
            "ur": "Urdu",
            "en": "English"
        }
        orig_lang_name = lang_map.get(orig_lang, "the original language")

        if original_lyrics:
            if source_trans == "api":
                LANGUAGE_CONFIG = {
                    'hi': {
                        'name': 'Hindi',
                        'script': 'Devanagari Hindi script',
                        'instruction': (
                            "You are a professional Bollywood songwriter fluent in Hindi. "
                            f"Translate the following {orig_lang_name} song lyrics into Hindi. Requirements:\n"
                            "1. Maintain a rhyme scheme and rhythm so it can be sung.\n"
                            "2. Capture the feel and emotion — take poetic license where needed.\n"
                            "3. CRITICAL: Respond ONLY in proper Hindi Devanagari script (हिन्दी). "
                            "Do NOT use Roman script, transliteration, or Hinglish. "
                            "Every word must be written in Devanagari characters.\n"
                            f"4. No explanations, no {orig_lang_name}, no romanized text — only the translated lyrics in Devanagari."
                        ),
                    },
                    'bn': {
                        'name': 'Bengali',
                        'script': 'Bengali script',
                        'instruction': (
                            "You are a professional Bengali songwriter and poet. "
                            f"Translate the following {orig_lang_name} song lyrics into Bengali. Requirements:\n"
                            "1. Maintain a rhyme scheme and rhythm so it can be sung.\n"
                            "2. Capture the feel and emotion — take poetic license where needed.\n"
                            "3. CRITICAL: Respond ONLY in proper Bengali Devanagari script (বাংলা). "
                            "Do NOT use Roman script, transliteration, or any English words. "
                            "Every word must be written in Bengali alphabets.\n"
                            f"4. No explanations, no {orig_lang_name}, no romanized text — only the translated lyrics in Bengali."
                        ),
                    },
                    'ur': {
                        'name': 'Urdu',
                        'script': 'Nastaliq Urdu script',
                        'instruction': (
                            "You are a professional Urdu songwriter and poet. "
                            f"Translate the following {orig_lang_name} song lyrics into Urdu. Requirements:\n"
                            "1. Maintain a rhyme scheme and rhythm so it can be sung.\n"
                            "2. Capture the feel and emotion — take poetic license where needed.\n"
                            "3. CRITICAL: Respond ONLY in proper Nastaliq Urdu script (اردو). "
                            "Do NOT use Roman script, transliteration, or any English words. "
                            "Every word must be written in Urdu alphabets.\n"
                            f"4. No explanations, no {orig_lang_name}, no romanized text — only the translated lyrics in Urdu."
                        )
                    },
                    'en': {
                        'name': 'English',
                        'script': 'Latin script',
                        'instruction': (
                            "You are a professional songwriter and poet fluent in English. "
                            f"Translate the following {orig_lang_name} song lyrics into English. Requirements:\n"
                            "1. Maintain a rhyme scheme and rhythm so it can be sung.\n"
                            "2. Capture the feel and emotion — take poetic license where needed.\n"
                            "3. CRITICAL: Respond ONLY in proper English Latin script. "
                            "Do NOT use any non-English words. "
                            "Every word must be written in English alphabets.\n"
                            f"4. No explanations, no {orig_lang_name}, no romanized text — only the translated lyrics in English."
                        )
                    }
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
                            if orig_lang == 'en' or target_lang == 'en':
                                translated_line = argostranslate.translate.translate(
                                    line, orig_lang, target_lang
                                )
                            else:
                                intermediate_line = argostranslate.translate.translate(
                                    line, orig_lang, 'en'
                                )
                                translated_line = argostranslate.translate.translate(
                                    intermediate_line, 'en', target_lang
                                )
                            translated_lines.append(translated_line)
                            
                    translated_lyrics = '\n'.join(translated_lines)
                    
                except Exception as e:
                    translated_lyrics = f"Translation Error: {str(e)}"

    def romanize_urdu(text):
        # Map written by AI
        urdu_map = {
            # Base Consonants
            'ا': 'a', 'ب': 'b', 'پ': 'p', 'ت': 't', 'ٹ': 't', 'ث': 's',
            'ج': 'j', 'چ': 'ch', 'ح': 'h', 'خ': 'kh', 'د': 'd', 'ڈ': 'd',
            'ذ': 'z', 'ر': 'r', 'ڑ': 'r', 'ز': 'z', 'ژ': 'zh', 'س': 's',
            'ش': 'sh', 'ص': 's', 'ض': 'z', 'ط': 't', 'ظ': 'z', 'ع': 'a',
            'غ': 'gh', 'ف': 'f', 'ق': 'q', 'ک': 'k', 'گ': 'g', 'ل': 'l',
            'م': 'm', 'ن': 'n', 'ں': 'n', 'و': 'w', 'ہ': 'h', 'ھ': 'h',
            'ی': 'y', 'ے': 'e',
            
            # Missing Vowels, Hamzas & Variations
            'آ': 'aa',  # Alif Madda (Long A)
            'ئ': 'i',   # Hamza on Yeh
            'ؤ': 'o',   # Hamza on Waw
            'أ': 'a',   # Hamza on Alif
            'ي': 'y',   # Arabic Yeh (often generated by translation models)
            
            # Punctuation
            '،': ',',   # Arabic Comma
            '؟': '?',   # Arabic Question Mark
            '۔': '.',   # Urdu Full Stop
            
            # Diacritics (Harakat)
            'َ': 'a',   # Zabar (Top line)
            'ِ': 'i',   # Zer (Bottom line)
            'ُ': 'u',   # Pesh (Top curl)
            'ّ': '',    # Tashdeed (Emphasis mark - safely ignored for basic Romanization)

            # Spacing
            ' ': ' ', '\n': '\n'
        }
        return "".join(urdu_map.get(char, char) for char in text)
    
    if script_selected == "iast" and translated_lyrics and target_lang in ['hi', 'bn', 'ur']:
        try:
            source_script = sanscript.DEVANAGARI if target_lang == 'hi' else sanscript.BENGALI
            for line in translated_lyrics.split('\n'):
                if line.strip() == "":
                    romanized_lines.append("")
                else:
                    if target_lang == 'ur':
                            roman_line = romanize_urdu(line)
                    else:
                        roman_line = transliterate(line, source_script, sanscript.IAST)
                        
                    romanized_lines.append(roman_line.lower())

            romanized_lyrics = '\n'.join(romanized_lines)
        except Exception as e:
            romanized_lyrics = f"Transliteration Error: {str(e)}"
            
        translated_lyrics = romanized_lyrics
    
    return render(request, 'translator/index.html', {
        'source_trans': source_trans,
        'original_lyrics': original_lyrics,
        'translated_lyrics': translated_lyrics,
        'orig_lang': orig_lang,
        'target_lang': target_lang,
        'script_selected': script_selected
    })