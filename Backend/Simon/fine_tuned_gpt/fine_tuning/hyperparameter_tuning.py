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
from rouge import Rouge

#from human_evaluation import generate_translations

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
datasets = [[interviewAndQuestions_train_50p, interviewAndQuestions_test_50p]]

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
        #return "test.jsonl"
        return "interviewOnly_val.jsonl"
    elif "interviewAndQuestions_25p" in dataset_name:
        #return "test.jsonl"
        return "interviewAndQuestions_val_25p.jsonl"
    elif "interviewAndQuestions_50p" in dataset_name:
        #return "test.jsonl"
        return "interviewAndQuestions_val_50p.jsonl"
    elif "interviewAndQuestions_100p" in dataset_name: 
        #return "test.jsonl"
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
#all the fine-tuned models generated from the grid-search like experiment
FT_model_ids = pd.read_csv("/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/results/IDs_and_hyperparameters.csv")

model_scores = {}

rouge = Rouge()

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
    total_rouge_n = 0
    
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

        bleu = sentence_bleu([reference_translation.split()], generated_translation.split(), smoothing_function=SmoothingFunction().method2)
        meteor = meteor_score([reference_translation.split()], generated_translation.split())
        scores  = rouge.get_scores(generated_translation, reference_translation)
        rouge_n_score = scores[0]['rouge-1']['f']
        
        count += 1
        
        total_bleu += bleu
        total_meteor += meteor
        total_rouge_n += rouge_n_score
        
    total_model_score = (total_bleu + total_meteor + total_rouge_n) / validation_set_length
    
    
    print("total BLEU: " + str(total_bleu))
    print("total METEOR: " + str(total_meteor))
    print("avg BLEU for: " + str(model_dataset) + " " + str((0.3965763478953719)))
    print("avg METEOR for: " + str(model_dataset) + " " + str((total_meteor/validation_set_length)))
    print("avg ROGUE_N for: " + str(model_dataset) + " " + str((total_rouge_n/validation_set_length)))
    print("total average (BLEU+METEOR+ROGUE_N) for " + str(model_dataset) + ": " + str((total_model_score)))
    total_scores["model_id: "] = model_id
    total_scores[f"validation_dataset_name"] = (specific_validationSet(model_dataset))
    total_scores[f"validation_dataset_size"] = (validation_set_length)
    total_scores[f"BLEU_smoothing_function"] = "method2"
    total_scores[f"total_bleu: "] = (total_bleu)
    total_scores[f"total_METEOR: "] = (total_meteor)
    total_scores[f"total_ROGUE_N: "] = (total_rouge_n)
    total_scores[f"average_bleu: "] = (total_bleu/validation_set_length)
    total_scores[f"average_METEOR: "] = (total_meteor/validation_set_length)
    total_scores[f"average_ROGUE_N: "] = (rouge_n_score/validation_set_length)
    
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

with open('/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/results/model_scores_withRogue.json', 'a') as f:
    json.dump(model_scores, f, indent=4)


#%%
################################################################################
################################################################################
################################################################################
########## ADDING ROUGE N: 
################################################################################
################################################################################
################################################################################


# FT_model_ids = pd.read_csv("/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/results/IDs_and_hyperparameters.csv")

# rouge = Rouge()

# with open('/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/results/model_scores_withRogue.json', 'r') as f:
#     model_scores = json.load(f)

# def calculate_rouge_scores(generated_translation, reference_translation):
#     scores = rouge.get_scores(generated_translation, reference_translation)
#     return scores[0]['rouge-1']['f']

# all_rouge_n_scores = {}

# for _, row in FT_model_ids.iterrows():
#     model_dataset = row["dataset"]
#     model_id = row["model_id"]
#     path = f"/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/preprocess/validation_sets/{specific_validationSet(model_dataset)}"
#     count = 1

#     print("Model_dataset: " + model_dataset)

#     validation_dataset = load_jsonlFile(path)
#     validation_dataset_sentence = convert_chatprompt_to_csv(validation_dataset)
#     validation_set_length = len(validation_dataset_sentence)
#     print("Validation_set name: "+ specific_validationSet(model_dataset) + " size:" +str(validation_set_length))
    
#     total_rouge_n = 0

#     for _, row in validation_dataset_sentence.iterrows():
#         target_sentence = row["danish"]
#         reference_translation = row["ukranian"]
#         print("count: " + str(count) + ", DK: " + target_sentence + ", UKR: " + reference_translation)
#         count += 1
        
#         completion = client.chat.completions.create(
#             model=model_id,
#             messages=[
#                 {"role": "system", "content": "Translate from danish to ukranian"},
#                 {"role": "user", "content": target_sentence}
#             ]
#         )
#         generated_translation = completion.choices[0].message.content #generated translated sentence


#         rouge_n_score = calculate_rouge_scores(generated_translation, reference_translation)
#         total_rouge_n += rouge_n_score
#         print("total rouge score: " + str(total_rouge_n))

