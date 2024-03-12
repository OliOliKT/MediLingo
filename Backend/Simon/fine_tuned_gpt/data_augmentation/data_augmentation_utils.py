from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from textattack.augmentation import EmbeddingAugmenter, CharSwapAugmenter
import pandas as pd
import json

#BACKTRANSLATION - DANISH to GERMAN toDANISH
DA_DE_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-da-de")
DA_DE_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-da-de")

DE_DA_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-de-da")
DE_DA_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-de-da")

#CharSwap
CS_augmenter = CharSwapAugmenter()

#EMBEDDING - ENGLISH to DANISH

EN_DA_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-da")
EN_DA_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-da")
EM_augmenter = EmbeddingAugmenter()

######### augmentation on the JSON file

def backtranslation_danish(sentence):

    #danish to german 
    
    inputs_da = DA_DE_tokenizer(sentence, return_tensors="pt")

    translation_ids_da = DA_DE_model.generate(**inputs_da)

    translated_sentence = DA_DE_tokenizer.decode(translation_ids_da[0], skip_special_tokens=True)
    
    #now back from german to danish
    
    inputs_en = DE_DA_tokenizer(translated_sentence, return_tensors="pt")
    
    translation_ids_da = DE_DA_model.generate(**inputs_en)
    
    backtranslated_sentence = DE_DA_tokenizer.decode(translation_ids_da[0], skip_special_tokens=True)

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

def english_to_danish(sentence):
    
    
    inputs_en = EN_DA_tokenizer(sentence, return_tensors="pt")
    
    translation_ids_da = EN_DA_model.generate(**inputs_en)
    
    synonym_sentence = EN_DA_tokenizer.decode(translation_ids_da[0], skip_special_tokens=True)

    return synonym_sentence

def embedding_and_translate(dataset):
    df = pd.read_csv(dataset)
    rows = []
    for _, row in df.iterrows():
        embedded = EM_augmenter.augment(row["english"])
        danish_translation = english_to_danish(embedded)
        ukranian= row["ukranian"]
        rows.append((danish_translation, embedded[0], ukranian))
    
    new_df = pd.DataFrame(rows, columns=["danish", "english", "ukrainian"])

    new_df.to_csv("augmented.csv",index=False)
    
