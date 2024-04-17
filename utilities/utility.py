import re
from prettytable import PrettyTable
from utilities.constants import CHAR_FREQUENCY_TABLE_TITLE


def print_letter_frequency_table(freq_data: list, title: str):
    """
    Prints the frequency of each character in a text file
    and presents them in a table.

    @param freq_data:
        A list containing the letter frequencies.

    @param title:
        A string representing the title of the text.

    @return: None
    """
    table = PrettyTable()
    table.title = CHAR_FREQUENCY_TABLE_TITLE.format(title)
    table.field_names = ['Character', 'Frequency']

    for (letter, frequency) in freq_data:
        table.add_row((letter, frequency))

    print(table)


def char_frequency_count(text_file_path: str, title: str):
    """
    Count the frequency of each character in a text file.

    @param text_file_path:
        A string representing the path to the text file.

    @param title:
        A string representing the title of the text.

    @return letter_count:
        A sorted list of the frequency of each character in a text file.
    """
    with (open(text_file_path, 'r')) as file:
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
        results = sorted(letter_count.items(), key=lambda item: item[1], reverse=True)

        # Print results in a table
        print_letter_frequency_table(results, title)
        return results[0]


if __name__ == '__main__':
    freq = char_frequency_count("../data/moby_dick.txt", "Moby Dick")
