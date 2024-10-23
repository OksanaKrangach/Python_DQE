"""
******************************************************************************************
Expand previous Homework 5 with additional class, which allow to provide records by text file:
1.Define your input format (one or many records)
2.Default folder or user provided file path
3.Remove file if it was successfully processed
4.Apply case normalization functionality form Homework 3/4

******************************************************************************************
File structure description:
each line contains separate publication text and has a structured format like: "News # Text # City #"

Example of the input file structure:
News # This is an example of a news text that spans multiple lines and should be processed correctly. # Austin #
Private ad # I'm selling a slightly used bike in great condition. Contact me for more details! # 2024/12/01 #
Joke # Why don't skeletons fight each other? Because they don't have the guts! # Humor #
---

******************************************************************************************
HW: All publications will be saved in the publications.txt file that is stored in the Classes_OOP folder.
    If the file doesn't exist, it will be created automatically.

    When entering text from the console, '###' symbols on the new line is used as the end of input indicator.
"""


import os
from datetime import datetime
import random
import sys
import strings_func_4


class Publication:
    """Base class for different types of publications."""

    def __init__(self, title: str, text: str):
        self.title = title
        self.text = text
        self.date = datetime.now().strftime("%Y/%m/%d")
        self.time = datetime.now().strftime("%H:%M")
        self.max_length: int = 50
        self.info_line = ''

    def format_publication(self) -> str:
        """Returns the formatted string of the publication to be saved to the file."""
        self.text = self.text if self.text else 'Here should be your text'
        formatted_title = f"{self.title}{'-' * (self.max_length - len(self.title))}"
        return f"{formatted_title}\n{self.text}\n"

    @staticmethod
    def get_multiline_input(p_prompt: str = "Enter the text: ", termination_symbol="###") -> list:
        """Gets user input that can span multiple lines until a termination symbol is entered.
        If any line exceeds max_length, it will be split into whole words.
        """
        print(f"{p_prompt} (End input with '{termination_symbol}' on a new line):")
        input_lines = []
        while True:
            line = input().strip()
            if line == termination_symbol:
                break
            input_lines.append(line)
        return input_lines

    def split_text(self, p_text: list) -> str:
        # Split into lines with max_length, keeping whole words intact
        formatted_text = []

        for line in p_text:
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

    @staticmethod
    def get_valid_expiration_date() -> str:
        """Prompts the user to input a valid expiration date in the format YYYY/MM/DD that is greater than today."""
        while True:
            expiration_date = input("Enter the expiration date (YYYY/MM/DD): ")
            try:
                # Parse the date and compare it with today's date
                exp_date = datetime.strptime(expiration_date, "%Y/%m/%d")
                if exp_date > datetime.now():
                    return expiration_date
                else:
                    print("The expiration date must be in the future. Please try again.")
            except ValueError:
                print("Invalid date format. Please use YYYY/MM/DD format and enter a valid date.")


class News(Publication):
    """News publication with city information."""

    def __init__(self, text: str, city: str):
        super().__init__("News", text)
        self.city = city

    def format_publication(self) -> str:
        """Formats the news record for saving."""
        self.city = self.city if self.city else 'Great_City'
        self.date = self.date if self.date else '9999-12-31'
        self.info_line = f"{self.city}, {self.date}  {self.time}"
        base_format = super().format_publication()
        return f"{base_format}{self.info_line}"


class PrivateAd(Publication):
    """Private ad publication with expiration date and day left calculation."""

    def __init__(self, text: str, expiration_date: str):
        super().__init__("Private ad", text)
        self.expiration_date = expiration_date
        self.days_left = self.calculate_days_left()

    def calculate_days_left(self) -> int:
        """Calculates the number of days left until expiration."""
        exp_date = datetime.strptime(self.expiration_date, "%Y/%m/%d")
        return (exp_date - datetime.now()).days

    def format_publication(self) -> str:
        """Formats the ad record for saving."""
        self.info_line = f"Actual until: {self.expiration_date}, {self.days_left} days left"
        base_format = super().format_publication()
        return f"{base_format}{self.info_line}"


class Joke(Publication):
    """Joke publication with hashtag and a random fun index."""

    def __init__(self, text: str, hashtag: str):
        super().__init__("Joke", text)
        self.hashtag = hashtag
        self.fun_index = random.randint(1, 10)
        self.fun_index_char = self.generate_fun_index_char()

    def generate_fun_index_char(self) -> str:
        """Generates a character-based fun index"""
        return '*' * self.fun_index

    def format_publication(self) -> str:
        """Formats the joke record for saving."""
        self.hashtag = self.hashtag if self.hashtag else 'FunnyJoke'
        self.info_line = f"HashTag: #{self.hashtag} Fun Index: {self.fun_index_char} ({self.fun_index}/10)"
        base_format = super().format_publication()
        return f"{base_format}{self.info_line}"


class FileManager:
    """File manager class to handle saving publications to a text file."""

    def __init__(self, file_path: str = None):
        self.default_path = os.path.join(os.getcwd(), 'publications.txt')
        if file_path is None:
            self.file_path = self.default_path
        else:
            self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def save_to_file(self, publication: Publication):
        """Saves a new publication to the text file."""
        mode = 'a' if os.path.exists(self.file_path) and os.stat(self.file_path).st_size > 0 else 'w'
        with open(self.file_path, mode) as f:
            if mode == 'w':
                f.write("News feed:\n")
            else:
                f.write("\n\n")  # Add two empty lines between publications
            f.write(publication.format_publication())

    @staticmethod
    def read_file(p_file_path: str) -> str:
        """Reads the file and returns its content."""
        if not os.path.exists(p_file_path):
            return "File not found"
        with open(p_file_path, 'r') as f:
            return f.read()


