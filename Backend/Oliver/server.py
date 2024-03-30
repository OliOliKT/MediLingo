# import os
# from flask import Flask, jsonify, request
# from openai import OpenAI
# import openai_whisper

# app = Flask(__name__)

# with open("key.txt", 'r') as key_file:
#     API_KEY = key_file.read().strip()

# client = OpenAI(api_key=API_KEY)
# model = openai_whisper.load_model("base")


# @app.route('/transcribe', methods=['POST'])
# def transcribe_audio():
#     if 'audio' not in request.files:
#         return "Audio file is required.", 400
#     audio_file = request.files['audio']
#     audio_path = "./temp_audio.webm"
#     audio_file.save(audio_path)

#     # Process the audio file with Whisper
#     result = model.transcribe(audio_path)
    
#     os.remove(audio_path)
    
#     return jsonify({"text": result['text']})


# @app.route("/translate")
# def getTranslation(input):
#     completion = client.chat.completions.create(
#         model="ft:gpt-3.5-turbo-0125:personal:medilingo:8z7ujSsh",
#         messages=[
#             {"role": "system", "content": "Translating from Danish to Ukrainian for medical purposes"},
#             {"role": "user", "content": input}
#         ]
#     )
#     gen_translation = completion.choices[0].message.content
    
#     return gen_translation

# if __name__ == '__main__':
#     app.run(debug=True)