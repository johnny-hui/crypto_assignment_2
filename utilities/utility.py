import csv
import os
import re
import string
import sys
from fractions import Fraction
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from models.caesar import Enc_Dec
from utilities.constants import CHAR_FREQUENCY_TABLE_TITLE, CSV_FILE_DIR, GRAPH_FILE_DIR, TOP_SIX_FREQ_USED_LETTERS, \
    CONDITIONAL_PROBABILITY_TABLE_TITLE


def __check_task_1_complete():
    """
    Checks if task 1 (pre-requisite) was performed
    prior to executing task 2.

    @return: None
    """
    if os.path.exists(CSV_FILE_DIR):
        files = os.listdir(CSV_FILE_DIR)

        for file in files:
            if file.endswith('.csv'):
                return None

        sys.exit("[+] ERROR: Task 1 was not performed prior to performing this task!")
    else:
        sys.exit("[+] ERROR: Task 1 was not performed prior to performing this task!")


def calculate_relative_probabilities(freq_data: dict):
    """
    Calculates the frequency of each letter relative
    to the total number of words in the document.

    @param freq_data:
        A dictionary containing the frequencies for each letter

    @return probabilities:
        A dictionary of key/value pairs (letter:frequency)
    """
    total_letters = 0
    for (_, frequency) in freq_data.items():
        total_letters += frequency

    # Calculate probabilities for each letter by dividing its frequency by total number of letters
    probabilities = {letter: (frequency / total_letters) for letter, frequency in freq_data.items()}
    return probabilities


def __print_summary(prob_dict: dict, freq_data: dict = None,
                    title: str = None, task: int = 1, offset: int = 0):
    """
    Prints the frequency and relative frequency (probability)
    of each character in a text file and presents them in a table.

    In addition, ensures the sum of all relative frequencies == 1.

    @param freq_data:
        A dictionary containing the letter frequencies.

    @param title:
        A string representing the title of the text.

    @param task:
        An optional argument that if specified
        prints the summary for Task 2 (default value = 1)

    @param offset:
        An optional argument which is specifically
        used for Task 2 (default value = 0)

    @return: None
    """
    # Instantiate Table
    table = PrettyTable()

    if task != 1:
        # Define Title/Columns
        table.title = CONDITIONAL_PROBABILITY_TABLE_TITLE.format(title)
        table.field_names = ['Frequently Used Letter', 'Cipher Letter', "Probability", "Key (Offset)"]

        # Fill table with data
        for letter, (cipher_letter, probability) in prob_dict.items():
            table.add_row([letter, cipher_letter, probability, offset])

        print("=" * 80)
        print(table)
    else:
        total_probability = 0
        table.title = CHAR_FREQUENCY_TABLE_TITLE.format(title)
        table.field_names = ['Character', 'Frequency', "Relative Frequency"]

        for ((letter, frequency), probability) in zip(freq_data.items(), prob_dict.values()):
            table.add_row((letter, frequency, round(probability, 5)))
            total_probability += probability

        print(table)
        print(f"[+] Sum of Probabilities = {total_probability}")


