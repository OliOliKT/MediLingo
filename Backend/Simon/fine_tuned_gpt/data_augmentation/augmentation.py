import nlpaug.augmenter.word as naw
import json

def load_jsonlFile(path):
    lines = []
    with open(path, 'r', encoding="utf-8") as file:
        for line in file:
            lines.append(line)
    return lines

def write_jsonlFile(file ,path):
    with open(path,"w",encoding="utf-8") as file:
        for line in file:
            file.write(json.dumps(line,ensure_ascii=False) + "\n")

def augmentation_backtranslation(input_file, output_file):
    data_aug = naw.BackTranslationAug()
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

augmentation_backtranslation('dataset.jsonl', 'backtranslated.jsonl')