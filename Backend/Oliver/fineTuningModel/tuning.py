from openai import OpenAI
import os

# API_KEY = "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"
API_KEY = "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"

client = OpenAI(api_key=API_KEY)

current_directory = os.path.dirname(__file__)
training_file_path = os.path.join(current_directory, "training_set.jsonl")
validation_file_path = os.path.join(current_directory, "validation_set.jsonl")

training_id = client.files.create(file = open(training_file_path, "rb"), purpose = "fine-tune").id
test_id = client.files.create(file=open(validation_file_path, "rb"), purpose = "fine-tune").id

response = client.fine_tuning.jobs.create(
                                        training_file = training_id, 
                                        validation_file = test_id,
                                        model = "gpt-3.5-turbo",
                                        suffix = "MediLingo", 
                                        hyperparameters={
                                                        "n_epochs": 3,  
                                                        "learning_rate_multiplier": 1, 
                                                        "batch_size": 64,
                                        }
)

tuning_id = response.id
print("\n" + tuning_id)

response = client.fine_tuning.jobs.list_events(fine_tuning_job_id = tuning_id, limit = 50)

messages = response.data
messages.reverse()

print("\n")
for m in messages:
    print(m.message)
  