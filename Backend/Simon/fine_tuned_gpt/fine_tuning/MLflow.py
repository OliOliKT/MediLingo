import mlflow
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.meteor_score import meteor_score
from openai import OpenAI

API_KEY = "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"

client = OpenAI(api_key=API_KEY)

interviewOnly = ""
interviewAndQuestions = ""

interviewOnly_id= client.files.create(file=open(interviewOnly, "rb"), purpose="fine-tune").id
interviewAndQuestions_id = client.files.create(file=open(interviewAndQuestions, "rb"), purpose="fine-tune").id

epochs= [3, 4]
learning_rate_multiplier= [1.0,2.0]
batch_size= [32,64]
datasets = [interviewOnly_id, interviewAndQuestions_id]

#creating grid search over each hyperparameter combinations
for epoch in epochs:
    for learningRate in learning_rate_multiplier:
        for batchSize in batch_size:
            for dataset_id in datasets:
                job = client.fine_tuning.jobs.create(
                    training_file=dataset_id,
                    model="gpt-3.5-turbo",
                    hyperparameters={
                        "n_epochs": epoch,
                        "learning_rate_multiplier": learningRate,
                        "batch_size": batchSize
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
        
        generated_translation = completion.choices[0].message.content #generated sentence
        reference_translation = ukranian_radiograph_sentences[danish_radiograph_sentences.index(sentence)] #correct translation for the sentence

        bleu = sentence_bleu([reference_translation.split()], generated_translation.split())

        meteor = meteor_score([reference_translation], generated_translation)

        total_score.append(bleu+meteor)
    
    print("\nTotal score for " + model_id + ": " + str(total_score))

