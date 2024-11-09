# Descriptions:
"""
Task_8
Expand previous Homework 5/6/7 with additional class, which allow to provide records by JSON file:
1.Define your input format (one or many records)
2.Default folder or user provided file path
3.Remove file if it was successfully processed
******************************************************************************************
File structure description:
txt: each line contains separate publication text and has a structured format like: "News # Text # City #"
json: each element contains one-line publication text

Example of the input file structure:
txt:
News # this is An example OF a neWS tExt that spans muLtiple lines and shOuld BE processed correctly. # auSTin #
Private_Ad # I'm selling a slightly used bike in great condition. Contact me for more details!  # 2024/12/01 #
Joke # why don't skeLEtons fight each other? becauSE they DOn't have THE guts! # huMor #
News # global TeMperatures hit a reCord high, sparKing concerns among scientists. # Climate Hub #
Private_ad # Limited time offEr! geT a branD-new coffee maker at a discountEd price. # 2024/12/05 #
Joke # why did the GolFer brIng an extra pair of sOcks? In case he got a Hole-in-one! # GolfHumor #

json:
[
    {
        "type": "News",
        "text": "new teChnological breaKthrough.",
        "city": "Tech City"
    },
    {
        "type": "Private_ad",
        "text": "Selling: a brAnd-new laPTop.",
        "expiration_date": "2024/11/15"
    },
    {
        "type": "Joke",
        "text": "Why did the comPuter go to the doctor? It had a virus!",
        "hashtag": "FunnyJoke"
    }
]

xml:
<Publications>
    <Publication>
        <Type>News</Type>
        <Text>new teChnological breaKthrough.</Text>
        <City>Tech City</City>
    </Publication>
    <Publication>
        <Type>Private_ad</Type>
        <Text>Selling a brAnd-new laPTop..</Text>
        <Expiration_date>2024/11/15</Expiration_date>
    </Publication>
    <Publication>
        <Type>Joke</Type>
        <Text>Why did the coMPuter GO To the doctor? it haD a virus!</Text>
        <Hashtag>FunnyJoke</Hashtag>
    </Publication>
</Publications>
******************************************************************************************
HW: All publications will be saved in the publications.txt file that is stored in the root folder.
    If the file doesn't exist, it will be created automatically.

    When entering text from the console, '###' symbols on the new line is used as the 'end of input' indicator.

"""

import os
import random
import sys
import csv
from collections import Counter
import re
from datetime import datetime, timedelta
from strings_func_4 import capitalize_sentences
import json
import xml.etree.ElementTree as ElementTree


class Publication(object):
    """Base class for different types of publications."""

    def __init__(self, title: str, text: str):
        self.title = title
        self.text = text
        self.max_length: int = 50
        self.info_line = ''

    def format_publication(self) -> str:
        """Returns the formatted string of the publication to be saved to the file."""
        self.text = self.split_text(self.text if self.text else 'Here should be your text')
        formatted_title = f"{self.title} {'-' * (self.max_length - len(self.title))}"
        return f"{formatted_title}\n{self.text}\n"

    def split_text(self, line: str) -> str:
        # Split into lines with max_length, keeping whole words intact
        formatted_text = []

        words = line.strip().split()  # Split each line into words
        current_line = ""

        for word in words:
            # Check if adding the next word would exceed the max_length
            if len(current_line) + len(word) + 1 > self.max_length:
                formatted_text.append(current_line)  # Append the current line to the result
                current_line = word  # Start a new line with the current word
            else:
                if current_line:
                    current_line += " " + word  # Add the word to the current line with a space
                else:
                    current_line = word  # Start a new line if current_line is empty

        if current_line:
            formatted_text.append(current_line)  # Append any remaining words in current_line

        # Join the formatted text with newline characters and return it as a single string
        return '\n'.join(formatted_text)


