
# from textattack.augmentation import EmbeddingAugmenter
# from textattack.augmentation import WordNetAugmenter
from textattack.augmentation import CharSwapAugmenter
import json
import os

current_directory = os.path.dirname(__file__)
file_name = "../preprocess/dataset.jsonl"
file_path = os.path.join(current_directory,file_name)
file_path2 = os.path.join(current_directory,"../data_augmentation/CharSwapAug.jsonl")

def load_jsonlFile(path):
    lines = []
    with open(path, 'r', encoding="utf-8") as file:
        for line in file:
            lines.append(json.loads(line))
    return lines

def write_jsonlFile(file ,path):
    with open(path,"w+",encoding="utf-8") as f:
        f.write(json.dumps(file,ensure_ascii=False) + "\n")

aug = CharSwapAugmenter()

def augmentation_CharSwap(input_file, output_file):
    data_aug = CharSwapAugmenter()
    dataset = load_jsonlFile(input_file)

    for obj in dataset:
        original_messages = obj["messages"]
        augmented_messages = []

        for message in original_messages:
            if message["role"] == "user":
                danish_text = message["content"]
                backtranslated_danish = data_aug.augment(danish_text)
                message["content"] = backtranslated_danish
            elif message["role"] == "assistant":
                ukrainian_text = message["content"]
                backtranslated_ukrainian = data_aug.augment(ukrainian_text)
                message["content"] = backtranslated_ukrainian

            augmented_messages.append(message)

        augmented_obj = {"messages": augmented_messages}
        write_jsonlFile(augmented_obj, output_file)

augmentation_CharSwap(file_path, file_path2)

# embed_aug = EmbeddingAugmenter()

# def augmentation_CharSwap(input_file, output_file):
#     data_aug = CharSwapAugmenter()
#     dataset = load_jsonlFile(input_file)

#     for obj in dataset:
#         original_messages = obj["messages"]
#         augmented_messages = []

#         for message in original_messages:
#             if message["role"] == "user":
#                 danish_text = message["content"]
#                 backtranslated_danish = data_aug.augment(danish_text)
#                 message["content"] = backtranslated_danish
#             elif message["role"] == "assistant":
#                 ukrainian_text = message["content"]
#                 backtranslated_ukrainian = data_aug.augment(ukrainian_text)
#                 message["content"] = backtranslated_ukrainian

#             augmented_messages.append(message)

#         augmented_obj = {"messages": augmented_messages}
#         write_jsonlFile(augmented_obj, output_file)

# augmentation_CharSwap('/preprocess/dataset.jsonl', '/data_augmentation/CharSwapAug.jsonl')






