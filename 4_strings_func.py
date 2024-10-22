import re


# Function to convert text to lowercase
def to_lower(text):
    return text.lower()


# Function to calculate the number of whitespace characters
def count_whitespace(text):
    return sum(1 for char in text if char.isspace())


# Function to replace ' iz ' with ' is '
def replace_iz_with_is(text):
    return re.sub(r'\s+iz\s+', ' is ', text)


# Function to find all sentences using a regular expression
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
    sentences = re.split(r'([.!?:]\s*)', text)
    capitalized_sentences = []

    for i, part in enumerate(sentences):
        if i % 2 == 0:
            capitalized_sentences.append(part.capitalize())
        else:
            capitalized_sentences.append(part)

    return ''.join(capitalized_sentences)


# Main function to normalize the text from letter case point of view
def process_text(inp_text):
    # Step 1: Convert to lowercase
    lower_str = to_lower(inp_text)

    # Step 2: Calculate number of whitespace characters
    whitespace_count = count_whitespace(init_text)
    print(f"Number of whitespace characters: {whitespace_count}\n")

    # Step 3: Replace ' iz ' with ' is '
    updated_text = replace_iz_with_is(lower_str)

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
    init_text = """homEwork:
 tHis iz your homeWork, copy these Text to variable.



 You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



 it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



 last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""

    process_text(init_text)
