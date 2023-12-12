# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from helpers import _load_data, _analyze_question, _load_data_files
#test

DATASETS = _load_data_files("thesis_data")

# Analyze the question across datasets and find the frequency of each response for each question across each year
def find_answer_frequency(question_id, datasets=DATASETS):
    frequency_distribution_dict = {}
    all_responses = set()
    for dataset in datasets:
        try:
            data = _load_data(dataset)
            distribution = _analyze_question(data, question_id)
            print(distribution)
            frequency_distribution_dict[os.path.basename(dataset).split('.')[0]] = distribution
            all_responses.update(distribution.index)
        except Exception as e:
            print(f"No question_id {question_id} was found for dataset {dataset}")
    return frequency_distribution_dict

# Use the frequencies and output in a table
def create_frequency_distribution_table(frequency_distribution_dict):
    frequency_distribution_table = pd.DataFrame(frequency_distribution_dict)
    frequency_distribution_table.fillna(0, inplace=True)  # Fill missing values with 0
    frequency_distribution_table.index = frequency_distribution_table.index.astype(int)
    return frequency_distribution_table

# Calculate percent change in frequency of response for each question in consecutive years
def create_percent_change_distribution_table(frequency_distribution_dict):
    percent_change_distribution_table = pd.DataFrame(frequency_distribution_dict).pct_change(axis='columns').iloc[:, 1:] * 100  
    percent_change_distribution_table = percent_change_distribution_table.round(2)  # Round to 2 decimal places
    return percent_change_distribution_table

# Plotting
def plot_distribution(frequency_distribution_dict):
    plt.figure(figsize=(10, 6))
    for year, distribution in frequency_distribution_dict.items():
        plt.scatter(distribution.index, distribution.values, label=f"Dataset {year}")

    # Set x-axis to only show integer ticks
    all_responses = set()
    for distribution in frequency_distribution_dict.values():
        all_responses.update(distribution.index)
    plt.xticks(range(int(min(all_responses)), int(max(all_responses)) + 1))

    plt.xlabel('Response')
    plt.ylabel('Frequency')
    plt.title('Distribution of Responses for Question')
    plt.legend()
    plt.show()


def save_results(question_id):
    # Create a "results" directory if it doesn't exist for the specific question
    if not os.path.exists("results"):
        os.makedirs("results")

    results_path = os.path.join("results", question_id)
    if not os.path.exists(results_path):
        os.makedirs(results_path)
    
    # Create frequency distribution dict
    frequency_distribution_dict = find_answer_frequency(question_id)
    print(frequency_distribution_dict)

    # Create frequency distribution table and save
    frequency_distribution_table = create_frequency_distribution_table(frequency_distribution_dict)
    print(f"Frequency distribution for question {question_id}")
    print(frequency_distribution_table)
    frequency_distribution_table.to_csv(f"{results_path}/{question_id}_response_frequency.csv")

    # Create percent change table and save
    percent_change_distribution_table = create_percent_change_distribution_table(frequency_distribution_dict)
    print(f"Percent change between years per response for {question_id}")
    print(percent_change_distribution_table)
    percent_change_distribution_table.to_csv(f"{results_path}/{question_id}_percent_change.csv")

    # Plotting and save the plot
    plt.figure(figsize=(10, 6))
    for year, distribution in frequency_distribution_dict.items():
        plt.scatter(distribution.index, distribution.values, label=f"Dataset {year}")

    # Set x-axis to only show integer ticks
    all_responses = set()
    for distribution in frequency_distribution_dict.values():
        all_responses.update(distribution.index)
    plt.xticks(range(int(min(all_responses)), int(max(all_responses)) + 1))

    plt.xlabel('Response')
    plt.ylabel('Frequency')
    plt.title('Distribution of Responses for Question')
    plt.legend()
    plt.savefig(f"{results_path}/{question_id}.png")

def run():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py [question_id]")
        sys.exit(1)
    
    question_id = sys.argv[1]
    print(question_id)
    save_results(question_id=question_id)

if __name__ == "__main__":
    # python3 main.py [question_id]
    run()

