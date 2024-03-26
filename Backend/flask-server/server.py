from flask import Flask
from openai import OpenAI

app = Flask(__name__)
with open("key.txt", 'r') as key_file:
    API_KEY = key_file.read().strip()

client = OpenAI(api_key=API_KEY)

@app.route("/route")
def getTranslation(input):
    
    completion = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:personal:medilingo:8z7ujSsh",
        messages=[
            {"role": "system", "content": "Translating from Danish to Ukrainian for medical purposes"},
            {"role": "user", "content": input}
        ]
    )
    gen_translation = completion.choices[0].message.content
    
    return gen_translation




