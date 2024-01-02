# -*- coding: utf-8 -*-
import click
from analyze import save_results
from helpers import load_data_files, get_question_ids

DATASETS = load_data_files("thesis_data")
QUESTION_IDS = get_question_ids("question_ids.txt")

@click.command()
@click.option('--question', default=None, help='Individual question ID to get results for')

def run(question):
    if question:
        save_results(question_id=question, datasets=DATASETS)
    else:
        for question in QUESTION_IDS:
            save_results(question_id=question, datasets=DATASETS)

if __name__ == "__main__":
    run()

