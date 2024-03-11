from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from textattack.augmentation import EmbeddingAugmenter
import pandas as pd

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

augmenter = EmbeddingAugmenter()


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

######### augmentation on csv file! 
def embedding_replacement(sentence):
    augmented_sentences = augmenter.augment(sentence)
    return augmented_sentences

def english_to_danish(sentence):
    
    inputs_en = EN_DA_tokenizer(sentence, return_tensors="pt")
    
    translation_ids_da = EN_DA_model.generate(**inputs_en)
    
    synonym_sentence = EN_DA_tokenizer.decode(translation_ids_da[0], skip_special_tokens=True)

    return synonym_sentence

def embedding_and_translate(dataset):
    df = pd.read_csv(dataset)
    rows = []
    for _, row in df.iterrows():
        embedded = embedding_replacement(row["english"])
        danish_translation = english_to_danish(embedded)
        ukranian= row["ukranian"]
        rows.append((danish_translation, embedded[0], ukranian))
    
    new_df = pd.DataFrame(rows, columns=["danish", "english", "ukrainian"])

    new_df.to_csv("augmented.csv",index=False)


