import pandas as pd
import os

def _load_data(file_path):
    return pd.read_csv(file_path)

def _analyze_question(data, question_id):
    return data[question_id].value_counts(normalize=True).sort_index()

def load_data_files(folder_path):
    files_list = []
    for filename in os.listdir(folder_path):
        filename = filename.split('.')[0]
        if filename:
            files_list.append(filename)
    files_list.sort()
    files = [os.path.join(folder_path, str(item)+".csv") for item in files_list]
    return files

def get_question_ids(question_file_path):
    question_ids = []
    with open(question_file_path, 'r') as file:
        for line in file:
            question = line.strip()
            question_ids.append(question)
    return question_ids