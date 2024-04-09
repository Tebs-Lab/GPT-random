from collections import Counter
import json
import pathlib
import re

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def fix_and_cast_to_int(non_number_string):
    '''
    The exhaustive set of failure patterns in the data is very small,
    so we can manually correct them. Future experiments may require 
    updates to this function to succeed.
    '''
    try:
        return int(non_number_string)
    except:
        pass

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

def main():
    dataset_dir = pathlib.Path(__file__).parent / 'gpt_raw_responses'
    parse_file_re = re.compile('^r(\d+?)\.(\d+).json$')
    for filepath in sorted(dataset_dir.iterdir()):
        requested_num_of_nums = int(parse_file_re.findall(filepath.name)[0][0])
        with open(filepath) as f:
            raw_data = json.load(f)


        chat_gpt_random_list = [fix_and_cast_to_int(i) for i in raw_data['text_response'].split(' ') if fix_and_cast_to_int(i) != None]
        print(f'{requested_num_of_nums}: {min(chat_gpt_random_list)} - {max(chat_gpt_random_list)} ({len(chat_gpt_random_list)})')

if __name__ == '__main__':
    main()

"""FYI, output when run on the original 60 datasets:
10: 10 - 89
10: 3 - 91
10: 18 - 91
10: 15 - 94
10: 5 - 91
10: 5 - 85
10: 3 - 97
10: 13 - 91
10: 7 - 94
10: 10 - 93
10: 5 - 93
10: 12 - 98
10: 17 - 93
10: 12 - 98
10: 15 - 92
10: 12 - 95
10: 11 - 83
10: 8 - 91
10: 5 - 88
10: 14 - 87
100: 0 - 99
100: 1 - 99
100: 1 - 98
100: 1 - 100
100: 1 - 100
100: 1 - 100
100: 1 - 99
100: 1 - 100
100: 1 - 99
100: 6 - 99
100: 1 - 99
100: 12 - 96
100: 1 - 99
100: 1 - 100
100: 2 - 99
100: 10 - 98
100: 1 - 99
100: 1 - 100
100: 1 - 99
100: 1 - 99
1000: 3 - 1326
1000: 0 - 984752398
1000: 1 - 891
1000: 17 - 987
1000: 1 - 999
1000: 0 - 100
1000: 4 - 99
1000: 1 - 999
1000: 0 - 99
1000: 7 - 99
1000: 5 - 998
1000: 0 - 8294
1000: 3 - 100
1000: 1 - 101
1000: 10 - 99
1000: 87 - 998
1000: 0 - 100
1000: 12 - 90
1000: 1 - 999
1000: 48 - 999
"""