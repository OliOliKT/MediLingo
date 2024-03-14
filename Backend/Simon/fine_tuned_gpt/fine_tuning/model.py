from openai import OpenAI
with open("key.txt", 'r') as key:
  API_KEY = key.read()
  
client = OpenAI(api_key=API_KEY)

phrase = "Har du nogen form for sukkersyge?"

completion = client.chat.completions.create(
  model="ft:gpt-3.5-turbo-0125:personal:medilingo:8z7ujSsh",
  messages=[
    {"role": "system", "content": "Translate from danish to ukranian"},
    {"role": "user", "content": phrase}
  ]
)

print(completion.choices[0].message.content)
