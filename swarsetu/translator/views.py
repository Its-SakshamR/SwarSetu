from django.shortcuts import render
import argostranslate.translate

def home(request):
    original_lyrics = ""
    translated_lyrics = ""
    target_lang = "hi" # Default to Hindi

    if request.method == "POST":
        original_lyrics = request.POST.get('lyrics', '')
        target_lang = request.POST.get('language', 'hi')

        if original_lyrics:
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
                translated_lyrics = f"Translation Error: {e}"

    return render(request, 'translator/index.html', {
        'original_lyrics': original_lyrics,
        'translated_lyrics': translated_lyrics,
        'target_lang': target_lang
    })