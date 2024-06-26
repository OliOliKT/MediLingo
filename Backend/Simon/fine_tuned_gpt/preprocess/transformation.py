#%%
import pandas as pd
import json
from sklearn.model_selection import train_test_split
#%%
def excel_to_csv(input, output):

    df = pd.read_excel(input).to_csv(output,index=False,header=["danish", "english", "ukranian"])

excel_to_csv("/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/preprocess/datasets/interview1.xlsx", "interview1.csv")

#%%

def csv_to_jsonl(input,output):
    
    df = pd.read_csv(input)
    
    jsonl = []
    for idx, row in df.iterrows():
        messages = []
        messages.append({"role": "system", "content": "Translating from Danish to Ukrainian for medical purposes"})
        messages.append({"role": "user", "content": row["danish"]})
        messages.append({"role": "assistant", "content": row["ukranian"]})
        jsonl.append({"messages": messages})

    with open(output, 'w') as f:
        for sentence in jsonl:
            f.write(json.dumps(sentence, ensure_ascii=False) + '\n')
            
csv_to_jsonl("/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/preprocess/old_datasets/original_interview.csv","original_interview.jsonl")

#%%

def combine_csv(file1, file2, output_file):

    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    combined_df = pd.concat([df1, df2], ignore_index=True)
    
    combined_df.to_csv(output_file, index=False)

combine_csv("/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/preprocess/datasets/f_interview.csv", "/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/preprocess/datasets/interview3.csv","interview_all.csv")

#%%
def get_dfs():
    
    data = []
    with open("/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/preprocess/final_datasets/interviewAndQuestions_100p.jsonl", 'r') as f:
        for line in f:
            data.append(json.loads(line))
    
    dataset, validation_set = train_test_split(data, train_size=0.90,shuffle=True)
    
    training, test= train_test_split(dataset, train_size=0.80,shuffle=True)
    
    with open("interviewAndQuestions_train_100p.jsonl", 'w') as f:
        for item in training:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    with open("interviewAndQuestions_test_100p.jsonl", 'w') as f:
        for item in test:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
            
    with open("interviewAndQuestions_val_100p.jsonl", 'w') as f:
        for item in validation_set:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

get_dfs()

# %%
