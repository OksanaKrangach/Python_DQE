import re


# Function to convert text to lowercase
def to_lower(func):
    def wrapper(text):
        result = func(text)
        return result.lower() if isinstance(result, str) else result

    return wrapper


# Function to calculate the number of whitespace characters
def count_whitespace(text):
    return sum(1 for char in text if char.isspace())


# Function to find all sentences using a regular expression
@to_lower
def find_sentences(text):
    return re.findall(r'\b\w[^.!?]*[.!?]', text)


# Function to extract the last word of each sentence
def extract_last_words(sentences):
    return [sentence.strip().split()[-1].rstrip('.!?') for sentence in sentences]


# Function to join the last words into a new sentence
def create_new_sentence(last_words):
    return ' '.join(last_words) + '.'


# Function to find the insertion point in the text
def find_insertion_point(text, phrase):
    return text.find(phrase) + len(phrase)


# Function to insert new sentence at the found position
def insert_new_sentence(text, new_sentence, insertion_point):
    return text[:insertion_point] + ' ' + new_sentence + text[insertion_point:]


# Function to capitalize the first letter of each sentence
def capitalize_sentences(text):
    # Check if text contains only numbers or dates in 'YYYY/MM/DD' format
    if re.match(r'^\d{4}/\d{2}/\d{2}$', text) or text.isdigit():
        return text  # Return as-is if it's a date or numeric-only

    # Step 1: Capitalize sentences with standard delimiters
    sentences = re.split(r'([.!?#]\s*)', text)
    capitalized_sentences = [part.capitalize() for part in sentences]
    partially_capitalized = ''.join(capitalized_sentences)

    # Step 2: Capitalize the first letter after `:\n` and any whitespace that follows it
    final_text = re.sub(r':\n\s*([a-zA-Z])', lambda match: ':\n' + match.group(1).upper(), partially_capitalized)

    return final_text


# Main function to normalize the text from letter case point of view
def process_text(p_inp_text):
    # Step 1: Convert to lowercase
    lower_str = to_lower(lambda x: x)(p_inp_text)

    # Step 2: Calculate number of whitespace characters
    whitespace_count = count_whitespace(lower_str)
    print(f"Number of whitespace characters: {whitespace_count}\n")

    # Step 3: Replace ' iz ' with ' is '
    updated_text = re.sub(r'\s+iz\s+', ' is ', lower_str)

    # Step 4: Find sentences and create new sentence from last words
    sentences = find_sentences(updated_text)
    last_words = extract_last_words(sentences)
    new_sentence = create_new_sentence(last_words)

    # Step 5: Insert new sentence at the correct position
    insertion_point = find_insertion_point(updated_text, "end of this paragraph.")
    final_text = insert_new_sentence(updated_text, new_sentence, insertion_point)

    # Step 6: Capitalize the first letter of each sentence
    final_text = capitalize_sentences(final_text)

    # Step 7: Print final text and calculate whitespace in the final text
    print(final_text)


# Run the main function
if __name__ == "__main__":
    # Save text into variable
    inp_text = """homEwork:
 tHis iz your homeWork, copy these Text to variable.


 You NEED TO normalize it: fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.


 it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.


 last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""

    process_text(inp_text)
