# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os
from helpers import _load_data, _analyze_question

# Analyze the question across datasets and find the frequency of each response for each question across each year
def _find_answer_frequency(question_id, datasets):
    frequency_distribution_dict = {}
    all_responses = set()
    for dataset in datasets:
        try:
            data = _load_data(dataset)
            distribution = _analyze_question(data, question_id)
            distribution.index = distribution.index.map(lambda x: int(float(x)) if x == x else 0)
            frequency_distribution_dict[os.path.basename(dataset).split('.')[0]] = distribution
            all_responses.update(distribution.index)
        except Exception as e:
            print(f"No question_id {question_id} was found for dataset {dataset}")
    return frequency_distribution_dict

# Use the frequencies and output in a table
def _create_frequency_distribution_table(frequency_distribution_dict):
    frequency_distribution_table = pd.DataFrame(frequency_distribution_dict)
    frequency_distribution_table.fillna(0, inplace=True)  # Fill missing values with 0
    frequency_distribution_table.index = frequency_distribution_table.index.astype(int)
    return frequency_distribution_table

# Calculate percent change in frequency of response for each question in consecutive years
def _create_percent_change_distribution_table(frequency_distribution_dict):
    percent_change_distribution_table = pd.DataFrame(frequency_distribution_dict).pct_change(axis='columns').iloc[:, 1:] * 100  
    percent_change_distribution_table = percent_change_distribution_table.round(2)  # Round to 2 decimal places
    return percent_change_distribution_table

# Plotting
def _plot_distribution(frequency_distribution_dict, question_id):
    plt.figure(figsize=(10, 8))
    
    # Sort the years to define the color order
    sorted_years = sorted(frequency_distribution_dict.keys())

    # Define a full spectrum rainbow color map
    rainbow_colors = ['red', 'orange', 'yellow', 'green', 'blue', 'violet']
    cmap = mcolors.LinearSegmentedColormap.from_list('CustomMap', rainbow_colors, N=16)
    
    all_responses = sorted(set().union(*[distribution.index for distribution in frequency_distribution_dict.values()]))
    response_positions = range(len(all_responses))
    response_mapping = {response: position for response, position in zip(all_responses, response_positions)}
    
    # Plot each distribution using mapped positions
    for i, year in enumerate(sorted_years):
        distribution = frequency_distribution_dict[year]
        even_spaced_positions = [response_mapping[response] for response in distribution.index]
        # Normalize i to the colormap based on the number of data points
        plt.scatter(even_spaced_positions, distribution.values, label=f"Dataset {year}",
                    color=cmap(i / (16 - 1)))
    
    # Set the axis labels and title
    plt.xticks(response_positions, all_responses)
    plt.xlabel('Response')
    plt.ylabel('Frequency')
    plt.title(f"Distribution of Responses for Question {question_id}")
    plt.legend()
    
    return plt.gcf()

def save_results(question_id, datasets):
    # Create a "results" directory if it doesn't exist for the specific question
    if not os.path.exists("results"):
        os.makedirs("results")

    results_path = os.path.join("results", question_id)
    if not os.path.exists(results_path):
        os.makedirs(results_path)
    
    # Create frequency distribution dict
    frequency_distribution_dict = _find_answer_frequency(question_id, datasets)
    print(frequency_distribution_dict)

    # Create frequency distribution table and save
    frequency_distribution_table = _create_frequency_distribution_table(frequency_distribution_dict)
    print(f"Frequency distribution for question {question_id}")
    print(frequency_distribution_table)
    frequency_distribution_table.to_csv(f"{results_path}/{question_id}_response_frequency.csv")

    # Create percent change table and save
    percent_change_distribution_table = _create_percent_change_distribution_table(frequency_distribution_dict)
    print(f"Percent change between years per response for {question_id}")
    print(percent_change_distribution_table)
    percent_change_distribution_table.to_csv(f"{results_path}/{question_id}_percent_change.csv")

    plot = _plot_distribution(frequency_distribution_dict, question_id)
    plot.savefig(f"{results_path}/{question_id}.png")
    plt.close(plot)