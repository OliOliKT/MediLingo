import pandas as pd
import json
from sklearn.model_selection import train_test_split

def df_to_csv(input, output):
    input.to_csv(output, index = False, header = ["danish", "english", "ukranian"])
    return pd.read_csv(output)


def format_to_chatgpt_format(input, output):
    chatCompletion = []
    for _, row in input.iterrows():
        messages = []
        messages.append({"role": "system", "content": "Translating from Danish to Ukrainian for medical purposes"})
        messages.append({"role": "user", "content": row["danish"]})
        messages.append({"role": "assistant", "content": row["ukranian"]})
        chatCompletion.append({"messages": messages})

    with open(output, 'w') as f:
        for object in chatCompletion:
            f.write(json.dumps(object, ensure_ascii=False) + '\n')


def train_and_val_set(input, training_output, validation_output):
    training, validation = train_test_split(input, train_size = 0.8, shuffle=False)
    format_to_chatgpt_format(training, training_output)
    format_to_chatgpt_format(validation, validation_output)