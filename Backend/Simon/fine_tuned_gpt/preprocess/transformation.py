#%%
import pandas as pd
import json
from sklearn.model_selection import train_test_split
#%%
def excel_to_csv(input, output):

    df = pd.read_excel(input).to_csv(output,index=False,header=["danish", "english", "ukranian"])
    

#%%
def get_dfs():
    
    df = pd.read_csv("dataset.csv")
    
    training, validation = train_test_split(df, train_size=0.8,shuffle=False)
    
    trainingSet = []
    for idx, row in training.iterrows():
        messages = []
        messages.append({"role": "system", "content": "Translating from Danish to Ukrainian for medical purposes"})
        messages.append({"role": "user", "content": row["danish"]})
        messages.append({"role": "assistant", "content": row["ukranian"]})
        trainingSet.append({"messages": messages})

    validationSet = []
    for idx, row in validation.iterrows():
        messages = []
        messages.append({"role": "system", "content": "Translating from Danish to Ukrainian for medical purposes"})
        messages.append({"role": "user", "content": row["danish"]})
        messages.append({"role": "assistant", "content": row["ukranian"]})
        validationSet.append({"messages": messages})
    
    with open("training_set.jsonl", 'w') as f:
        for sentence in trainingSet:
            f.write(json.dumps(sentence, ensure_ascii=False) + '\n')

    with open("validation_set.jsonl", 'w') as f:
        for sentence in validationSet:
            f.write(json.dumps(sentence, ensure_ascii=False) + '\n')

get_dfs()

# %%
