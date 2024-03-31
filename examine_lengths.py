from collections import Counter
import json
import pathlib
import re

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
Results:
For Requested Size 10
10 20

For Requested Size 100
98 4
100 3
97 3
99 3
101 2
95 1
102 1
103 1
85 1
87 1

For Requested Size 1000
2048 7
1379 1
1023 1
998 1
167 1
1851 1
100 1
1726 1
319 1
153 1
1182 1
176 1
102 1
1981 1

stopped early values
2048
2048
2048
2048
2048
2048
2048
"""

def main():
    dataset_dir = pathlib.Path(__file__).parent / 'gpt_raw_responses'

    # It's silly I need to do this, I should have included the number of numbers requested directly in the saved JSON!
    # That was bad planning, but at least I still can extract the value from the filename. 
    parse_file_re = re.compile('^r(\d+?)\.(\d+).json$')

    generated_lists_by_request_size = {
        10: [],
        100: [],
        1000: []
    }

    stopped_due_to_length = []

    for filepath in sorted(dataset_dir.iterdir()):
        requested_num_of_nums = int(parse_file_re.findall(filepath.name)[0][0])
        with open(filepath) as f:
            raw_data = json.load(f)

        # Assume GPT followed instructions split on space should give some numbers
        chat_gpt_random_list = raw_data['text_response'].split(' ')

        # Parse out the ints
        ints = []

        for i in chat_gpt_random_list:
            try:
                ints.append(int(i))
            except:
                print('non-int value: ', i)
                corrected = correct_known_failures(i)
                if corrected is not None:
                    ints.append(i)

        generated_lists_by_request_size[requested_num_of_nums].append(ints)
        if raw_data['finish_reason'] == 'length':
            stopped_due_to_length.append(ints)


    for requested_size, list_of_results in generated_lists_by_request_size.items():
        length_frequency = Counter()
        for l in list_of_results:
            length_frequency[len(l)] += 1

        print(f"For Requested Size {requested_size}")
        for length, frequency in length_frequency.most_common():
            print(length, frequency)

    print("stopped early values")
    for early_stopped in stopped_due_to_length:
        print(len(early_stopped))



def correct_known_failures(non_number_string):
    '''
    The exhaustive set of failure patterns in the data is very small,
    so we can manually correct them. Future experiments may require 
    updates to this function to succeed.
    '''

    # These are the only patterns where GPT almost produced a number
    # other known failure patterns are not salvageable.
    if non_number_string.endswith('...'):
        return int(non_number_string[:-3])
    elif non_number_string.endswith('.'):
        return int(non_number_string[:-1])
    elif non_number_string.endswith('stringstream'):
        return int(non_number_string[:-12])
    elif '\n' in non_number_string and non_number_string != '\n':
        return int(non_number_string.split('\n')[0])
    
    return None


if __name__ == '__main__':
    main()
