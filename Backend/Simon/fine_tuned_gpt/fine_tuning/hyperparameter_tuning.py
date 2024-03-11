import itertools
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.meteor_score import meteor_score
from openai import OpenAI

with open("key.txt", 'r') as key:
  API_KEY = key.read()
  
client = OpenAI(api_key=API_KEY)

interviewOnly = ""
interviewAndQuestions = ""

interviewOnly_id= client.files.create(file=open(interviewOnly, "rb"), purpose="fine-tune").id
interviewAndQuestions_id = client.files.create(file=open(interviewAndQuestions, "rb"), purpose="fine-tune").id

epochs= [3, 4]
learning_rate_multiplier= [1.0,2.0]
batch_size= [32,64]
datasets = [interviewOnly_id, interviewAndQuestions_id]

hyperparameter_combinations = itertools.product(epochs, learning_rate_multiplier, batch_size, datasets)

for epoch, learning_rate, batch_size, dataset_id in hyperparameter_combinations:

    #creating grid search over each hyperparameter combinations
    job = client.fine_tuning.jobs.create(
            training_file=dataset_id,
            model="gpt-3.5-turbo",
            suffix=f"E={epoch}_LR{learning_rate}_BS={batch_size}_ID={dataset_id}",
            hyperparameters={
                "n_epochs": epoch,
                "learning_rate_multiplier": learning_rate,
                "batch_size": batch_size
            }
        )

#questions in our test-sample-set for each subdepartment                        
danish_radiograph_sentences = [
    "Har du nogensinde fået metal i øjet?"
    
]

#correct translated sentence from danish to ukranian
ukranian_radiograph_sentences = [
    ""
]

#all the fine-tuned models generated from the grid-search like experiment
FT_model_ids = [
    ""
]          


model_scores = {}

#calculating combined score (BLEU + METEOR) for each model
for model_id in FT_model_ids:
    
    total_score = []
    
    for sentence in danish_radiograph_sentences:
        completion = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "Translate from danish to ukranian"},
                {"role": "user", "content": sentence}
            ]
        )
        
        generated_translation = completion.choices[0].message.content #generated translated sentence
        reference_translation = ukranian_radiograph_sentences[danish_radiograph_sentences.index(sentence)] #finding the correct ukraninan translation for the sentence
        
        bleu = sentence_bleu([reference_translation.split()], generated_translation.split())

        meteor = meteor_score([reference_translation], generated_translation)

        total_score.append(bleu+meteor)
    
    print("\nTotal score for " + model_id + ": " + str(total_score))
    
    #saving model in the dictionary
    
    model_scores[model_id] = sum(total_score)

    
