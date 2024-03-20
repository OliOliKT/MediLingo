#%% Imports and constants

import os

# OpenAI API key
API_KEY = "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"

# Current directory
current_directory = os.path.dirname(__file__)

# Default file paths
excel_questions_filepath = os.path.join(current_directory, "data", "questions.xlsx")
csv_interviews_filepath = os.path.join(current_directory, "data", "interviews.csv")

# Created file paths
csv_questions_filepath = os.path.join(current_directory, "data", "questions.csv")
json_questions_filepath = os.path.join(current_directory, "data", "questions.jsonl")
training_questions_filepath = os.path.join(current_directory, "data", "training_set_questions.jsonl")
validation_questions_filepath = os.path.join(current_directory, "data", "validation_set_questions.jsonl")

json_interviews_synonym_filepath = os.path.join(current_directory, "data", "interview_synonym.jsonl")

#%% Create datasets

from createDatasets import df_to_csv, format_to_chatgpt_format, train_and_val_set
import pandas as pd

# Convert Excel dataset to DataFrame
dataset_df = pd.read_excel(excel_questions_filepath)

# Convert DataFrame to CSV with headers and create DataFrame again
dataset_df_with_headers = df_to_csv(dataset_df, csv_questions_filepath)

# Convert DataFrame with headers to JSONL in ChatGPT format
format_to_chatgpt_format(dataset_df_with_headers, json_questions_filepath)

# Split dataset into training and validation sets
train_and_val_set(dataset_df_with_headers, training_questions_filepath, validation_questions_filepath)

#%% Tune the model

from finetuning import tune_data

tune_data(training_questions_filepath, validation_questions_filepath, API_KEY)

#%% Test the model

from model import test_model

phrase = "har du nogensinde fået metalsplinter i øjet?"
test_model(phrase)

#%% Validate training set

from validating import validate_data

validate_data(training_questions_filepath)

#%% Augment dataset

from augmentation import backtranslate_augmenter, char_swap_augmenter, embed_and_translate

embed_and_translate(csv_interviews_filepath, json_interviews_synonym_filepath)   