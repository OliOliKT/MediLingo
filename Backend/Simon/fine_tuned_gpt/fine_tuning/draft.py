#%%
import itertools
import os
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score
from nltk.tokenize import word_tokenize
from openai import OpenAI
import time
import csv
import pandas as pd
import json
import numpy as np
from Backend.Simon.fine_tuned_gpt.fine_tuning.evaluation.human_evaluation import generate_translations

with open("/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/key.txt", 'r') as key:
  API_KEY = key.read()
  
client = OpenAI(api_key=API_KEY)

# datasets

interviewOnly_train = "/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/datasets/interviewOnly_train.jsonl"
interviewOnly_test = "/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/datasets/interviewOnly_test.jsonl"

interviewAndQuestions_train_25p = "/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/datasets/interviewAndQuestions_train_25p.jsonl"
interviewAndQuestions_test_25p = "/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/datasets/interviewAndQuestions_test_25p.jsonl"

interviewAndQuestions_train_50p = "/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/datasets/interviewAndQuestions_train_50p.jsonl"
interviewAndQuestions_test_50p = "/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/datasets/interviewAndQuestions_test_50p.jsonl"

interviewAndQuestions_train_100p = "/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/datasets/interviewAndQuestions_train_100p.jsonl"
interviewAndQuestions_test_100p = "/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/datasets/interviewAndQuestions_test_100p.jsonl"


#%%

#experiment
datasets = [[interviewOnly_train, interviewOnly_test],[interviewAndQuestions_train_25p, interviewAndQuestions_test_25p],
            [interviewAndQuestions_train_50p, interviewAndQuestions_test_50p],[interviewAndQuestions_train_100p, interviewAndQuestions_test_100p]]

models_and_parameters = []

for dataset_id in datasets:
    
    train_id = client.files.create(file=open(dataset_id[0], "rb"), purpose="fine-tune").id
    test_id = client.files.create(file=open(dataset_id[1], "rb"), purpose="fine-tune").id   
    dataset_name = client.files.retrieve(train_id).filename #filename for model suffix
    
    #creating grid search over each hyperparameter combinations
    job = client.fine_tuning.jobs.create(
            training_file=train_id,
            validation_file=test_id,
            model="gpt-3.5-turbo",
            suffix=f"MediLingo",
            hyperparameters={
                "n_epochs": 3,
            }
        )
    
    while True:
        job_info = client.fine_tuning.jobs.retrieve(job.id)
        if job_info.status == "succeeded":
            print(f"Fine-tuning job {job.id} completed")
            
            model_id = client.fine_tuning.jobs.retrieve(job.id).fine_tuned_model
            
            if "interviewOnly" in dataset_name:
                row = f"interviewOnly; {model_id}; {job.hyperparameters}"
                models_and_parameters.append(row) 
            elif "interviewAndQuestions_train_25p" in dataset_name:
                row = f"interviewAndQuestions_25p; {model_id}; {job.hyperparameters}"
                models_and_parameters.append(row)
            elif "interviewAndQuestions_train_50p" in dataset_name:
                row = f"interviewAndQuestions_50p; {model_id}; {job.hyperparameters}"
                models_and_parameters.append(row)
            else: 
                row = f"interviewAndQuestions_100p; {model_id}; {job.hyperparameters}"
                models_and_parameters.append(row)
            
            break
        elif job_info.status == "failed":
            print(f"Fine-tuning job {job.id} failed")
            break
        elif job_info.status == "cancelled":
            break
        else:
            print(job_info.status)
            print(f"Fine-tuning job {job.id} still running...")
            
            time.sleep(10) #wait 10 seconds before new check

#save all the finetuned models in a csv file
with open('/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/results/IDs_and_hyperparameters.csv', 'a', encoding='utf-8') as file:
    writer = csv.writer(file)
    for translation in models_and_parameters:
        dataset,model_id, hyper = translation.split(";")
        writer.writerow([dataset.strip(), model_id.strip(), hyper.strip()])

#questions in our test-sample-set for each subdepartment          

#%%

def load_jsonlFile(path):
    lines = []
    with open(path, 'r', encoding="utf-8") as file:
        for line in file:
            lines.append(json.loads(line))
    return lines

def specific_validationSet(dataset_name):

    if "interviewOnly" in dataset_name:
        return "interviewOnly_val.jsonl"
    elif "interviewAndQuestions_25p" in dataset_name:
        return "interviewAndQuestions_val_25p.jsonl"
    elif "interviewAndQuestions_50p" in dataset_name:
        return "interviewAndQuestions_val_50p.jsonl"
    else: 
        return "interviewAndQuestions_val_100p.jsonl"

def convert_chatprompt_to_csv(dataset):

    csv_messages = []
    
    for obj in dataset:
        danish_text = ""
        ukrainian_text = ""
        original_messages = obj["messages"]

        for message in original_messages:
            if message["role"] == "user":
                danish_text = message["content"]
            elif message["role"] == "assistant":
                ukrainian_text = message["content"]
    
        if danish_text and ukrainian_text:
            csv_messages.append((danish_text.strip(), ukrainian_text.strip()))

    path = "/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/results/TempValidation.csv"
    
    with open(path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['danish', 'ukranian'])

        for danish, ukrainian in csv_messages:
            writer.writerow([danish, ukrainian])

    output = pd.read_csv(path)
    
    os.remove(path)
    
    return output

