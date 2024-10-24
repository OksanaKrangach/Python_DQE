"""
Create a tool, which will do user generated news feed:
1.User select what data type he wants to add
2.Provide record type required data
3.Record is published on text file in special format

You need to implement:
1.News – text and city as input. Date is calculated during publishing.
2.Privat ad – text and expiration date as input. Day left is calculated during publishing.
3.Your unique one with unique publish rules.

Each new record should be added to the end of file.

HW: All publications will be saved in the publications.txt file that is stored in the 5_Classes folder.
    If the file doesn't exist, it will be created automatically.

    When entering any text, '#' symbol is used as the end of input indicator.
"""

import os
from datetime import datetime
import random


class Publication:
    """Base class for different types of publications."""

    def __init__(self, title: str, text: str):
        self.title = title
        self.text = text
        self.date = datetime.now().strftime("%Y/%m/%d")
        self.time = datetime.now().strftime("%H:%M")
        self.max_length = 40
        self.info_line = ''

    def format_publication(self) -> str:
        """Returns the formatted string of the publication to be saved to the file."""
        formatted_title = f"{self.title}{'-' * (self.max_length - len(self.title))}"
        return f"{formatted_title}\n{self.text}\n"

    def get_multiline_input(self, p_prompt: str = "Enter the text", termination_symbol: str = "#") -> str:
        """Gets user input that can span multiple lines until a termination symbol is entered.
        If any line exceeds max_length, it will be split into whole words.
        """
        print(f"{p_prompt} (end input with '{termination_symbol}' on a new line):")
        lines = []

        while True:
            line = input()
            if line.strip() == termination_symbol:
                break

            # Strip the line of leading/trailing whitespace
            line = line.strip()

            # Check if the line is not empty
            if line:
                # Split the line into words and manage line length
                current_line = ""
                for word in line.split():
                    # If adding the next word exceeds max_length, save the current line and start a new one
                    if len(current_line) + len(word) + (1 if current_line else 0) > self.max_length:
                        lines.append(current_line)  # Append the current line to the list
                        current_line = word  # Start a new line with the current word
                    else:
                        if current_line:
                            current_line += " " + word  # Add a space before appending the next word
                        else:
                            current_line = word  # Start the first word on a new line

                # Append the last line after processing the words
                if current_line:
                    lines.append(current_line)

        # Join lines with newline characters and return
        return '\n'.join(lines)

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
        self.info_line = f"{self.city}, {self.date}  {self.time}"
        base_format = super().format_publication()
        return f"{base_format}{self.info_line}"


class PrivateAd(Publication):
    """Private Ad publication with expiration date and day left calculation."""

    def __init__(self, text: str, expiration_date: str):
        super().__init__("Private Ad", text)
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
        """Generates a character-based fun index """
        return '*' * self.fun_index

    def format_publication(self) -> str:
        """Formats the joke record for saving."""
        self.info_line = f"HashTag: #{self.hashtag} Fun Index: {self.fun_index_char} ({self.fun_index}/10)"
        base_format = super().format_publication()
        return f"{base_format}{self.info_line}"


class FileManager:
    """File manager class to handle saving publications to a text file."""

    def __init__(self, file_path: str = None):
        if file_path is None:
            self.file_path = os.path.join(os.getcwd(), 'publications.txt')
            print(self.file_path)
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

    def read_file(self) -> str:
        """Reads the file and returns its content."""
        if not os.path.exists(self.file_path):
            return "File not found"
        with open(self.file_path, 'r') as f:
            return f.read()


def main():
    """Main function to handle user input and add publications to the file."""

    print("\nWelcome to the User-Generated News Feed!")
    print("Please select the type of publication you want to add:")
    print("1. News")
    print("2. Private Ad")
    print("3. Joke")

    fm = FileManager()
    base_publication = Publication("", "")

    while True:
        choice = input("\nEnter your choice (1, 2, or 3). Exit code - '0'. Read all news feed - '5' : ")

        if choice == "0":
            print("\nExiting the program.")
            break

        elif choice == "1":
            # Create a news publication
            text = base_publication.get_multiline_input(f"Enter the news text")
            city = base_publication.get_multiline_input("Enter the city")
            news = News(text=text, city=city)
            fm.save_to_file(news)
            print("News has been added to the feed.")

        elif choice == "2":
            # Create a private ad
            text = base_publication.get_multiline_input("Enter the ad text")
            expiration_date = Publication.get_valid_expiration_date()
            private_ad = PrivateAd(text=text, expiration_date=expiration_date)
            fm.save_to_file(private_ad)
            print("Private Ad has been added to the feed.")

        elif choice == "3":
            # Create a joke
            text = base_publication.get_multiline_input("Enter the joke text")
            hashtag = base_publication.get_multiline_input("Enter a hashtag")
            joke = Joke(text=text, hashtag=hashtag)
            fm.save_to_file(joke)
            print("Joke has been added to the feed.")

        elif choice == '5':
            print(fm.read_file())

        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
