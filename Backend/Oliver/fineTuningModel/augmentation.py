from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from textattack.augmentation import EmbeddingAugmenter, CharSwapAugmenter, EasyDataAugmenter, CheckListAugmenter, WordNetAugmenter
import pandas as pd
import json
import random
import nltk
nltk.download('punkt')
nltk.download('stopwords')
import random


#BACKTRANSLATION - DANISH to GERMAN to DANISH
DA_DE_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-da-de")
DA_DE_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-da-de")
DE_DA_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-de-da")
DE_DA_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-de-da")

# Character Swap Augmenter
CS_augmenter = CharSwapAugmenter()

#EMBEDDING - ENGLISH to DANISH
EN_DA_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-da")
EN_DA_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-da")

# Easy Data Augmenter
EM_augmenter = CheckListAugmenter()

# Backtranslate from Danish to German to Danish
def backtranslation(sentence):
    inputs_da = DA_DE_tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    translation_ids_de = DA_DE_model.generate(**inputs_da)
    translated_sentence = DA_DE_tokenizer.decode(translation_ids_de[0], skip_special_tokens=True)

    inputs_de = DE_DA_tokenizer(translated_sentence, return_tensors="pt", padding=True, truncation=True)
    translation_ids_da = DE_DA_model.generate(**inputs_de)
    backtranslated_sentence = DE_DA_tokenizer.decode(translation_ids_da[0], skip_special_tokens=True)

    return backtranslated_sentence


# Load JSON file
def load_json_file(file_path):
    lines = []
    with open(file_path, 'r', encoding = "utf-8") as file:
        for line in file:
            lines.append(json.loads(line))
    return lines


# Write JSON file
def write_json_file(input_file_path, output_file_path):
    with open(output_file_path, "w+", encoding = "utf-8") as f:
        f.write(json.dumps(input_file_path, ensure_ascii = False) + "\n")


def backtranslate_augmenter(input_file, output_file):
    dataset = load_json_file(input_file)

    for obj in dataset:
        original_messages = obj["messages"]
        augmented_messages = []

        for message in original_messages:
            if message["role"] == "user":
                danish_text = message["content"]
                backtranslated_danish = backtranslation(danish_text)
                message["content"] = backtranslated_danish

            augmented_messages.append(message)

        augmented_obj = {"messages": augmented_messages}
        write_json_file(augmented_obj, output_file)


def char_swap_augmenter(input_file, output_file_path):
    dataset = load_json_file(input_file)
    augmented_messages = []

    for object in dataset:

        danish_text = object["messages"][1]["content"]
        object["messages"][1]["content"] = CS_augmenter.augment(danish_text)[0]

        ukrainian_text = object["messages"][2]["content"]
        object["messages"][2]["content"] = CS_augmenter.augment(ukrainian_text)[0]

        augmented_messages.append(object)
    
    with open(output_file_path, 'w') as f:
        for object in augmented_messages:
            f.write(json.dumps(object, ensure_ascii=False) + '\n')


def english_to_danish(sentence):
    
    inputs_en = EN_DA_tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    
    translation_ids_da = EN_DA_model.generate(**inputs_en)
    
    synonym_sentence = EN_DA_tokenizer.decode(translation_ids_da[0], skip_special_tokens=True)

    return synonym_sentence


def english_to_danish(sentence):
    inputs_en = EN_DA_tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    translation_ids_da = EN_DA_model.generate(**inputs_en)
    synonym_sentence = EN_DA_tokenizer.decode(translation_ids_da[0], skip_special_tokens=True)
    return synonym_sentence


def embed_and_translate(input, output):
    df = pd.read_csv(input)
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
    new_df.to_csv(output, index=False)