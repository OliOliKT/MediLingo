from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from textattack.augmentation import EmbeddingAugmenter, CharSwapAugmenter
import pandas as pd
import json

#SOURCE LANGUAGE
DA_EN_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-da-en")
DA_EN_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-da-en")

EN_DA_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-da")
EN_DA_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-da")

#TARGET LANGUAGE
UK_EN_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-uk-en")
UK_EN_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-uk-en")

EN_UK_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-uk")
EN_UK_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-uk")

EM_augmenter = EmbeddingAugmenter()
CS_augmenter = CharSwapAugmenter()

######### augmentation on the JSON file

def backtranslation_danish(sentence):

    inputs_da = DA_EN_tokenizer(sentence, return_tensors="pt")

    translation_ids_da = DA_EN_model.generate(**inputs_da)

    translated_sentence = DA_EN_tokenizer.decode(translation_ids_da[0], skip_special_tokens=True)
    
    #now back to danish
    
    inputs_en = EN_DA_tokenizer(translated_sentence, return_tensors="pt")
    
    translation_ids_da = EN_DA_model.generate(**inputs_en)
    
    backtranslated_sentence = EN_DA_tokenizer.decode(translation_ids_da[0], skip_special_tokens=True)

    return backtranslated_sentence

def backtranslation_ukrainian(sentence):
    
    inputs_UK = UK_EN_tokenizer(sentence, return_tensors="pt")

    translation_ids_UK = UK_EN_model.generate(**inputs_UK)

    translated_sentence = UK_EN_tokenizer.decode(translation_ids_UK[0], skip_special_tokens=True)
    
    #now back to ukranian
    
    inputs_en = EN_UK_tokenizer(translated_sentence, return_tensors="pt")
    
    translation_ids_en = EN_UK_model.generate(**inputs_en)
    
    backtranslated_sentence = EN_UK_tokenizer.decode(translation_ids_en[0], skip_special_tokens=True)

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
    
