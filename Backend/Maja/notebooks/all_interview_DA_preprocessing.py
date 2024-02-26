#%%
from docx import Document
import pandas as pd
import numpy as np
import re
import spacy as sp
import nltk
from nltk.stem.snowball import DanishStemmer
import lemmy
# %%
def read_docx(file_path):
    doc = Document(file_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return ' '.join(text)
# %%
# Path to your .docx file
docx_file_path = '/Users/majastyrkandersen/Desktop/bispebjerg/interviews_merged.docx'

# Read the content of the .docx file
document_text = read_docx(docx_file_path)
# %%
# To lower case
lower_cased = document_text.lower()
# %%
# Remove punctuation
pattern = r'[^\w\s]'
cleaned = re.sub(pattern, '', lower_cased)
# %%
# Remove stopwords using spaCy

nlp = sp.load("da_core_news_sm")
# %%
# Rename un-tokenized data
text = cleaned

# Process the text data
doc = nlp(text)
# %%
# Remove stopwords

filtered_tokens = [token.text for token in doc if not token.is_stop]
# %%
# Remove names Oliver, Arthur, Sonja, and Charlotte
names = ["oliver", "sonja", "arthuer", "charlotte"]

tokens_without_names = list(filter(lambda x: x not in names, filtered_tokens))
# %%
# Normalizing the text (stemming and lemmatization) using NLTK

stemmer = DanishStemmer()
stemmed_tokens = [stemmer.stem(token) for token in tokens_without_names]
# %%
print(stemmed_tokens)
# %%
# Create an instance of the standalone lemmatizer (without POS (Parts of Speech))
lemmatizer = lemmy.load("da")
lemmatized_tokens = [lemmatizer.lemmatize("", token) for token in stemmed_tokens]
# %%
print(lemmatized_tokens)
# %%
# We got 6800 tokens
number_of_elements = len(lemmatized_tokens)
print(number_of_elements)
# %%

# TODO:
# Set up MLFlow
#define metrics to conduct experiements on
#save the best model

# TODO:
# Train a GPT model on ENG
# Train a GPT model on UKR
# Train a GPT model on DA

# TODO: 
# Train a BERT model on ENG
# Train a BERT model on UKR
# Train a BERT model on DA

# TODO: 
# Train a T5 model on ENG
# Train a T5 model on UKR
# Train a T5 model on DA

# T5 model - DA - UKR

## input --> "har du diabetes" 
## Whisper --> "har du diabetes" --> FT model --> "Do you have any KP"


#%%
from transformers import GPT2Model, GPT2Tokenizer
# %%

#preprocess data
#create pipeline
#different huggingface libs
#model --> decode 

## PROTOTYPE TESTING

## Frontend (React App)
    ## http POST request --> backend
## Backend (REST-API)
    ## POST request --> S2T (whisper)
    ## whisper --> string object
    ## fine-tuned model machine translation --> "nastrovia"
    ## POST request --> frontend

## fetch POST request from backend
## Display on app



