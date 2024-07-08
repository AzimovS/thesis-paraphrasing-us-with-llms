from itertools import product
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import pandas as pd
import metrics
import itertools
import time

start_time = time.time()

NUM_COMBINATIONS = 1
IS_DEFINITION_INCLUDED = True
OPTIONS = ["increase", "decrease", "don't change"]
MODEL_NAME="solar"

FILENAME = "Synthetic User Stories.xlsx"
SHEETNAME = "Dataset"
 
df = pd.read_excel(FILENAME, SHEETNAME)
df = df.sample(n=100, random_state=42)

llm = Ollama(model=MODEL_NAME)

metric_functions = [
    metrics.total_characters,
    metrics.uppercase_characters,
    metrics.lowercase_characters,
    metrics.special_characters,
    metrics.numbers,
    metrics.blanks,
    metrics.number_of_words,
    metrics.average_length_of_words,
    metrics.number_of_propositions,
    metrics.average_length_of_propositions,
    metrics.punctuation_characters,
    metrics.lowercase_words,
    metrics.uppercase_words,
    metrics.vocabulary_richness,
    metrics.number_of_urls,
    metrics.flesch_kincaid_grade_level,
    metrics.flesch_reading_ease,
    metrics.dale_chall_readability,
    metrics.automated_readability_index,
    metrics.coleman_liau_index,
    metrics.gunning_fog,
    metrics.smog_index,
    metrics.linsear_write_index
]

prompt = PromptTemplate(
    input_variables=["user_story"],
    template="Paraphrase the following user story and output only paraphrased version: \n{user_story}",
)
chain = prompt | llm

for index, row in df.iterrows():
    user_story = row['User Story']
    paraphrased = None
    try:
        paraphrased = chain.invoke({'user_story': user_story})
        if ":" in paraphrased:
            paraphrased = paraphrased.split(":")[1]
        paraphrased = paraphrased.lstrip()
    except:
        paraphrased = "ERROR"
        print("\nERROR", user_story)
    df.at[index, f"par {MODEL_NAME}"] = paraphrased

df.to_csv(f"paraphrased_{MODEL_NAME}.csv", index=False)

end_time = time.time()
execution_time = end_time - start_time

print("Execution time:", execution_time, "seconds")



for func in metric_functions:
    # df['original_' + func.__name__] = df['User Story'].apply(func)
    df['llm_' + func.__name__] = df[f"par {MODEL_NAME}"].apply(func)

df.to_csv(f"metricvalues_{MODEL_NAME}.csv", index=False)
