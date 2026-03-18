# Swarsetu: Lyrics Translator

Swarsetu is a single-page Django web application designed to translate English song lyrics into Hindi and Bengali. It currently supports both offline dictionary based BASIC translation and online AI translation. 

## Important: First-Time Setup

```bash
# 1. Set up a virtual env and activate it
python3 -m venv venv
source venv/bin/activate

# 2. Download the requirements
pip install -r requirements.txt

# 3. Download offline dict
python download_models.py

```

## About the AI translation

Please change the GEMINI_API_KEY in settings.py file to use your own Gemini Api key.