from textattack.augmentation import CharSwapAugmenter
import json
import os

current_directory = os.path.dirname(__file__)
json_file_path = os.path.join(current_directory, "dataset.jsonl")
augmented_dataset_file_path = os.path.join(current_directory, 'augmentedDataset.jsonl')

def load_json_file(file_path):
    lines = []
    with open(file_path, 'r', encoding = "utf-8") as file:
        for line in file:
            lines.append(json.loads(line))
    return lines


def write_json_file(input_file_path, output_file_path):
    with open(output_file_path, "w+", encoding = "utf-8") as f:
        f.write(json.dumps(input_file_path, ensure_ascii = False) + "\n")


def augmenter(input_file, output_file_path):
    data_aug = CharSwapAugmenter()
    dataset = load_json_file(input_file)
    augmented_messages = []

    for object in dataset:

        danish_text = object["messages"][1]["content"]
        object["messages"][1]["content"] = data_aug.augment(danish_text)[0]

        ukrainian_text = object["messages"][2]["content"]
        object["messages"][2]["content"] = data_aug.augment(ukrainian_text)[0]

        augmented_messages.append(object)
    
    with open(output_file_path, 'w') as f:
        for object in augmented_messages:
            f.write(json.dumps(object, ensure_ascii=False) + '\n')


augmenter(json_file_path, augmented_dataset_file_path)