#     # calculate average ROUGE-N score
#     average_rouge_n = total_rouge_n / len(validation_dataset_sentence)
#     print("avg rouge: " + str(average_rouge_n))
    
#     # add average ROUGE-N score to all_rouge_n_scores dictionary
#     all_rouge_n_scores[model_dataset] = average_rouge_n

# # append all ROUGE-N scores to the model_scores dictionary
# model_scores["total_avg_ROUGE_N_scores"] = all_rouge_n_scores

# # append updated model scores to the JSON file
# with open('/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/results/model_scores_withRogue.json', 'a') as f:
#     json.dump(model_scores, f, indent=4)

# # for testing purposes!
# # with open('/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/results/model_scores_withRogue_test.json', 'a') as f:
# #     json.dump(model_scores, f, indent=4)




#%%
################################################################################
################################################################################
################################################################################
########## GENERATE TRANSLATIONS FOR THE HUMAN EVALUATION:
################################################################################
################################################################################
################################################################################

danish_radiograph_sentences = {
    "MR": 
        ["Har du fået lavet kunstige led?",
        "Har du fået indopereret metal i kroppen?",
        "Er du blevet opereret i et andet land?",
        "Har du nogensinde fået metalsplinter i øjet?",
        "Har du arbejdet som smed, eller andet arbejdet der involverer metalsplinter?",
        "Har du nogen piercinger?",
        "Har du noget metal på dig, for eksempel piercinger?",
        "Har du hårnåle i håret?",
        "Er der nogen mulighed for at du kan være gravid?",
        "Er der en chance for, at du kunne være gravid?",
        "Har du en pacemaker?",
        "Er du hjerteopereret?",
        "Er du blevet opereret i hjertet?",
        "Føler du dig klaustrofobisk i små rum?",
        "Har du oplevet angst i trange eller små rum?",
        "Har du været soldat?",
        "Er du nogensinde blevet ramt af skud eller lignende?",
        "Hvornår fik du indsat din metalprotese?",
        "Har du nogen høreapparater?",
        "Er du nogensinde blevet opereret i hovedet?"],
    "CT": 
        ["Har du nogen kendte allergier?",
        "Har du haft allergiske symptomer tidligere?",
        "Er der noget, du ikke kan tåle på grund af allergi?",
        "Har du haft nogen nyresygdomme?",
        "Er dine nyrer blevet opereret",
        "Har du fået undersøgt din nyrefunktion?",
        "Har du diabetes?",
        "Har du sukkersyge?",
        "Har du fået taget en blodprøve?",
        "Tager du nogen form for medicin?",
        "Har du prøvet at få jod indeholdende kontrast før",
        "Har du nogensinde fået kontrastvæske før?",
        "Skete der noget sidste gang, du fik kontrast",
        "Skete der noget sidste gang, du fik en indsprøjtning med kontrasten?",
        "Du kan opleve en varmefornemmelse i kroppen, når du får kontrastinjektionen",
        "Det kan føles som om, du tisser, når du får kontrasten.",
        "Du kan få en metalsmag i munden af kontrasten",
        "Scanneren vil fortælle dig undervejs, at du skal trække vejret ind og holde det. Efterfølgende vil den også fortælle, når du skal trække vejret normalt igen.",
        "Under scanningen skal du trække vejret ind og holde det i ca. 4-5 sekunder.",
        "Du skal kunne ligge fladt ned på ryggen under hele scanningen"],
    "UL": 
        ["Har du prøvet at få taget en vævsprøve før?",
        "Har du prøvet at få taget en biopsi før?",
        "Er du bange for nåle?",
        "Vi skal tage en vævsprøve fra din lever",
        "Du kommer til at mærke et prik, når vævsprøven bliver taget",
        "Har du prøvet at få lokalbedøvelse før?",
        "Du skal have noget lokalbedøvelse, som bagefter skal have lov til at virke i et minuts tid",
        "Det må ikke gøre ondt, når du har fået lokalbedøvelsen",
        "Du kan mærke at det svier og spænder, når du får lokalbedøvelsen",
        "Efter bedøvelsen skal du ikke kunne mærke noget I det område",
        "Du skal have indsat et kateter i dine lunger",
        "Vi kommer til at hjælpe dig med at kunne trække vejret igen ved at indsætte et kateter i dine lunger",
        "Vi skal indsætte et kateter i dine lunger, så du kan trække vejret bedre",
        "Du kommer til at mærke et lille prik, for vi kan desværre ikke bedøve lunge hinden",
        "Lunge hinden kan desværre ikke bedøves, så du vil kunne mærke, når vi stikker igennem den",
        "Du har en masse væske i din mave, så vi kommer til at indsætte et dræn for at afhjælpe dig.",
        "Er det muligt at du kan ligge på din venstre side under scanningen?",
        "Det er afgørende, at du ligger stille gennem hele scanningen.",
        "Vi laver undersøgelsen sterilt, så det er meget vigtigt at du ikke rykker eller flytter dig undervejs, når vi stikker dig",
        "Det er vigtigt at du siger til, hvis du får det dårligt."]
}

