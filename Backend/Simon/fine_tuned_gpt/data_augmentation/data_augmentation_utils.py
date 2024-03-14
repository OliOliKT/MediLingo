#%%
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from textattack.augmentation import EmbeddingAugmenter, CharSwapAugmenter, EasyDataAugmenter, CheckListAugmenter, WordNetAugmenter
import pandas as pd
import json
import random
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('stopwords')


#BACKTRANSLATION - DANISH to GERMAN to DANISH

DA_DE_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-da-de")
DA_DE_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-da-de")

DE_DA_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-de-da")
DE_DA_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-de-da")

#CharSwap
CS_augmenter = CharSwapAugmenter()

#EMBEDDING - ENGLISH to DANISH

EN_DA_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-da")
EN_DA_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-da")

EM_augmenter = CheckListAugmenter()

## translation
def danish_to_german(sentence):
    inputs_da = DA_DE_tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    translation_ids_de = DA_DE_model.generate(**inputs_da)
    da_sentence = DA_DE_tokenizer.decode(translation_ids_de[0], skip_special_tokens=True)
    return da_sentence

def german_to_danish(sentence):
    inputs_de = DE_DA_tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    translation_ids_da = DE_DA_model.generate(**inputs_de)
    de_sentence = DE_DA_tokenizer.decode(translation_ids_da[0], skip_special_tokens=True)
    return de_sentence


######### augmentation on the JSON file

def backtranslation_danish(sentence):
    # max_length = 512
    
    # # Check if the number of tokens in the sentence exceeds the maximum length
    # number_of_tokens = DA_DE_tokenizer.tokenize(sentence)
    
    # if len(number_of_tokens) > max_length:
    #     # Split the sentence into chunks
    #     chunks = []
    #     start = 0
    #     while start < len(number_of_tokens):
    #         chunks.append(number_of_tokens[start:start+max_length])
    #         start += max_length
        
    #     # Translate each chunk separately
    #     backtranslated_chunks = []
    #     for chunk in chunks:
    #         translated_sentence = danish_to_german(chunk)
    #         backtranslated_chunk = german_to_danish(translated_sentence)
    #         backtranslated_chunks.append(backtranslated_chunk)
        
    #     # Concatenate the backtranslated chunks
    #     backtranslated_sentence = " ".join(backtranslated_chunks)
    #     return backtranslated_sentence
    # else:
        # If the sentence doesn't exceed the maximum length, directly translate it
        translated_sentence = danish_to_german(sentence)
        backtranslated_sentence = german_to_danish(translated_sentence)
        return backtranslated_sentence
        

def load_jsonlFile(path):
    lines = []
    with open(path, 'r', encoding="utf-8") as file:
        for line in file:
            lines.append(json.loads(line))
    return lines

def write_jsonlFile(file ,path):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(file, ensure_ascii=False) + '\n')

def augmentation_BackTrans(input_file, output_file):
    dataset = load_jsonlFile(input_file)

    for obj in dataset:
        original_messages = obj["messages"]
        augmented_messages = []

        for message in original_messages:
            if message["role"] == "user":
                danish_text = message["content"]
                backtranslated_danish = backtranslation_danish(danish_text)
                message["content"] = backtranslated_danish

            augmented_messages.append(message)

        augmented_obj = {"messages": augmented_messages}
        write_jsonlFile(augmented_obj, output_file)

def CharSwap(input_file, output_file):
    dataset = load_jsonlFile(input_file)

    for obj in dataset:
        original_messages = obj["messages"]
        augmented_messages = []

        for message in original_messages:
            if message["role"] == "user":
                danish_text = message["content"]
                backtranslated_danish = CS_augmenter.augment(danish_text)
                message["content"] = backtranslated_danish
            elif message["role"] == "assistant":
                ukrainian_text = message["content"]
                backtranslated_ukrainian = CS_augmenter.augment(ukrainian_text)
                message["content"] = backtranslated_ukrainian

            augmented_messages.append(message)

        augmented_obj = {"messages": augmented_messages}
        write_jsonlFile(augmented_obj, output_file)

######### augmentation on csv file! 
#%%

    
def english_to_danish(sentence):
    
    inputs_en = EN_DA_tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    
    translation_ids_da = EN_DA_model.generate(**inputs_en)
    
    synonym_sentence = EN_DA_tokenizer.decode(translation_ids_da[0], skip_special_tokens=True)

    return synonym_sentence


from nlpaug.util import Action
import nlpaug.augmenter.word as naw
import random

def english_to_danish(sentence):
    inputs_en = EN_DA_tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    translation_ids_da = EN_DA_model.generate(**inputs_en)
    synonym_sentence = EN_DA_tokenizer.decode(translation_ids_da[0], skip_special_tokens=True)
    return synonym_sentence

def embedding_and_translate(dataset):
    df = pd.read_csv(dataset)
    rows = []
    for _, row in df.iterrows():
        sentence = row["english"]

        target = nltk.pos_tag(nltk.word_tokenize(sentence))

        adjective = [word for word, pos in target if pos.startswith('JJ')]
        verb = [word for word, pos in target if pos.startswith('VB')]

        if adjective:
            oneRandomAdjective = random.choice(adjective)
            synonym = WordNetAugmenter().augment(oneRandomAdjective)
            sentence = sentence.replace(oneRandomAdjective, synonym[0])
        elif verb:
            oneRandomVerb = random.choice(verb)
            synonym = WordNetAugmenter().augment(oneRandomVerb)
            sentence = sentence.replace(oneRandomVerb, synonym[0])
        
        danish_translation = english_to_danish(sentence)
        ukranian = row["ukranian"]
        rows.append((danish_translation, sentence, ukranian))
    
    new_df = pd.DataFrame(rows, columns=["danish", "english", "ukranian"])
    new_df.to_csv("interview_embedded_augmented.csv", index=False)

#embedding_and_translate("/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/data_augmentation/lol.csv")   
augmentation_BackTrans("/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/data_augmentation/lol.jsonl","2_3000_total_backtranslated_DE_DA.jsonl")


# %%
