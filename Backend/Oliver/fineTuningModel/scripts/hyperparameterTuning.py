import os
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score
from openai import OpenAI
import time
import csv
import pandas as pd
import json
from rouge import Rouge


def create_hyperparameter_combinations(API_KEY, training_set, testing_set, IDs_and_hyperparameter_file):

    client = OpenAI(api_key=API_KEY)

    datasets = [[training_set, testing_set]]

    models_and_parameters = []

    for dataset_id in datasets:
        
        train_id = client.files.create(file=open(dataset_id[0], "rb"), purpose="fine-tune").id
        test_id = client.files.create(file=open(dataset_id[1], "rb"), purpose="fine-tune").id   
        dataset_name = client.files.retrieve(train_id).filename # Filename for model suffix
        
        # Create grid search over each hyperparameter combinations
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

                # row = f"{dataset_name}; {model_id}; {job.hyperparameters}"
                # models_and_parameters.append(row) 
                
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
                
                time.sleep(10) # Wait 10 seconds before new check

    with open(IDs_and_hyperparameter_file, 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        for translation in models_and_parameters:
            dataset, model_id, hyper = translation.split(";")
            writer.writerow([dataset.strip(), model_id.strip(), hyper.strip()])       


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
    elif "interviewAndQuestions_100p" in dataset_name: 
        return "interviewAndQuestions_val_100p.jsonl"

def convert_chatprompt_to_csv(dataset, file_path):

    csv_messages = []

    for object in dataset:
        danish_text = object["messages"][1]["content"]
        ukrainian_text = object["messages"][2]["content"]
        if danish_text and ukrainian_text:
            csv_messages.append((danish_text.strip(), ukrainian_text.strip())) 
    path = os.path.join(file_path, "TempValidation.csv")

    with open(path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['danish', 'ukranian'])

        for danish, ukrainian in csv_messages:
            writer.writerow([danish, ukrainian])

    output = pd.read_csv(path)
    
    os.remove(path)
    
    return output

# All the fine-tuned models generated from the grid-search like experiment
def calculate_scores(API_KEY, IDs_and_hyperparameter_file, validation_repo, model_scores_filepath):

    client = OpenAI(api_key=API_KEY)

    FT_model_ids = pd.read_csv(IDs_and_hyperparameter_file)

    model_scores = {}

    rouge = Rouge()

    # Calculating combined score (BLEU + METEOR) for each model

    for _,row in FT_model_ids.iterrows():
        
        model_dataset = row["dataset"]
        model_id = row["model_id"]
        path = f"{validation_repo}{specific_validationSet(model_dataset)}"        
        validation_dataset = load_jsonlFile(path)
        
        # Converting the json to list of sentence pairs
        validation_dataset_sentence = convert_chatprompt_to_csv(validation_dataset, validation_repo)
        validation_set_length = len(validation_dataset_sentence)
        
        print("Validation_set name: "+ specific_validationSet(model_dataset) + " size:" +str(validation_set_length))
        
        best_model = {"best_dataset": "", "best_model_id": "","best_score": 0}
        total_scores = {}
        count = 1 # Index starts at 0, but the first sentence is = 1
        print("Model_dataset: " + model_dataset)
        total_model_score = 0
        total_bleu = 0
        total_meteor = 0
        total_rouge_n = 0
        
        for _, row in validation_dataset_sentence.iterrows():    
            
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
            
            generated_translation = completion.choices[0].message.content # Generated translated sentence

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
        
        # Saving sub-department scores in a dictionary for the model
        
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

    with open(model_scores_filepath, 'a') as f:
        json.dump(model_scores, f, indent=4)


##########################################################
########## GENERATE TRANSLATIONS FOR THE HUMAN EVALUATION:
##########################################################

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

def generate_translations(model_id, path, API_KEY):
    client = OpenAI(api_key=API_KEY)
    translations = []
    columns = ['danish', 'generated_translation']
    
    for sub_department in danish_radiograph_sentences:
        phrases = danish_radiograph_sentences[sub_department]

        for _, sentence in enumerate(phrases):
            completion = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": "Translate from danish to ukranian"},
                    {"role": "user", "content": sentence}
                ]
            )
            
            generated_translation = completion.choices[0].message.content # Generated translated sentence
            translations.append({'danish': sentence, 'generated_translation': generated_translation})
        
    df = pd.DataFrame(translations, columns=columns)
    df.to_excel(path, index=False)