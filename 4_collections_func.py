import random
import string


# Generate random dictionaries and return a list of them
def generate_random_dict_list(cnt_elements):
    dict_list = []  # Initialize an empty list to hold the dictionaries

    # Iterate to create `cnt_elements` number of dictionaries
    for _ in range(cnt_elements):
        # Generate a random dictionary and append it to the list
        n = random.randint(2, 10)  # Number of elements in the dictionary
        random_dict = generate_random_dict(n)
        dict_list.append(random_dict)

    return dict_list


# Generate a random dictionary with random keys and values
def generate_random_dict(n):

    dict_elem = {}  # Create an empty dictionary element

    for _ in range(n):  # Create dictionary element
        # Generate key and value for the dictionary element
        k = random.choice(string.ascii_lowercase)
        v = random.randint(0, 100)
        # Add the new element with key k and value v
        dict_elem[k] = v
    return dict_elem


# Merge two dictionaries with custom rules for duplicate keys
def merge_dicts(dict1, dict2, index):
    merged = dict1.copy()
    for key, value in dict2.items():
        matching_keys = [k for k in merged if k.startswith(key)]
        if matching_keys:
            existing_key = matching_keys[0]
            if value > merged[existing_key]:  # Keep the max value
                new_key = f"{key}_{index}"
                del merged[existing_key]
                merged[new_key] = value
        else:
            merged[key] = value
    return merged


# Create one dictionary from a list of dictionaries
def combine_dict_list(dict_list):
    # Initialize an empty dictionary to accumulate results
    result_dict = {}

    # Iterate over each dictionary in the list
    for current_dict in dict_list:
        # Find the index of the current dictionary in the list and add 1 for 1-based index
        index = dict_list.index(current_dict) + 1

        # Merge the current dictionary into the result_dict using merge_dicts()
        result_dict = merge_dicts(result_dict, current_dict, index)

    return result_dict


# Main function to generate, merge, and print dictionaries
def create_list():
    # Generate random number of dictionaries
    cnt_elements = random.randint(2, 10)
    # Generate dictionaries
    dict_list = generate_random_dict_list(cnt_elements)

    print(f"Generated list of dictionaries:\n{dict_list}\n")

    result_dict = combine_dict_list(dict_list)

    print(f"Resulting dictionary with unique keys:\n{result_dict}")


# Run the main function
if __name__ == "__main__":
    create_list()
