#%% Imports and constants

import os

# OpenAI API key
API_KEY = "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"

# Current directory
current_directory = os.path.dirname(__file__)

# Default file paths
excel_questions_filepath = os.path.join(current_directory, "data", "questions", "questions.xlsx")
csv_interviews_filepath = os.path.join(current_directory, "data", "interviews", "interviews.csv")

# Created file paths
csv_questions_filepath = os.path.join(current_directory, "data", "questions", "questions.csv")
json_questions_filepath = os.path.join(current_directory, "data", "questions", "questions.jsonl")
training_questions_filepath = os.path.join(current_directory, "data", "questions", "training_set_questions.jsonl")
validation_questions_filepath = os.path.join(current_directory, "data", "questions", "validation_set_questions.jsonl")

json_interviews_filepath = os.path.join(current_directory, "data", "interviews", "interviews.jsonl")
training_interviews_filepath = os.path.join(current_directory, "data", "interviews", "training_set_interviews.jsonl")
validation_interviews_filepath = os.path.join(current_directory, "data", "interviews", "validation_set_interviews.jsonl")
json_interviews_synonym_filepath = os.path.join(current_directory, "data", "interviews", "interview_synonym.jsonl")

#%% Create datasets for questions

from Backend.Oliver.fineTuningModel.scripts.createDatasets import df_to_csv, format_to_chatgpt_format, train_and_val_set
import pandas as pd

# Convert Excel dataset to DataFrame
dataset_df = pd.read_excel(excel_questions_filepath)

# Convert DataFrame to CSV with headers and create DataFrame again
dataset_df_with_headers = df_to_csv(dataset_df, csv_questions_filepath)

# Convert DataFrame with headers to JSONL in ChatGPT format
format_to_chatgpt_format(dataset_df_with_headers, json_questions_filepath)

# Split dataset into training and validation sets
train_and_val_set(dataset_df_with_headers, training_questions_filepath, validation_questions_filepath)

#%% Tune model for questions

from Backend.Oliver.fineTuningModel.scripts.finetuning import tune_data

tune_data(training_questions_filepath, validation_questions_filepath, API_KEY)

#%% Test model for questions

from Backend.Oliver.fineTuningModel.scripts.model import test_model

phrase = "har du nogensinde fået metalsplinter i øjet?"
test_model(phrase)

#%% Validate training set for questions

from Backend.Oliver.fineTuningModel.scripts.validating import validate_data

validate_data(training_questions_filepath)

#%% Create datasets for interviews

from Backend.Oliver.fineTuningModel.scripts.createDatasets import format_to_chatgpt_format, train_and_val_set
import pandas as pd

dataset_df = pd.read_csv(csv_interviews_filepath)

format_to_chatgpt_format(dataset_df, json_interviews_filepath)

train_and_val_set(dataset_df, training_interviews_filepath, validation_interviews_filepath)

#%% Augment interview dataset

from Backend.Oliver.fineTuningModel.scripts.augmentation import backtranslate_augmenter, char_swap_augmenter, embed_and_translate

embed_and_translate(csv_interviews_filepath, json_interviews_synonym_filepath)

#%% Hyperparameter tuning

from Backend.Oliver.fineTuningModel.scripts.hyperparameter_tuning import generate_translations, save_as_csv, calculate_combined_score, create_hyperparameter_combinations, fine_tune_models

FT_model_ids = {
    "InterviewOnly": "ft:gpt-3.5-turbo-0125:personal:medilingo:8z7ujSsh"
}

best_model = {
    "InterviewOnly": "ft:gpt-3.5-turbo-0125:personal:medilingo:8z7ujSsh"
}

create_hyperparameter_combinations(API_KEY, training_interviews_filepath, validation_interviews_filepath)

fine_tune_models(API_KEY)

calculate_combined_score(API_KEY, FT_model_ids)

generated = generate_translations(API_KEY, best_model["InterviewOnly"])

save_as_csv(generated)