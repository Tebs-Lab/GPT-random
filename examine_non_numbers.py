from collections import Counter
import json
import pathlib
import re

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
Results:

In general, it followed the instructions for format very well. 
9 times there were multiple spaces in a row
2 times it added an ellipsis to the end
2 times it added a period to the end
1 time it added 'stringstream' to the end
1 time a newline appeared somewhere 
and in one dataset the chatbot added friendly text before and after the number string
  "I can provide 100 random numbers" and "Let me know if you would like more numbers!"

('', 9)
('77.', 1)
('4...', 1)
('\n', 1)
('93stringstream', 1)
('9...', 1)
('13.', 1)
('I', 1)
('can', 1)
('provide', 1)
('random', 1)
('numbers:', 1)
('40\n\nLet', 1)
('me', 1)
('know', 1)
('if', 1)
('you', 1)
('would', 1)
('like', 1)
('more', 1)
('numbers!', 1)
'''

non_numbers = Counter()
dataset_dir = pathlib.Path(__file__).parent / 'gpt_raw_responses'

for filepath in sorted(dataset_dir.iterdir()):
    with open(filepath) as f:
        raw_data = json.load(f)

    chat_gpt_random_list = raw_data['text_response'].split(' ')


    # EDA showed that GPT always tried to produce ints, so that's what we test for.
    for i in chat_gpt_random_list:
        try:
            int(i)
        except:
            non_numbers[i] += 1


for tup in non_numbers.most_common():
    print(tup)
