# Swarsetu: Lyrics Translator

Swarsetu is a single-page Django web application designed to translate English song lyrics into Hindi and Bengali. It currently supports both offline dictionary based BASIC translation and online AI translation. 

## Important: First-Time Setup

```bash
# 1. Install dependencies
pip install django argostranslate spacy

# 2. Download the offline translation models
python download_models.py

# 3. Download the SpaCy dependencies for offline chunking
python -m spacy download xx_ent_wiki_sm
python -m spacy download xx_sent_ud_sm?

```

## About the AI translation

Please change the GEMINI_API_KEY in settings.py file to use your own Gemini Api key.