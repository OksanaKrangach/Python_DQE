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
    # Generate number of elements in the list item. Each dictionary can contain from 2 to 10 elements
    n = random.randint(2, 10)
    # Initiate dictionary element
    dict_elem = {}

    # Create dictionary element
    for j in range(n):
        # Generate key and value for the dictionary element
        k = random.choice(string.ascii_lowercase)
        v = random.randint(0, 100)
        # Add the new element with key k and value v
        dict_elem[k] = v

    dict_list.append(dict_elem)

print(f"Number of list elements: {cnt_elements}")
print(dict_list)

# Task_2 Create one dictionary
result_dict = {}

# Counter to track the index of the dictionary
index = 1

# Iterate over the list of dictionaries
for d in dict_list:
    for key, value in d.items():
        # Check if the key (or a variant with an underscore) already exists in result_dict
        matching_keys = [k for k in result_dict if k.startswith(key)]

        if matching_keys:
            # Find the existing key that matches the current key
            existing_key = matching_keys[0]
            # Update the key in the dictionary if the current value is larger
            if value > result_dict[existing_key]:
                new_key = f"{key}_{index}"
                # Delete previously added element with this key
                del result_dict[existing_key]
                # Add new element with this key and updated number of dictionary
                result_dict[new_key] = value
        else:
            # If the key is not already in the dictionary, add it
            result_dict[key] = value

    # Increment the index after processing each dictionary
    index += 1

print(result_dict)
