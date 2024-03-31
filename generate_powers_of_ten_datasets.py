from openai import OpenAI

import json
import pathlib
import random

'''
I don't want to pay for more requests than I need to so I want to generate
and save a bunch of raw text responses from ChatGPT. 

Goals of this procedure:

* Get 20 samples of requesting 10, 100, and 1000 random numbers
* Minimal variation amongst API parameters
    * I will set and save the "seed" parameter using a random number generator.
    * The API is stochastic by default, and I want that behavior, but I also
      want to maximize reproducibility. Setting the seed allows me to save it.
* Make it auditable: store relevant about the prompt/session with the response.
    * Let's use JSON, everyone loves JSON.
'''
def main():
    client = OpenAI()

    output_folder = pathlib.Path(__file__).parent / 'gpt_raw_responses'

    # 20 of 10
    for i in range(20):
        kwargs = produce_prompt_kwargs(10)
        filename = f'r10.{i}.json'
        request_then_serialize(client, kwargs, output_folder, filename)

    # 20 of 100
    for i in range(20):
        kwargs = produce_prompt_kwargs(100)
        filename = f'r100.{i}.json'
        request_then_serialize(client, kwargs, output_folder, filename)

    # 20 of 1000
    for i in range(20):
        kwargs = produce_prompt_kwargs(1000)
        filename = f'r1000.{i}.json'
        request_then_serialize(client, kwargs, output_folder, filename)


def request_then_serialize(client, api_kw_args, folder_path, filename):
    response = client.chat.completions.create(**api_kw_args)

    json_to_save = {
        'request_arguments': api_kw_args,
        'system_fingerprint': response.system_fingerprint,
        'id': response.id,
        'model_version': response.model,
        'text_response': response.choices[0].message.content,
        'finish_reason': response.choices[0].finish_reason

    }

    with open(folder_path/filename, 'w') as f:
        json.dump(json_to_save, f)


def produce_prompt_kwargs(num_of_nums):
    """
    Produce a dict that fits the OpenAI API for chat completion.
    The content of the user prompt changes with num_of_nums, and the seed
    is randomly generated. Everything else is deterministic.
    """
    user_prompt_content = f'Generate {num_of_nums} random numbers.'
    seed = random.getrandbits(32) # Produce a random 32-bit integer

    return {
        'model': "gpt-3.5-turbo",
        'messages': [
        {
            "role": "system", # Without this GPT added friendly but awkward to parse text to the output.
            "content": "You are a number generator. In all of your responses only use numbers, with each number separated using a space."
        },
        {
            "role": "user",
            "content": user_prompt_content
        }],
        'temperature': 1,
        'max_tokens': 4096, # Artificially large, GPT should generate many fewer if it follows the prompt.
        'top_p': 1,
        'frequency_penalty': 0,
        'presence_penalty': 0,
        'seed': seed
    }

if __name__ == '__main__':
    main()