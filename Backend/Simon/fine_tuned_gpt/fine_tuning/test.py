import json

def switch_content(data):
    switched_data = {
        "messages": []
    }
    user_message = None
    assistant_message = None
    system_message = None
    
    for messages in data['messages']:
        if messages['role'] == 'system':
            system_message = {"role": "system", "content": "Translating from Ukrainian to Danish for medical purposes"}
        elif messages['role'] == 'user':
            user_message = {"role": "assistant", "content": messages['content']}
        elif messages['role'] == 'assistant':
            assistant_message = {"role": "user", "content": messages['content']}
        else:
            switched_data["messages"].append(messages)
    
    # Append user messages before the assistant messages
    switched_data["messages"].append(system_message)
    switched_data["messages"].append(assistant_message)
    switched_data["messages"].append(user_message)

    return switched_data

# Example dataset
data = {
    "messages": [
        {"role": "system", "content": "Translating from Danish to Ukrainian for medical purposes"},
        {"role": "user", "content": "Du vil føle en prikkende fornemmelse, når vævsprøven bliver taget fra din lever."},
        {"role": "assistant", "content": "Ви відчуєте пощипування, коли ми будемо брати зразок тканини з вашої печінки."}
    ]
}

input_file = '/Users/simono/Desktop/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/datasets/interviewAndQuestions_test_100p.jsonl'
output_file = '/Users/simono/Desktop/MediLingo/Backend/Simon/fine_tuned_gpt/fine_tuning/datasets/new_interviewAndQuestions_test_100p.jsonl'

# Open input JSONL file
with open(input_file, 'r') as f:
    # Open output JSONL file
    with open(output_file, 'w') as fout:
        # Process each line (JSON object) in the input file
        for line in f:
            # Load JSON object from the line
            data = json.loads(line)
            # Process the data
            switched_data = switch_content(data)
            # Write the processed data to the output file
            json.dump(switched_data, fout, ensure_ascii=False)
            fout.write('\n')  # Write newline to separate JSON objects in the JSONL file
