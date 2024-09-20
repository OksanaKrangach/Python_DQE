# Home task_1 Basics
# Create a python script:

# create list of 100 random numbers from 0 to 1000
# sort list from min to max (without using sort())
# calculate average for even and odd numbers
# print both average result in console
# Each line of code should be commented with description.#
# Commit script to git repository and provide link as home task result.

import random

# create empty list
random_list = []

# add to the list 100 random numbers from 0 to 1000
for i in range(100):
    random_list.append(random.randint(0, 1000))

# sort list from min to max (without using sort())
n = len(random_list)
for i in range(n):
    # Starting from the first element
    min_index = i
    # Compare rest of the elements with i-element to find the smallest
    for j in range(i + 1, n):
        if random_list[j] < random_list[min_index]:
            min_index = j
    # Swap the found minimum element with the first element
    random_list[i], random_list[min_index] = random_list[min_index], random_list[i]

# Print the sorted list
print(random_list)

# calculate average for even and odd numbers
ev_sum = 0
od_sum = 0
ev_cnt = 0
od_cnt = 0

# Iterate through the list to classify and sum even and odd numbers
for elem in random_list:
    if elem % 2 == 0:
        ev_sum += elem
        ev_cnt += 1
    else:
        od_sum += elem
        od_cnt += 1

# Calculate averages
if ev_cnt > 0:
    ev_avg = ev_sum / ev_cnt
else:
    ev_avg = 0

if od_cnt > 0:
    od_avg = od_sum / od_cnt
else:
    od_avg = 0

# print both average results rounded to 3 decimals in console
print(f"Average for even numbers: {ev_avg:.3f} \nAverage for odd  numbers: {od_avg:.3f}")