class News(Publication):
    """News publication with city information."""

    def __init__(self, p_pc_dict: dict):
        super().__init__("News", p_pc_dict["Text"])
        self.city = self.split_text(p_pc_dict["City"]) if p_pc_dict["City"] else 'Great_City'

    def format_publication(self) -> str:
        """Formats the news record for saving."""
        date = datetime.now().strftime("%Y/%m/%d")
        time = datetime.now().strftime("%H:%M")
        self.info_line = f"{self.city}, {date}  {time}"
        base_format = super().format_publication()
        return f"{base_format}{self.info_line}"


class PrivateAd(Publication):
    """Private ad publication with expiration date and day left calculation."""

    def __init__(self, p_pc_dict: dict):
        super().__init__("Private_ad", p_pc_dict["Text"])
        self.expiration_date = p_pc_dict["Expiration_date"] \
            if p_pc_dict["Expiration_date"] else (datetime.now() + timedelta(days=1)).strftime("%Y/%m/%d")
        self.days_left = self.calculate_days_left()

    def calculate_days_left(self) -> int:
        """Calculates the number of days left until expiration."""
        if isinstance(self.expiration_date, str):
            exp_date = datetime.strptime(self.expiration_date, "%Y/%m/%d")
        else:
            exp_date = self.expiration_date
        return (exp_date - datetime.now()).days

    def format_publication(self) -> str:
        """Formats the ad record for saving."""
        info_line = f"Actual until: {self.expiration_date}, {self.days_left} days left"
        base_format = super().format_publication()
        return f"{base_format}{info_line}"


class Joke(Publication):
    """Joke publication with hashtag and a random fun index."""

    def __init__(self, p_pc_dict: dict):
        super().__init__("Joke", p_pc_dict["Text"])
        self.hashtag = self.split_text(p_pc_dict["Hashtag"])

    def format_publication(self) -> str:
        """Formats the joke record for saving."""
        fun_index = random.randint(1, 10)
        self.hashtag = self.hashtag if self.hashtag else 'FunnyJoke'
        self.info_line = f"HashTag: #{self.hashtag} Fun Index: {'*' * fun_index} ({fun_index}/10)"
        base_format = super().format_publication()
        return f"{base_format}{self.info_line}"


