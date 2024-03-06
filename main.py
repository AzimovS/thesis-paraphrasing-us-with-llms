from langchain_community.llms import Ollama
import pandas as pd
import metrics

FILENAME = "Synthetic User Stories.xlsx"
SHEETNAME = "Dataset"

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
    metrics.number_of_urls
]

llm = Ollama(model="llama2")
df = pd.read_excel(FILENAME, SHEETNAME)
df = df[:100]


def add_paraphrase_column(x):
    output = llm.invoke(
        f'Can you paraphrase the following user story: """{x}"""')
    output = output.split(':\n\n')[1]
    if output[0] == '"':
        return output[1:-1]
    return output


df['Paraphrased User Story'] = df['User Story'].apply(add_paraphrase_column)

for func in metric_functions:
    df['original_' + func.__name__] = df['User Story'].apply(func)
    df['llm_' + func.__name__] = df['Paraphrased User Story'].apply(func)
    df['diff_' + func.__name__] = df['original_' + func.__name__] - df['llm_' + func.__name__]

df.to_csv("new.csv")
