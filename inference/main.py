from itertools import product
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import pandas as pd
import metrics
import itertools
import time

start_time = time.time()

NUM_COMBINATIONS = 1
OPTIONS = ["increase", "decrease", "don't change"]
# OPTIONS = ["increase"]


FILENAME = "Synthetic User Stories.xlsx"
SHEETNAME = "Dataset"

df = pd.read_excel(FILENAME, SHEETNAME)
df = df.sample(n=100, random_state=42)

llm = Ollama(model="gemma:7b")


metric_to_instructions = {
    metrics.total_characters: " number of total characters",
    metrics.uppercase_characters: " number of uppercase characters",
    metrics.lowercase_characters: " number of lowercase characters",
    metrics.special_characters: " number of special characters",
    metrics.numbers: " number of numbers",
    metrics.blanks: " number of blanks",
    metrics.number_of_words: " number of words",
    metrics.average_length_of_words: " average length of words",
    metrics.number_of_propositions: " number of propositions",
    metrics.average_length_of_propositions: " average length of propositions",
    metrics.punctuation_characters: " number of punctuation characters",
    metrics.lowercase_words: " number of lowercase words",
    metrics.uppercase_words: " number of uppercase words",
    metrics.vocabulary_richness: " number of vocabulary richness",
    metrics.number_of_urls: " number of urls",
    metrics.flesch_kincaid_grade_level: " flesch kincaid grade level",
    metrics.flesch_reading_ease: " flesch reading ease",
    metrics.dale_chall_readability: " dale chall readability",
    metrics.automated_readability_index: " automated readability index",
    metrics.coleman_liau_index: " coleman liau index",
    metrics.gunning_fog: " gunning fog",
    metrics.smog_index: " smog index",
    metrics.linsear_write_index: " linsear write index"
}


# Generate combinations of keys
metric_combinations = itertools.combinations(
    list(metric_to_instructions.keys()), NUM_COMBINATIONS)


def eval(user_story, par, metric_func, option):
    res_user_story = metric_func(user_story)
    res_par = metric_func(par)
    print(res_user_story, res_par)
    if option == 'increase' and res_user_story < res_par:
        return 1
    if option == "don't change" and res_user_story == res_par:
        return 1
    if option == 'decrease' and res_user_story > res_par:
        return 1
    return 0

# metric_combinations = [list(comb) for comb in metric_combinations]
# print(metric_combinations)

def generate_all_pairs(list1, list2):
    res = []

    def recursion(cur, index=0):
        if len(cur) >= len(list1):
            res.append(cur)
            return
        for j in range(len(list2)):
            recursion(cur + [(list1[index], list2[j])], index + 1)

    recursion([])

    return res


all_combinations = []
for comb in metric_combinations:
    all_combinations.append(generate_all_pairs(comb, OPTIONS))

for combination in all_combinations:
    for pairs in combination:
        prompt_instructions = ""
        for pair in pairs:
            if prompt_instructions:
                prompt_instructions += ", "
            prompt_instructions += f'{pair[1]} {metric_to_instructions[pair[0]]}'
        print(prompt_instructions)
        prompt = PromptTemplate(
            input_variables=["user_story", "prompt_instructions"],
            template="Based on the following instruction: {prompt_instructions}.  Paraphrase the following user story and output only paraphrased version: \n{user_story}",
        )
        chain = prompt | llm

        for index, row in df.iterrows():
            user_story = row['User Story']
            paraphrased = None
            try:
                paraphrased = chain.invoke(
                    {'user_story': user_story, 'prompt_instructions': prompt_instructions})
                if ":" in paraphrased:
                    paraphrased = paraphrased.split(":")[1]
                paraphrased = paraphrased.lstrip()
            except:
                paraphrased = "ERROR"
                print("\nERROR", user_story)
            df.at[index, f"par {prompt_instructions}"] = paraphrased
            final_res = []
            for pair in pairs:
                final_res.append(eval(
                    user_story=user_story, par=paraphrased, metric_func=pair[0], option=pair[1]))
            print(final_res)
            df.at[index, f"res {prompt_instructions}"] = 1 if all(
                final_res) else 0
    df.to_csv("withparaphrased.csv", index=False)

end_time = time.time()
execution_time = end_time - start_time

print("Execution time:", execution_time, "seconds")