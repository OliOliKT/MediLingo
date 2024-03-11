#%%
from textattack.augmentation import CharSwapAugmenter
from data_augmentation_utils import backtranslation_danish, backtranslation_ukrainian, embedding_and_translate
import json
import os

current_directory = os.path.dirname(__file__)
file_name = "../preprocess/dataset.jsonl"
file_path = os.path.join(current_directory,file_name)
file_path2 = os.path.join(current_directory,"../data_augmentation/BackTrans.jsonl")

#%%
#augmentation_BackTrans("fine_tuned_gpt/data_augmentation/dataset.jsonl", file_path2)

embedding_and_translate("input_dataset.csv")
# %%
