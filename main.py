from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
import pandas as pd
import metrics

FILENAME = "Synthetic User Stories.xlsx"
SHEETNAME = "Dataset"


llm = Ollama(model="llama2")
response_schemas = [
    ResponseSchema(name="paraphrased", description="paraphrased version to the user's input"),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()
prompt = PromptTemplate(
    template="Paraphrase the user story provided by user.\n{format_instructions}\n{user_story}",
    input_variables=["user_story"],
    partial_variables={"format_instructions": format_instructions},
)

chain = prompt | llm | output_parser

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

df = pd.read_excel(FILENAME, SHEETNAME)
df = df[6000:]

def add_paraphrase_column(x):
    output = None
    try: 
        output = chain.invoke({'user_story': x})['paraphrased']
    except:
        output = "ERROR"
        print("ERROR", x)
    return output


df['Paraphrased User Story'] = df['User Story'].apply(add_paraphrase_column)
df.to_csv('tmp.csv', index=True)

for func in metric_functions:
    df['original_' + func.__name__] = df['User Story'].apply(func)
    df['llm_' + func.__name__] = df['Paraphrased User Story'].apply(func)
    df['diff_' + func.__name__] = df['original_' + func.__name__] - df['llm_' + func.__name__]

df.to_csv("withparaphrased.csv", index=False)
