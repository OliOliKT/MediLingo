#%%
from textattack.augmentation import CharSwapAugmenter
from data_augmentation_utils import backtranslation_danish, backtranslation_ukrainian, embedding_and_translate
import json
import os

current_directory = os.path.dirname(__file__)
file_name = "../preprocess/dataset.jsonl"
file_path = os.path.join(current_directory,file_name)
file_path2 = os.path.join(current_directory,"../data_augmentation/BackTrans.jsonl")

def load_jsonlFile(path):
    lines = []
    with open(path, 'r', encoding="utf-8") as file:
        for line in file:
            lines.append(json.loads(line))
    return lines

def write_jsonlFile(file ,path):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(file, ensure_ascii=False) + '\n')
#%%
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
            elif message["role"] == "assistant":
                ukrainian_text = message["content"]
                backtranslated_ukrainian = backtranslation_ukrainian(ukrainian_text)
                message["content"] = backtranslated_ukrainian

            augmented_messages.append(message)

        augmented_obj = {"messages": augmented_messages}
        write_jsonlFile(augmented_obj, output_file)

#%%
#augmentation_BackTrans("fine_tuned_gpt/data_augmentation/dataset.jsonl", file_path2)

embedding_and_translate("input_dataset.csv")
# %%