def load_data_from_csv(file_path: str):
    """
    Loads data from CSV file and returns it as a dictionary.

    @param file_path:
        A string representing the path to the CSV file.

    @return freq_data:
        A dictionary containing the frequencies for each letter
    """
    freq_data = {}

    # PROTOCOL: Get CSV file path from the file path in parameter
    file_name = (file_path.split('/')[-1].split('.')[0]) + ".csv"

    # Load CSV file and store data in freq_data
    try:
        with open(os.path.join(CSV_FILE_DIR, file_name), 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip the header row if it exists
            for row in csv_reader:
                letter, count = row
                freq_data[letter] = int(count)
    except FileNotFoundError:
        sys.exit("[+] ERROR: The corresponding CSV file was not found; please perform Task 1 again.")

    return freq_data


def __save_results_to_csv(freq_data: dict, file_path: str):
    """
    Saves the letter frequency data to a CSV file.

    @param freq_data:
        A dictionary containing the letter frequencies

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
            for letter, count in freq_data.items():
                writer.writerow([letter, count])

        print("[+] CSV FILE CREATED: Results saved to the following path: {}".format(file_path))
    except IOError:
        sys.exit("[+] ERROR: An error has occurred while saving frequency results to CSV.")


def get_letter_frequency(file_path: str, message: str = None, task: int = 1):
    """
    Count the frequency of each character in a text file.

    @param file_path:
        A string representing the path to the text file.

    @param message:
        An optional argument that when provided takes in
        and reads the encrypted message

    @param task:
        An optional argument that when provided performs
        get letter frequency for task 2 (default value = 1)

    @return letter_count:
        A sorted dictionary of the frequency of each character in a text file
    """
    letter_count = {}

    # Perform letter frequency for task 2
    if task != 1:
        for char in message:
            if char in letter_count:
                letter_count[char] += 1
            else:
                letter_count[char] = 1
        results = dict(sorted(letter_count.items(), key=lambda item: item[0]))
        return results

    with (open(file_path, 'r')) as file:
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
        results = dict(sorted(letter_count.items(), key=lambda item: item[0]))
        return results


def generate_prob_distribution_graph(prob_dict: dict, file_path: str,
                                     title: str, task: int = 1):
    """
    Generates a graph of the frequency distribution of
    each character for a given text.

    @param prob_dict:
        A dictionary containing the relative frequencies/probabilities (value)
        for each letter (keys)

    @param file_path:
        A string representing the path to the text file.

    @param title:
        A string representing the title of the text.

    @param task:
        An optional argument that when provided for task 2,
        produces a probability distribution graph for the
        encrypted ciphertext (default value = 1)

    @return: None
    """
    if not os.path.exists(GRAPH_FILE_DIR):
        os.makedirs(GRAPH_FILE_DIR)

    # Define file name, extension, and graph title
    if task != 1:
        file_name = (file_path.split('/')[-1].split('.')[0]) + "_encrypted_distribution_graph.png"
        plt.title('Relative Distribution of Letters in {} (Encrypted)'.format(title))
    else:
        file_name = (file_path.split('/')[-1].split('.')[0]) + "_distribution_graph.png"
        plt.title('Relative Distribution of Letters in {}'.format(title))

    # Generate the graph
    plt.bar(prob_dict.keys(), prob_dict.values())
    plt.xlabel('Letters')
    plt.ylabel('Relative Frequency')

    # Save graph
    plt.savefig(os.path.join(GRAPH_FILE_DIR, file_name))
    print("[+] GRAPH FILE CREATED: The following file has been created {}".format(file_name))


def calculate_conditional_probabilities(file_path: str, cipher_freq_data: dict):
    """
    Calculates the conditional probabilities for each of the
    top 6 frequently used English letters given the set of all
    ciphertext letters.

    @attention: Equation Used
        𝑃(𝑀 = 𝑚|𝐶 = 𝑐) = 𝑃(𝐶 = 𝑐|𝑀 = 𝑚) ∙ 𝑃(𝑀 = 𝑚) / 𝑃(𝐶 = 𝑐); where
        𝑷(𝑪 = 𝒄|𝑴 = 𝒎) = ∑{𝒌:𝒎=𝒅𝒌(𝒄)} 𝑷(𝑲 = 𝒌)

    @param file_path:
        A string representing the path to the text file.

    @param cipher_freq_data:
        A dictionary containing key/value pairs of
        cipher letters and their frequencies

    @return conditional_prob_dict:
        A dictionary containing ciphertext letters that correspond
        to one of the top six frequently used English letters with
        a probability of 1 (or 100%)
    """
    # Initialize Variables
    conditional_prob_dict = {}
    plain_text_char = 'e'
    summation = 0

    # Load plaintext letter frequency data from CSV
    plain_text_freq_data = load_data_from_csv(file_path)

    # Find the sum over all keys (offsets), where decrypted cipher char == plain text char
    print("=" * 80)
    print("[+] Now calculating: 𝑷(𝑪 = 𝒄|𝑴 = 'e') = ∑{𝒌:'e'=𝒅𝒌(𝒄)} 𝑷(𝑲 = 𝒌)")
    for offset in range(0, 26):
        for letter in list(string.ascii_lowercase):
            if Enc_Dec(letter, key=offset, mode='decrypt') == plain_text_char:
                summation += Fraction(1, 26)
                print(f"Offset: {offset} | Letter: {letter} -> {summation}")
    print(f"Result: 𝑷(𝑪 = 𝒄|𝑴 = 𝒎) = {summation}")

    # Find conditional probabilities of top 6 frequently used English letters
    for letter in TOP_SIX_FREQ_USED_LETTERS:
        print("=" * 80)
        print(f"[+] Now calculating: 𝑃(𝑀 = {letter}|𝐶 = 𝑐) = {summation} ∙ 𝑃(𝑀 = {letter}) / 𝑃(𝐶 = 𝑐)")

        for char in list(string.ascii_lowercase):  # => Set of all possible characters in ciphertext
            conditional_probability = (summation * plain_text_freq_data.get(letter)) / cipher_freq_data.get(char)
            print(f"𝑃(𝑀 = {letter}|𝐶 = {char}): {conditional_probability}")

            # Store results with 100% probability to dictionary
            if conditional_probability == 1:
                conditional_prob_dict[letter] = (char, conditional_probability)

    return conditional_prob_dict


def perform_task_1(text_file_path: str, title: str):
    """
    Performs task 1.

    @param text_file_path:
        A string representing the path to the text file.

    @param title:
        A string representing the title of the text

    @return: None
    """
    print(f"[+] Task 1 - Getting Letter Frequency Data for {title}")
    freq_data = get_letter_frequency(text_file_path)
    __save_results_to_csv(freq_data, text_file_path)

    probabilities = calculate_relative_probabilities(freq_data)
    generate_prob_distribution_graph(probabilities, text_file_path, title)

    __print_summary(probabilities, freq_data, title, task=1)


def perform_task_2(text_file_path: str, title: str, offset: int):
    """
    Performs Task 2 (calculating conditional probabilities).

    @param text_file_path:
        A string representing the path to the text file.

    @param title:
        A string representing the title of the text

    @param offset:
        An integer offset for Caesar's Cipher.

    @return: None
    """
    print(f"[+] Task 2 - Calculating the Conditional Probabilities for Top 6 Frequent Letters "
          f"Given Cipher Letters in {title}")

    if offset is None:
        sys.exit("[+] ERROR: An offset is required for Task 2 which was not provided (-o option)!")

    # Checks if Task 1 completed
    __check_task_1_complete()

    # Perform Task 2
    with (open(text_file_path, 'r')) as file:
        text = file.read().lower()
        text = re.sub(r'[^a-z]', '', text)

        ciphertext = Enc_Dec(text, offset, mode='encrypt')
        cipher_freq_data = get_letter_frequency(text_file_path, message=ciphertext, task=2)

        probabilities = calculate_relative_probabilities(cipher_freq_data)
        generate_prob_distribution_graph(probabilities, text_file_path, title, task=2)

        results = calculate_conditional_probabilities(text_file_path, cipher_freq_data)
        __print_summary(results, title=title, task=2, offset=offset)
