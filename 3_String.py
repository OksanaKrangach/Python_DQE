# Home task String Objects


import re

# Save text into variable
init_text = """homEwork:
 tHis iz your homeWork, copy these Text to variable.



 You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



 it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



 last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

# Convert text to lower case
lower_str = init_text.lower()

# Calculate the number of whitespace characters
whitespace_count = sum(1 for char in init_text if char.isspace())

print(f"Number of whitespace characters: {whitespace_count}\n")

# Replace ' iz ' with ' is '
updated_text = re.sub(r'\s+iz\s+', ' is ', lower_str)

# Create one more sentence with last words of each existing sentence and add it to the end of paragraph.

# Find all sentences using a regular expression
sentences = re.findall(r'\b\w[^.!?]*[.!?]', updated_text)
# print(sentences)

# Extract the last word of each sentence
last_words = [sentence.strip().split()[-1].rstrip('.!?') for sentence in sentences]

# Join the last words into a new sentence
new_sentence = ' '.join(last_words) + '.'

# Find the position to insert the new sentence
insertion_point = updated_text.find("end of this paragraph.") + len("end of this paragraph.")

# Insert the new sentence at the found position
final_text = updated_text[:insertion_point] + ' ' + new_sentence + updated_text[insertion_point:]

# Capitalize the first letter of each sentence
sentences = re.split(r'([.!?:]\s*)', final_text)
capitalized_sentences = []

for i, part in enumerate(sentences):
    if i % 2 == 0:
        capitalized_sentences.append(part.capitalize())
    else:
        capitalized_sentences.append(part)

final_text = ''.join(capitalized_sentences)

# Print the final result
print(final_text)
