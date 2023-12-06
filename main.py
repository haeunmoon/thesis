# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_data(file_path):
    """Load the dataset from a CSV file."""
    return pd.read_csv(file_path)

def analyze_question(data, question_id):
    """Analyze the responses for a given question."""
    return data[question_id].value_counts(normalize=True).sort_index()

# Paths to your datasets
datasets = ['thesis_data/2022.csv', 'thesis_data/2021.csv', 'thesis_data/2020.csv']
# question_id = '문1'  # Replace with the actual question ID
question_id = 'uni14'

# Analyze the question across datasets
distributions = []
all_responses = set()
for dataset in datasets:
    data = load_data(dataset)
    distribution = analyze_question(data, question_id)
    distributions.append(distribution)
    all_responses.update(distribution.index)

# Plotting
plt.figure(figsize=(10, 6))
for i, distribution in enumerate(distributions):
    plt.scatter(distribution.index, distribution.values, label=f'Dataset {i+1}')

# Set x-axis to only show integer ticks
plt.xticks(range(int(min(all_responses)), int(max(all_responses)) + 1))

plt.xlabel('Response')
plt.ylabel('Frequency')
plt.title(f'Distribution of Responses for Question {question_id}')
plt.legend()
plt.show()

