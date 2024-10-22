# Home task_2 Collections
"""
Write a code, which will:

1. create a list of random number of dicts (from 2 to 10)
dict's random numbers of keys should be letter,
dict's values should be a number (0-100),
example:[{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]

2. get previously generated list of dicts and create one common dict:
if dicts have same key, we will take max value, and rename key with dict number with max value
if key is only in one dict - take it as is,
example:{'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}
Each line of code should be commented with description.

Commit script to git repository and provide link as home task result.
"""

# Task_1 Create list of 100 random numbers from 0 to 1000
import random
import string

# Generate random number of list elements in the range from 2 to 10
cnt_elements = random.randint(2, 10)

dict_list = []

# Create list of  dictionaries
for i in range(cnt_elements):

    # Create dictionary element. Generate number of elements in the list item
    # Generate key and value for the dictionary element and add the new element with key k and value
    dict_elem = {random.choice(string.ascii_lowercase): random.randint(0, 100) for _ in range(random.randint(2, 10))}

    dict_list.append(dict_elem)

print(f"Number of list elements: {cnt_elements}")
print(dict_list)

# Task_2 Create one dictionary
# Initializing result dictionary to store the combined result
result_dict = {}

# Iterating over the list of dictionaries with their index, starting from 1
for index, d in enumerate(dict_list, start=1):
    for key, value in d.items():
        if key in result_dict:
            # If key already exists, checking if current value is greater than the stored value
            if value > result_dict[key][0]:
                # Updating value and recording the dictionary index for renaming
                result_dict[key] = (value, index)
        else:
            # Adding the key and value, and storing the dictionary index
            result_dict[key] = (value, index)

# Creating the final dictionary with renaming based on max value's index
final_dict = {}
for key, (value, idx) in result_dict.items():
    if sum(k == key for d in dict_list for k in d.keys()) > 1:
        # If the key appears in multiple dictionaries, rename it with the index of the dict with the max value
        final_dict[f"{key}_{idx}"] = value
    else:
        # If the key appears only in one dictionary, keep it as is
        final_dict[key] = value

print(final_dict)

