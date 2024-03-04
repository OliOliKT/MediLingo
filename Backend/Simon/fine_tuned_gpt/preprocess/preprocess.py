import pandas as pd
import json

def excel_to_csv(input, output):

    df = pd.read_excel(input).to_csv(output,index=False,header=["danish", "english", "ukranian"])
    
#excel_to_csv("dataset.xlsx","dataset.csv")

def csv_to_jsonl(input,output):
    csv_file = pd.read_csv(input)
    
    chatCompletion = []
    for index, row in csv_file.iterrows():
        messages = []
        messages.append({"role": "system", "content": "Translating from Danish to Ukrainian for medical purposes"})
        messages.append({"role": "user", "content": row["danish"]})
        messages.append({"role": "assistant", "content": row["ukranian"]})
        chatCompletion.append({"messages": messages})

    with open(output, 'w') as f:
        for sentence in chatCompletion:
            f.write(json.dumps(sentence,ensure_ascii=False) + '\n')

csv_to_jsonl("dataset.csv", "dataset.jsonl")


  