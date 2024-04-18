import csv
import os
import re
import sys
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from utilities.constants import CHAR_FREQUENCY_TABLE_TITLE, CSV_FILE_DIR, GRAPH_FILE_DIR


def calculate_probabilities(freq_data: list):
    total_letters = 0
    for (_, frequency) in freq_data:
        total_letters += frequency

    # Calculate probabilities for each letter by dividing its frequency by total number of letters
    probabilities = {letter: (frequency / total_letters) for letter, frequency in freq_data}
    return probabilities


def __print_summary(prob_dict: dict, freq_data: list, title: str):
    """
    Prints the frequency and relative frequency (probability)
    of each character in a text file and presents them in a table.

    In addition, ensures the sum of all relative frequencies == 1.

    @param freq_data:
        A list containing the letter frequencies.

    @param title:
        A string representing the title of the text.

    @return: None
    """
    total_probability = 0

    # Instantiate Table and Define Title/Columns
    table = PrettyTable()
    table.title = CHAR_FREQUENCY_TABLE_TITLE.format(title)
    table.field_names = ['Character', 'Frequency', "Relative Frequency"]

    # Fill table with data
    for ((letter, frequency), probability) in zip(freq_data, prob_dict.values()):
        table.add_row((letter, frequency, round(probability, 5)))
        total_probability += probability

    print(table)
    print(f"Sum of Probabilities = {total_probability}")


def __save_results_to_csv(freq_data: list, file_path: str):
    """
    Saves the letter frequency data to a CSV file.

    @param freq_data:
        A list containing the letter frequencies

    @param file_path:
        A string representing the path to the text file.

    @return: None
    """
    if not os.path.exists(CSV_FILE_DIR):
        os.makedirs(CSV_FILE_DIR)

    # Create CSV save path that includes file_name.csv
    file_name = (file_path.split('/')[-1].split('.')[0]) + ".csv"
    save_directory = os.path.join(CSV_FILE_DIR, file_name)

    # Save results to CSV file
    try:
        with open(save_directory, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Letter', 'Count'])

            # Add the data in letter, count format
            for letter, count in freq_data:
                writer.writerow([letter, count])

        print("[+] CSV FILE CREATED: Results saved to the following path: {}".format(file_path))
    except IOError:
        sys.exit("[+] ERROR: An error has occurred while saving frequency results to CSV.")


def get_letter_frequency(file_path: str):
    """
    Count the frequency of each character in a text file.

    @param file_path:
        A string representing the path to the text file.

    @param title:
        A string representing the title of the text.

    @return letter_count:
        A sorted list of the frequency of each character in a text file.
    """
    with (open(file_path, 'r')) as file:
        letter_count = {}

        # Read and convert the entire file to lowercase
        text = file.read().lower()

        # Remove all non-alphabetic characters
        text = re.sub(r'[^a-z]', '', text)

        # Iterate and store into dictionary
        for char in text:
            if char in letter_count:
                letter_count[char] += 1
            else:
                letter_count[char] = 1

        # Sort the results (from the highest freq to lowest)
        results = sorted(letter_count.items(), key=lambda item: item[0])
        return results


def generate_prob_distribution_graph(prob_dict: dict, file_path: str, title: str):
    """
    Generates a graph of the frequency distribution of each character for a given text.

    @param prob_dict:
        A dictionary containing the relative frequencies/probabilities (value)
        for each letter (keys)

    @param file_path:
        A string representing the path to the text file.

    @param title:
        A string representing the title of the text.

    @return: None
    """
    if not os.path.exists(GRAPH_FILE_DIR):
        os.makedirs(GRAPH_FILE_DIR)

    # Define file name and extension
    file_name = (file_path.split('/')[-1].split('.')[0]) + "_distribution_graph.png"

    # Generate the graph
    plt.bar(prob_dict.keys(), prob_dict.values())
    plt.xlabel('Letters')
    plt.ylabel('Relative Frequency')
    plt.title('Relative Distribution of Letters in {}'.format(title))

    # Save graph
    plt.savefig(os.path.join(GRAPH_FILE_DIR, file_name))
    print("[+] GRAPH FILE CREATED: The following file has been created {}".format(file_name))


def perform_task_1(text_file_path: str, title: str):
    freq_data = get_letter_frequency(text_file_path)
    __save_results_to_csv(freq_data, text_file_path)

    probabilities = calculate_probabilities(freq_data)
    generate_prob_distribution_graph(probabilities, text_file_path, title)

    __print_summary(probabilities, freq_data, title)