def generate_translations(model_id, path):
    translations = []
    columns = ['danish', 'generated_translation']
    
    for sub_department in danish_radiograph_sentences:
        phrases = danish_radiograph_sentences[sub_department]

        for idx, sentence in enumerate(phrases):
            completion = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": "Translate from danish to ukranian"},
                    {"role": "user", "content": sentence}
                ]
            )
            
            generated_translation = completion.choices[0].message.content # generated translated sentence
            translations.append({'danish': sentence, 'generated_translation': generated_translation})
        
    df = pd.DataFrame(translations, columns=columns)
    df.to_excel(path, index=False)


# import pandas as pd
# from googletrans import Translator

# def generate_translations_GT(path):
#     translations = []
#     columns = ['danish', 'generated_translation']
#     translator = Translator()
    
#     for sub_department in danish_radiograph_sentences:
#         phrases = danish_radiograph_sentences[sub_department]

#         for idx, sentence in enumerate(phrases):
#             translation = translator.translate(sentence, src='da', dest='uk')
#             generated_translation = translation.text
#             translations.append({'danish': sentence, 'generated_translation': generated_translation})
        
#     df = pd.DataFrame(translations, columns=columns)
#     df.to_excel(path, index=False)


#%% 
# interviewOnly

interviewOnly_id = "ft:gpt-3.5-turbo-0125:personal:medilingo:94UzywmL"
generate_translations(interviewOnly_id, "/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/evaluation/evaluation_interviewOnly.xlsx")

# %%

# interviewAndQuestions_50p

interviewOnly_id = "ft:gpt-3.5-turbo-0125:personal:medilingo:94Zh7J6M"
generate_translations(interviewOnly_id, "/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/evaluation/evaluation_interviewAndQuestions_100percent.xlsx")
#%%

normal = "gpt-3.5-turbo"
generate_translations(normal, "/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/evaluation_excelFiles/evaluation_stdGPT.xlsx")



# %%

################################################################################
################################################################################
################################################################################
########## SCORES ON KNOWN QUESTIONS (HUMAN EVALUATION)
################################################################################
################################################################################
################################################################################



#%%
# #all the fine-tuned models generated from the grid-search like experiment
# FT_model_ids = {
#     "interviewAndQuestions_50p": "ft:gpt-3.5-turbo-0125:personal:medilingo:94WHfDoL",
#     "InterviewAndQuestions_100p": "ft:gpt-3.5-turbo-0125:personal:medilingo:94Zh7J6M"
# }

# model_scores = {}

# #calculating combined score (BLEU + METEOR) for each model

# for model_name in FT_model_ids:
    
#     model_id = FT_model_ids[model_name]
#     total_scores = {}
#     count = 1 #index starts at 0, but the first sentence is = 1
    
#     total_model_score = 0
#     for sub_department in danish_radiograph_sentences:
#         phrases = danish_radiograph_sentences[sub_department]
#         reference_translations = ukranian_radiograph_sentences[sub_department]
        
#         total_bleu = 0
#         total_meteor = 0
#         for idx, sentence in enumerate(phrases):
#             completion = client.chat.completions.create(
#                 model=model_id,
#                 messages=[
#                     {"role": "system", "content": "Translate from danish to ukranian"},
#                     {"role": "user", "content": sentence}
#                 ]
#             )
            
#             generated_translation = completion.choices[0].message.content #generated translated sentence
                
#             # Finding the corresponding Ukrainian translation using the index
#             reference_translation = ukranian_radiograph_sentences[sub_department][idx-1] #finding the correct ukraninan translation for the sentence
            
#             bleu = sentence_bleu([reference_translation.split()], generated_translation.split(),smoothing_function=SmoothingFunction().method2)

#             meteor = meteor_score([reference_translation.split()], generated_translation.split())
            
#             print("count: " + str(count) + " : " + sub_department)
#             count += 1
            
#             total_bleu += bleu
#             total_meteor += meteor
#             total_model_score += (bleu + meteor)
        
#         print("avg BLEU for: " + sub_department + " " + str((total_bleu/20)))
#         print("avg METEOR for: " + sub_department + " " + str((total_meteor/20)))
            
#         total_scores[sub_department + "_avg_bleu: "] = (total_bleu/20)
#         total_scores[sub_department + "_avg_METEOR: "] = (total_meteor/20)
    
#     #saving sub-department scores in a dictionary for the model
#     print(count)
#     total_scores["total_average_score(BLEU+METEOR)"] = (total_model_score/60)
#     model_scores[model_name] = total_scores

# print("model performance: ")
# print(model_scores)

# with open('/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/results/model_scores_evaluation_questions.json', 'w') as f:
#     json.dump(model_scores, f, indent=4)



# %%
