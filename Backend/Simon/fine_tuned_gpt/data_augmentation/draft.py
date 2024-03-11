from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from textattack.augmentation import EmbeddingAugmenter, EasyDataAugmenter, BackTranslationAugmenter
import pandas as pd

#SOURCE LANGUAGE
EN_DA_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-da")
EN_DA_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-da")

EMB_augmenter = EmbeddingAugmenter()
ED_augmenter = EasyDataAugmenter()
BT_augmenter = BackTranslationAugmenter()

######### augmentation on the JSON file

def backtranslationToDanish(sentence):
    
    inputs_en = EN_DA_tokenizer(sentence, return_tensors="pt",padding=True, truncation=True)
    
    translation_ids_da = EN_DA_model.generate(**inputs_en)
    
    backtranslated_sentence = EN_DA_tokenizer.decode(translation_ids_da[0], skip_special_tokens=True)

    return backtranslated_sentence

######### augmentation on csv file! 
def embedding_replacement(sentence):
    augmented_sentences = EMB_augmenter.augment(sentence)
    return augmented_sentences

def easydata_replacement(sentence):
    augmented_sentences = ED_augmenter.augment(sentence)
    return augmented_sentences

def backtranslation_replacement(sentence):
    augmented_sentences = BT_augmenter.augment(sentence)
    return augmented_sentences

def embedding_and_translate(dataset):
    df = pd.read_csv(dataset)
    rows = []
    for _, row in df.iterrows():
        embedded = embedding_replacement(row["english"])
        danish_translation = backtranslationToDanish(embedded)
        ukranian= row["ukranian"]
        rows.append((danish_translation, embedded[0], ukranian))
    
    new_df = pd.DataFrame(rows, columns=["danish", "english", "ukrainian"])

    new_df.to_csv("EmbeddedAugmented.csv",index=False)
    
def easydata_and_translate(dataset):
    df = pd.read_csv(dataset)
    rows = []
    for _, row in df.iterrows():
        embedded = easydata_replacement(row["english"])
        danish_translation = backtranslationToDanish(embedded)
        ukranian= row["ukranian"]
        rows.append((danish_translation, embedded[0], ukranian))
    
    new_df = pd.DataFrame(rows, columns=["danish", "english", "ukrainian"])

    new_df.to_csv("EasyDataaugmented.csv",index=False)

def backtranslate_and_translate(dataset):
    df = pd.read_csv(dataset)
    rows = []
    for _, row in df.iterrows():
        embedded = backtranslation_replacement(row["english"])
        danish_translation = backtranslationToDanish(embedded)
        ukranian= row["ukranian"]
        rows.append((danish_translation, embedded[0], ukranian))
    
    new_df = pd.DataFrame(rows, columns=["danish", "english", "ukrainian"])

    new_df.to_csv("BackTranslated.csv",index=False)

backtranslate_and_translate("/Users/simono/Desktop/Thesis/Branches/MediLingo/Backend/Simon/fine_tuned_gpt/data_augmentation/test.csv")
