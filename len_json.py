import json


file_path = 'cleaned_data.json'

def count_words_in_json(file_path):
    
    with open(file_path, 'r',encoding='utf-8') as file:
        data = json.load(file)
    
    
    total_word_count = 0
    
    
    for key, value in data.items():
        
        words = value.split()
        
        total_word_count += len(words)
    
  
    return total_word_count


total_words = count_words_in_json(file_path)
print(f'Total number of words in the JSON values: {total_words}')