class FileManager:
    """File manager class to handle saving publications to a text file."""

    def __init__(self, p_file_path: str):
        self.file_path = p_file_path
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        self.mode = 'a' if os.path.exists(self.file_path) and os.stat(self.file_path).st_size > 0 else 'w'

    @staticmethod
    def validate_file_path(p_file_path: str, p_file_extension: str):

        if not os.path.exists(p_file_path):
            print('File is not present in the specified folder.')
            sys.exit()

        if not os.path.splitext(p_file_path)[1] == p_file_extension:
            print('Incorrect file format.')
            sys.exit()

    def save_publications(self, p_publication_list: list[Publication]):
        """Saves a new publication to the text file."""

        with open(self.file_path, self.mode) as f:
            if self.mode == 'w':
                f.write("News feed:")

            for publication in p_publication_list:
                f.write("\n\n")
                f.write(publication.format_publication())

    @staticmethod
    def read_txt_file(p_file_path: str) -> list[dict]:

        FileManager.validate_file_path(p_file_path, '.txt')

        try:
            publications = []
            with open(p_file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    title, text, info_line = (line.split('#') + [""] * 3)[:3]
                    title, text, info_line = title.strip(), text.strip(), info_line.strip()

                    title = title.upper()
                    publication = {"Type": title, "Text": text}

                    if title == "NEWS":
                        publication["City"] = info_line
                    elif title == "PRIVATE_AD":
                        publication["Expiration_date"] = info_line
                    elif title == "JOKE":
                        publication["Hashtag"] = info_line

                    publications.append(publication)
            return publications

        except ValueError:
            raise ValueError(f"TXT file '{p_file_path}' has an incorrect file structure")

    @staticmethod
    def read_json_file(p_file_path: str) -> list[dict]:

        FileManager.validate_file_path(p_file_path, '.json')

        try:
            with open(p_file_path, 'r', encoding='utf-8') as file:
                publications = json.load(file)

            return publications

        except ValueError:
            raise ValueError(f"JSON file '{p_file_path}' has an incorrect file structure")

    @staticmethod
    def read_xml_file(p_file_path: str) -> list[dict]:

        FileManager.validate_file_path(p_file_path, '.xml')

        try:
            publications = []
            tree = ElementTree.parse(p_file_path)
            root = tree.getroot()

            for record in root.findall('Publication'):
                record_dict = {}
                for elem in record:
                    record_dict[elem.tag] = elem.text

                publications.append(record_dict)
            return publications

        except ValueError:
            raise ValueError(f"XML file '{p_file_path}' has an incorrect file structure")


class PublicationCSVProcessor:
    """Class to process publications.txt file and generate two CSV files based on word and letter statistics."""

    def __init__(self, p_publication_file: str, p_words_csv_file: str, p_letters_csv_file: str):
        self.publication_file = p_publication_file
        self.words_csv_file = p_words_csv_file
        self.letters_csv_file = p_letters_csv_file

    def process_words(self):
        """Processes words in publications.txt and creates a CSV file with word counts."""
        if not os.path.exists(self.publication_file):
            print("Publication file not found!")
            return

        word_counter = Counter()

        with open(self.publication_file, 'r', encoding='utf-8') as file:
            for line in file:
                words = line.split()  # Split by whitespace to get individual words

                for word in words:
                    # Remove leading/trailing non-alphabetical characters
                    cleaned_word = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', word)

                    # Count the word only if it contains at least one letter
                    if any(char.isalpha() for char in cleaned_word):
                        word_counter[cleaned_word.lower()] += 1  # Count case-insensitive

        # Write results to the CSV file
        with open(self.words_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Word', 'Quantity'])

            # Write the word count to the CSV file
            for word, count in word_counter.items():
                writer.writerow([word, count])

    def process_letters(self):
        """Processes letters and digits in publications.txt and creates a CSV file with counts."""
        if not os.path.exists(self.publication_file):
            print("Publication file not found!")
            return

        letter_counter = Counter()
        upper_counter = Counter()

        total_letter_count = 0

        # Open the publication file and read its content
        with open(self.publication_file, 'r', encoding='utf-8') as file:
            for line in file:
                for char in line:
                    if char.isalpha():  # Check if the character is alphanumeric (letter or digit)
                        letter_counter[char.lower()] += 1  # Count the character (case-insensitive)
                        if char.isupper():  # Count uppercase letters
                            upper_counter[char.lower()] += 1
                        total_letter_count += 1

        # Open the CSV file and write the header and data
        with open(self.letters_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Letter/Digit', 'Count_all', 'Count_Upper', 'Percentage'])

            # Iterate over letters and digits that are in the file
            for char, count_all in letter_counter.items():
                count_upper = upper_counter[char]
                percentage = (count_upper / count_all * 100) if count_all > 0 else 0
                writer.writerow([char, count_all, count_upper, round(percentage, 2)])


class ConsoleInputPublication:
    """Processes publication information entered by the user via the console."""

    @staticmethod
    def get_valid_expiration_date() -> datetime:
        """Prompts the user to input a valid expiration date in the format YYYY/MM/DD that is greater than today."""
        while True:
            expiration_date = input("Enter the expiration date (YYYY/MM/DD): ")
            try:
                # Parse the date and compare it with today's date
                exp_date = datetime.strptime(expiration_date, "%Y/%m/%d")
                if exp_date > datetime.now():
                    return exp_date
                else:
                    print("The expiration date must be in the future. Please try again.")
            except ValueError:
                print("Invalid date format. Please use YYYY/MM/DD format and enter a valid date.")

    @staticmethod
    def process_publications() -> list[dict]:
        """Handles user input and adds publications to the file."""
        print("\nPlease select the type of publication you want to add:")
        print("1. News")
        print("2. Private_ad")
        print("3. Joke")

        input_publications = []

        while True:
            match input("\nEnter your choice (1, 2, or 3). Exit code - '0' : "):
                case "0":
                    print("\nExiting the program.")
                    break

                case "1":
                    inp_text = input("Enter the news text: ")
                    inp_city = input("Enter the city: ")
                    input_publications.append({"Type": "News", "Text": inp_text, "City": inp_city})
                    print("News has been added to the feed.")

                case "2":
                    inp_text = input("Enter the ad text: ")
                    expiration_date = ConsoleInputPublication.get_valid_expiration_date()

                    input_publications.append(
                        {"Type": "Private_ad", "Text": inp_text, "Expiration_date": expiration_date})

                    print("Private ad has been added to the feed.")

                case "3":
                    inp_text = input("Enter the joke text: ")
                    inp_hashtag = input("Enter a hashtag: ")

                    input_publications.append(
                        {"Type": "Joke", "Text": inp_text, "Hashtag": inp_hashtag})

                    print("Joke has been added to the feed.")

                case _:
                    print("Invalid choice. Please select a valid option.")

        return input_publications


def main():
    """Main function to determine how to process publications: console or file."""
    publication_file_name = 'publications.txt'
    words_csv_file_name = 'words_count.csv'
    letters_csv_file_name = 'letters_count.csv'
    publication_file = os.path.join(os.getcwd(), publication_file_name)
    words_csv_file = os.path.join(os.getcwd(), words_csv_file_name)
    letters_csv_file = os.path.join(os.getcwd(), letters_csv_file_name)
    txt_input_file_name = 'texts_for_publications.txt'
    json_input_file_name = 'texts_for_publications.json'
    xml_input_file_name = 'texts_for_publications.xml'
    csv_processor = PublicationCSVProcessor(publication_file, words_csv_file, letters_csv_file)

    print("\nWelcome to the User-Generated News Feed!")
    print("Please choose how would you like to input publications:")
    print("1. Console")
    print("2. 'txt' file")
    print("3. 'json' file")
    print("4. 'xml' file")
    print("Exit code - '0'")

    exit_requested = False

    while not exit_requested:
        input_type = input("\nEnter your choice: ").strip()

        if input_type == "0":
            print("\nExiting the program.")
            exit_requested = True

        elif input_type in ("1", "2", "3", "4"):

            if input_type == "1":
                publication_texts = ConsoleInputPublication.process_publications()
            else:
                match input_type:
                    case "2":
                        input_file_path = txt_input_file_name
                    case "3":
                        input_file_path = json_input_file_name
                    case _:
                        input_file_path = xml_input_file_name
                input_file_path = os.path.join(os.getcwd(), input_file_path)
                print(f"\nDefault file path is {input_file_path}")
                while True:
                    choice = \
                        input("\nSelect content file location (1. Default path 2. Other path. Exit code - '0'): ")
                    match choice:
                        case "0":
                            print("\nExiting the program.")
                            sys.exit()
                        case "1":
                            print('\nProcessing content file...')
                            break
                        case "2":
                            input_file_path = input("Please input full file path: ")
                            if os.path.exists(input_file_path):
                                break
                            else:
                                print("File not found. Please input correct file path: ")
                        case _:
                            print("Invalid input.")
                match input_type:
                    case "2":
                        publication_texts = FileManager.read_txt_file(input_file_path)
                    case "3":
                        publication_texts = FileManager.read_json_file(input_file_path)
                    case _:
                        publication_texts = FileManager.read_xml_file(input_file_path)

            publications_list = []
            for publication_item in publication_texts:
                item = {}
                for key, value in publication_item.items():
                    if type(value) == str:
                        item[capitalize_sentences(key)] = capitalize_sentences(value)
                    else:
                        item[capitalize_sentences(key)] = value
                match item["Type"]:
                    case "News":
                        publications_list.append(News(item))
                    case "Private_ad":
                        publications_list.append(PrivateAd(item))
                    case "Joke":
                        publications_list.append(Joke(item))
            FileManager(publication_file).save_publications(publications_list)
            csv_processor.process_words()  # Count the words
            csv_processor.process_letters()  # Count letters statistics
            print('\nFile was successfully processed and deleted')
            exit_requested = True

            if input_type in ("2", "3", "4"):
                os.remove(input_file_path)  # Delete input file if successfully processed

        else:
            print("Invalid input type. Please make your choice (1. Console  2. File. Exit code - '0'):")


if __name__ == "__main__":
    main()
