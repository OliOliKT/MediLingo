from openai import OpenAI

def tune_data(training_file, validation_file, client, API_KEY):

  client = OpenAI(api_key=API_KEY)

  # Validating training file
  training_id = client.files.create(file=open(training_file, "rb"), purpose="fine-tune").id

  # Validating test file
  test_id = client.files.create(file=open(validation_file, "rb"), purpose="fine-tune").id

  # Creating the fine-tuning job with default parameters
  response = client.fine_tuning.jobs.create(
    training_file = training_id, 
    validation_file = test_id,
    model = "gpt-3.5-turbo",
    suffix = "MediLingo", 
    hyperparameters = {
      "n_epochs": 3,  
      "learning_rate_multiplier": 1, 
      "batch_size": 64,
    }
  )
  # Getting the tuning id
  tuning_id = response.id
  print("\n" + tuning_id)

  # Getting the status of the fine-tuning job
  response = client.fine_tuning.jobs.list_events(fine_tuning_job_id=tuning_id, limit=50)

  # Getting the messages from the fine-tuning job
  messages= response.data
  messages.reverse()
  print("\n")
  for m in messages:
      print(m.message)