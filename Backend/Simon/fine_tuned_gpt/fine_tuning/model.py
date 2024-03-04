from openai import OpenAI
API_KEY = "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"
client = OpenAI(api_key=API_KEY)

phrase = "har du nogensinde fået metalsplinter i øjet?"

completion = client.chat.completions.create(
  model="ft:gpt-3.5-turbo-0125:personal:medilingo:8z7ujSsh",
  messages=[
    {"role": "system", "content": "Translate from danish to ukranian"},
    {"role": "user", "content": phrase}
  ]
)

print(completion.choices[0].message.content)
