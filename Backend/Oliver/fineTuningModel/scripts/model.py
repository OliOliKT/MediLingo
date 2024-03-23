from openai import OpenAI


def test_model(phrase, API_KEY):
  client = OpenAI(api_key=API_KEY)
  completion = client.chat.completions.create(
    model = "ft:gpt-3.5-turbo-0125:personal:medilingo:8z7ujSsh",
    messages = [
      {"role": "system", "content": "Translate from danish to ukranian"},
      {"role": "user", "content": phrase}
    ]
  )

  print(completion.choices[0].message.content)