class FileInputPublication:
    """Processes publication information from a file provided by the user."""

    def __init__(self, p_file_manager: FileManager, p_publication: Publication, p_input_file_path: str):
        self.input_file_path = p_input_file_path
        self.file_manager = p_file_manager
        self.publication = p_publication

    def process_publications(self):
        """Processes the input file and adds publications to the file manager."""
        print(self.input_file_path)
        if not os.path.exists(self.input_file_path):
            print("File with content not found.")
            sys.exit()

        with open(self.input_file_path, 'r') as f:
            lines = f.readlines()

        processed_text = strings_func_4.capitalize_sentences(''.join(lines))  # Normalize using process_text()

        for line in processed_text.split('\n'):
            # Assuming each line has a structured format like: "News # Text # City #"
            if line.startswith("News"):
                title, inp_text, inp_city = (line.split('#') + [""] * 3)[:3]
                text = self.publication.split_text([inp_text])
                city = self.publication.split_text([inp_city])
                news = News(text=text, city=city.strip())
                self.file_manager.save_to_file(news)
            elif line.startswith("Private ad"):
                title, inp_text, expiration_date = (line.split('#') + [""] * 3)[:3]
                text = self.publication.split_text([inp_text])
                private_ad = \
                    PrivateAd(text=text, expiration_date=expiration_date.strip())
                self.file_manager.save_to_file(private_ad)
            elif line.startswith("Joke"):
                title, inp_text, inp_hashtag = (line.split('#') + [""] * 3)[:3]
                text = self.publication.split_text([inp_text])
                hashtag = self.publication.split_text([inp_hashtag])
                joke = Joke(text=text, hashtag=hashtag.strip())
                self.file_manager.save_to_file(joke)

        os.remove(self.input_file_path)  # Delete the file if successfully processed


class ConsoleInputPublication:
    """Processes publication information entered by the user via the console."""

    def __init__(self, p_file_manager: FileManager):
        self.file_manager = p_file_manager

    def process_publications(self):
        """Handles user input and adds publications to the file."""
        print("\nWelcome to the User-Generated News Feed!")
        print("Please select the type of publication you want to add:")
        print("1. News")
        print("2. Private ad")
        print("3. Joke")

        base_publication = Publication("", "")

        while True:
            choice = input("\nEnter your choice (1, 2, or 3). Exit code - '0'. Read all news feed - '5' : ")

            if choice == "0":
                print("\nExiting the program.")
                sys.exit()

            elif choice == "1":
                inp_text = base_publication.get_multiline_input("Enter the news text: ")
                text = base_publication.split_text(inp_text)
                inp_city = base_publication.get_multiline_input("Enter the city: ")
                city = base_publication.split_text(inp_city)
                news = News(text=text, city=city)
                self.file_manager.save_to_file(news)
                print("News has been added to the feed.")

            elif choice == "2":
                inp_text = base_publication.get_multiline_input("Enter the ad text")
                text = base_publication.split_text(inp_text)
                expiration_date = Publication.get_valid_expiration_date()
                private_ad = PrivateAd(text=text, expiration_date=expiration_date)
                self.file_manager.save_to_file(private_ad)
                print("Private ad has been added to the feed.")

            elif choice == "3":
                inp_text = base_publication.get_multiline_input("Enter the joke text")
                text = base_publication.split_text(inp_text)
                inp_hashtag = base_publication.get_multiline_input("Enter a hashtag")
                hashtag = base_publication.split_text(inp_hashtag)
                joke = Joke(text=text, hashtag=hashtag)
                self.file_manager.save_to_file(joke)
                print("Joke has been added to the feed.")

            elif choice == '5':
                print(self.file_manager.read_file(self.file_manager.file_path))

            else:
                print("Invalid choice. Please select a valid option.")


def main():
    """Main function to determine how to process publications: console or file."""
    input_type = \
        input("How would you like to input publications? (1. Console  2. File. Exit code - '0'): ").strip().lower()
    input_file_name = 'texts_for_publications.txt'
    file_manager = FileManager()
    publication = Publication("", "")

    while True:
        if input_type == "0":
            print("\nExiting the program.")
            break
        elif input_type == "1":
            processor = ConsoleInputPublication(file_manager)
            processor.process_publications()
        elif input_type == "2":
            input_file_path = os.path.join(os.getcwd(), input_file_name)
            print(f"\nDefault file path is {input_file_path}")
            while True:
                choice = \
                    input("\nSelect location of the content file (1. Default path 2. Other path. Exit code - '0'):")
                if choice == "0":
                    print("\nExiting the program.")
                    sys.exit()
                elif choice == "1":
                    print('\nProcessing content file...')
                    break
                elif choice == "2":
                    input_file_path = input("Please input full file path: ")
                    break
                else:
                    print("Invalid input. Please make your choice (1. Default path 2. Other path. Exit code - '0'):")
            file_processor = FileInputPublication(file_manager, publication, input_file_path)
            file_processor.process_publications()
            print('\nFile was successfully processed and removed')
            sys.exit()
        else:
            print("Invalid input type. Please make your choice (1. Console  2. File. Exit code - '0'):")


if __name__ == "__main__":
    main()
