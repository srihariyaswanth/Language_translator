import os
from flask import Flask, render_template, request, jsonify, send_from_directory
# from googletrans import Translator
from deep_translator import GoogleTranslator
from gtts import gTTS
app = Flask(__name__)
# translator = Translator()
AUDIO_DIR = 'static/audio'

# Ensure the audio directory exists
os.makedirs(AUDIO_DIR, exist_ok=True)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    spoken_text = data['text']
    print(f'Received text: {spoken_text}')
    src_lang = data.get('src', 'en')  # Default to English as source language
    dest_lang = data.get('dest', 'ta')  # Default to Hindi as destination language
    # print(f"Received text: {spoken_text}")
    print(f"Source language: {src_lang}")
    print(f"Destination language: {dest_lang}")

    try:
        # Translate the recognized text to the desired language
        # translation = translator.translate(spoken_text, src=src_lang, dest=dest_lang)
        translated_text = GoogleTranslator(source=src_lang, target=dest_lang).translate(spoken_text)
        # translated_text = translation.text
        print(f'Translated text: {translated_text}')  # Print in the command prompt

        # Save the translated speech using gTTS
        audio_file_path = os.path.join(AUDIO_DIR, 'translated_speech.mp3')
        tts = gTTS(translated_text, lang=dest_lang)
        tts.save(audio_file_path)

        # Send the translated text and audio file URL back to the client
        return jsonify({'translatedText': translated_text, 'audioUrl': '/audio/translated_speech.mp3'})
    except Exception as e:
        print(f"Error: {str(e)}")  # Print any error to the command prompt
        return jsonify({'error': str(e)}), 500
@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)
if __name__ == "__main__":
    app.run(debug=True)