#%%
#%%
#all the fine-tuned models generated from the grid-search like experiment
FT_model_ids = pd.read_csv("/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/results/IDs_and_hyperparameters.csv")

model_scores = {}

#various smoothfunctions for BLEU score

smoothFunctions = [".method0",".method1",".method2",".method3", ".method4", ".method5",".method6","method7"]

#calculating combined score (BLEU + METEOR) for each model

for _,row in FT_model_ids.iterrows():
    
    model_dataset = row["dataset"]
    model_id = row["model_id"]
    path = f"/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/preprocess/validation_sets/{specific_validationSet(model_dataset)}"
    #loading validation json file
    
    print(path)
    
    validation_dataset = load_jsonlFile(path)
    
    #converting the json to list of sentence pairs
    validation_dataset_sentence = convert_chatprompt_to_csv(validation_dataset)
    validation_set_length = len(validation_dataset_sentence)
    
    print("Validation_set name: "+ specific_validationSet(model_dataset) + " size:" +str(validation_set_length))
    
    best_model = {"best_dataset": "", "best_model_id": "","best_score": 0}
    total_scores = {}
    count = 1 #index starts at 0, but the first sentence is = 1
    print("Model_dataset: " + model_dataset)
    total_model_score = 0
    total_bleu = 0
    total_meteor = 0
    
    for _,row in validation_dataset_sentence.iterrows():    
        
        target_sentence = row["danish"]
        reference_translation = row["ukranian"]
        print("count: " + str(count) + ", DK: " + target_sentence + ", UKR: " + reference_translation)
        
        completion = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "Translate from danish to ukranian"},
                {"role": "user", "content": target_sentence}
            ]
        )
        
        generated_translation = completion.choices[0].message.content #generated translated sentence
        
        #bleu_smoothingMethod2 = sentence_bleu([reference_translation.split()], generated_translation.split(), smoothing_function=SmoothingFunction().method2)
        
        #experimenting with smoothing function
        
        bleu_smoothingMethod1 = sentence_bleu([reference_translation.split()], generated_translation.split(), smoothing_function=SmoothingFunction().method1)
        #bleu_smoothingMethod3 = sentence_bleu([reference_translation.split()], generated_translation.split(), smoothing_function=SmoothingFunction().method3)
        # print("bleu_smooth1: " + str(bleu_smoothingMethod1))
        # print("bleu_smooth2: " + str(bleu_smoothingMethod2))
        # print("bleu_smooth3:" + str(bleu_smoothingMethod3))

        meteor = meteor_score([reference_translation.split()], generated_translation.split())
        
        count += 1
        
        total_bleu += bleu_smoothingMethod1
        total_meteor += meteor
        
    total_model_score = (total_bleu + total_meteor) / validation_set_length
    
    
    print("total BLEU: " + str(total_bleu))
    print("total METEOR: " + str(total_meteor))
    print("avg BLEU for: " + str(model_dataset) + " " + str((total_bleu/validation_set_length)))
    print("avg METEOR for: " + str(model_dataset) + " " + str((total_meteor/validation_set_length)))
    print("total average (BLEU+METEOR) for " + str(model_dataset) + ": " + str((total_model_score)))
    total_scores["model_id: "] = model_id
    total_scores[f"validation_dataset_name"] = (specific_validationSet(model_dataset))
    total_scores[f"validation_dataset_size"] = (validation_set_length)
    total_scores[f"total_bleu: "] = (total_bleu)
    total_scores[f"total_METEOR: "] = (total_meteor)
    total_scores[f"average_bleu: "] = (total_bleu/validation_set_length)
    total_scores[f"average_METEOR: "] = (total_meteor/validation_set_length)
    
    #saving sub-department scores in a dictionary for the model
    
    current_bestModel_score = total_model_score

    if current_bestModel_score > best_model["best_score"]:
        best_model["best_dataset"] = model_dataset
        best_model["best_model_id"] = model_id
        best_model["best_score"] = current_bestModel_score
        
    total_scores["total_average_score(BLEU+METEOR)"] = current_bestModel_score
    model_scores[model_dataset] = total_scores

print("\nmodel performance: ")
print(model_scores)

print("\nbest model: ")
print(best_model)

with open('/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/results/model_scores.json', 'w') as f:
    json.dump(model_scores, f, indent=4)



#%%

########## GENERATE TRANSLATIONS FOR THE HUMAN EVALUATION:

# interviewOnly

interviewOnly_id = "ft:gpt-3.5-turbo-0125:personal:medilingo:94UzywmL"
generate_translations(interviewOnly_id, "/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/evaluation/evaluation_interviewOnly.csv")

# %%

# interviewAndQuestions_50p

interviewOnly_id = "ft:gpt-3.5-turbo-0125:personal:medilingo:94WHfDoL"
generate_translations(interviewOnly_id, "/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/evaluation/evaluation_interviewOnly.csv")

#%%

# %%

# interviewAndQuestions_50p

interviewOnly_id = "ft:gpt-3.5-turbo-0125:personal:medilingo:94WHfDoL"
generate_translations(interviewOnly_id, "/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/evaluation/evaluation_interviewOnly.csv")
