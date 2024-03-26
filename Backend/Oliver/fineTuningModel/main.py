#%% Imports and constants

import os

# Current directory
current_directory = os.path.dirname(__file__)

# Default file paths
excel_questions_filepath = os.path.join(current_directory, "data", "questions", "questions.xlsx")
csv_interviews_filepath = os.path.join(current_directory, "data", "interviews", "interviews.csv")

# Question file paths
csv_questions_filepath = os.path.join(current_directory, "data", "questions", "questions.csv")
json_questions_filepath = os.path.join(current_directory, "data", "questions", "questions.jsonl")
training_questions_filepath = os.path.join(current_directory, "data", "questions", "training_set_questions.jsonl")
testing_questions_filepath = os.path.join(current_directory, "data", "questions", "testing_set_questions.jsonl")
validation_questions_filepath = os.path.join(current_directory, "data", "questions", "validation_set_questions.jsonl")

# Interview file paths
json_interviews_filepath = os.path.join(current_directory, "data", "interviews", "interviews.jsonl")
training_interviews_filepath = os.path.join(current_directory, "data", "interviews", "training_set_interviews.jsonl")
testing_interviews_filepath = os.path.join(current_directory, "data", "interviews", "testing_set_interviews.jsonl")
validation_interviews_filepath = os.path.join(current_directory, "data", "interviews", "validation_set_interviews.jsonl")
json_interviews_synonym_filepath = os.path.join(current_directory, "data", "interviews", "interview_synonym.jsonl")

# Hyperparameter tuning file paths
json_interview_questions_training = os.path.join(current_directory, "data", "evaluation", "interview_questions_training.jsonl")
json_interview_questions_validation = os.path.join(current_directory, "data", "evaluation", "interview_questions_validation.jsonl")

json_interview_questions_training_25p = os.path.join(current_directory, "data", "evaluation", "interview_questions_training_25p.jsonl")
json_interview_questions_testing_25p = os.path.join(current_directory, "data", "evaluation", "interview_questions_testing_25p.jsonl")

json_interview_questions_training_50p = os.path.join(current_directory, "data", "evaluation", "interview_questions_training_50p.jsonl")
json_interview_questions_testing_50p = os.path.join(current_directory, "data", "evaluation", "interview_questions_testing_50p.jsonl")

json_interview_questions_training_100p = os.path.join(current_directory, "data", "evaluation", "interview_questions_training_100p.jsonl")
json_interview_questions_testing_100p = os.path.join(current_directory, "data", "evaluation", "interview_questions_testing_100p.jsonl")

IDs_and_hyperparameters = os.path.join(current_directory, "data", "evaluation", "IDs_and_hyperparameters.csv")
evaluation_filepath = os.path.join(current_directory, "data", "evaluation")

evaluation_interview_filepath = os.path.join(current_directory, "data", "evaluation", "evaluation_interview.xlsx")
evaluation_interview_questions_50p_filepath = os.path.join(current_directory, "data", "evaluation", "evaluation_interview_questions_100percent.xlsx")
evaluation_stdGPT_filepath = os.path.join(current_directory, "data", "evaluation", "evaluation_stdGPT.xlsx")

model_scores_withRogue_json = os.path.join(current_directory, "data", "evaluation", "model_scores_withRogue.jsonl")

# OpenAI API key
key_filepath = os.path.join(current_directory, "scripts", "key.txt")
with open(key_filepath, 'r') as key:
  API_KEY = key.read()

#%% Create datasets for questions

from scripts.createDatasets import df_to_csv, format_to_chatgpt_format, train_test_val_set
import pandas as pd

# Convert Excel dataset to DataFrame
dataset_df = pd.read_excel(excel_questions_filepath)

# Convert DataFrame to CSV with headers and create DataFrame again
dataset_df_with_headers = df_to_csv(dataset_df, csv_questions_filepath)

# Convert DataFrame with headers to JSONL in ChatGPT format
format_to_chatgpt_format(dataset_df_with_headers, json_questions_filepath)

# Split dataset into training and validation sets
train_test_val_set(dataset_df_with_headers, training_questions_filepath, testing_questions_filepath, validation_questions_filepath)

#%% Create datasets for interviews

from scripts.createDatasets import format_to_chatgpt_format, train_test_val_set
import pandas as pd

dataset_df = pd.read_csv(csv_interviews_filepath)

format_to_chatgpt_format(dataset_df, json_interviews_filepath)

train_test_val_set(dataset_df, training_interviews_filepath, testing_interviews_filepath, validation_interviews_filepath)

#%% Hyperparameter tuning

from Backend.Oliver.fineTuningModel.scripts.hyperparameterTuning import generate_translations, calculate_scores, create_hyperparameter_combinations

create_hyperparameter_combinations(API_KEY, training_interviews_filepath, validation_interviews_filepath, IDs_and_hyperparameters)

calculate_scores(API_KEY, IDs_and_hyperparameters, evaluation_filepath, model_scores_withRogue_json)

# interviewOnly
interviewOnly_id = "ft:gpt-3.5-turbo-0125:personal:medilingo:94UzywmL"
generate_translations(interviewOnly_id, evaluation_interview_filepath, API_KEY)

# interviewAndQuestions_50p
interviewOnly_id = "ft:gpt-3.5-turbo-0125:personal:medilingo:94Zh7J6M"
generate_translations(interviewOnly_id, evaluation_interview_questions_50p_filepath, API_KEY)

# stdGPT
normal = "gpt-3.5-turbo"
generate_translations(normal, evaluation_stdGPT_filepath, API_KEY)

#%% Test model for questions

from scripts.model import test_model

phrase = "har du nogensinde fået metalsplinter i øjet?"
test_model(phrase, API_KEY)

#%% Validate training set for questions

from scripts.validating import validate_data

validate_data(training_questions_filepath)

#%% Augment interview dataset

from scripts.augmentation import embed_and_translate

embed_and_translate(csv_interviews_filepath, json_interviews_synonym_filepath)