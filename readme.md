# Does GPT Understand Random?

Read this blog post to understand why this repo exists: [blog.tebs-lab.com/p/28dd7d9d-5832-4aec-bcec-f0f93b6e2df4](blog.tebs-lab.com/p/28dd7d9d-5832-4aec-bcec-f0f93b6e2df4)

## Using this code

The two jupyter notebooks are my exploratory data analysis, cleaned up very slightly. `GPT_random_eda_initial` has by step by step approach for examining the initial dataset. `datasets_eda_2` is that same code repurposed to loop through all the generated datasets.

The other Python files are all scripts. `generate_powers_of_ten_datasets.py` was used to create the 60 JSON files in `gpt_raw_responses`. The rest loop through those 60 files and report specific features of the datasets.

## Install Dependencies:

You should use a virtual environment. Regardless of whether you choose to you can install the dependencies with:

```
pip install -r requirements.txt
```