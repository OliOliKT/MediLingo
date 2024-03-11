import os
import pandas as pd
import json
from sklearn.model_selection import train_test_split

current_directory = os.path.dirname(__file__)
excel_dataset_filepath = os.path.join(current_directory, "dataset.xlsx")
csv_dataset_filepath = os.path.join(current_directory, "dataset.csv")
json_dataset_filepath = os.path.join(current_directory, "dataset.jsonl")
training_set_filepath = os.path.join(current_directory, "training_set.jsonl")
validation_set_filepath = os.path.join(current_directory, "validation_set.jsonl")

dataset_df = pd.read_excel(excel_dataset_filepath)

def excel_to_csv(input, output):
    input.to_csv(output, index = False, header = ["danish", "english", "ukranian"])
    return pd.read_csv(output)


def format_to_chatgpt_format(input, output):
    chatCompletion = []
    for idx, row in input.iterrows():
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


dataset_df_with_headers = excel_to_csv(dataset_df, csv_dataset_filepath)
format_to_chatgpt_format(dataset_df_with_headers, json_dataset_filepath)
train_and_val_set(dataset_df_with_headers, training_set_filepath, validation_set_filepath)