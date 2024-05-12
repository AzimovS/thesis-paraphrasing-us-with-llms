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

FILENAME = "Synthetic User Stories.xlsx"
SHEETNAME = "Dataset"

df = pd.read_excel(FILENAME, SHEETNAME)
df = df.sample(n=100, random_state=42)

llm = Ollama(model="llama3")

metric_to_instructions = {
    metrics.total_characters: [" number of total characters", "Total characters typically refers to the count of all individual characters, including letters, numbers, punctuation marks, spaces, and any other symbols, within a given text."],
    metrics.uppercase_characters: [" number of uppercase characters", "Uppercase characters refer to letters in the alphabet that are written or printed in their capital form. In English, uppercase characters include the letters A through Z. These characters are often used at the beginning of sentences, for proper nouns, and in acronyms."],
    metrics.lowercase_characters: [" number of lowercase characters", "Lowercase characters refer to letters in the alphabet that are written or printed in their smaller form. In English, lowercase characters include the letters a through z. These characters are commonly used in the body of sentences and words."],
    metrics.special_characters: [" number of special characters", "Special characters are symbols or characters that are not letters or numbers. They include punctuation marks such as commas, periods, exclamation points, question marks, as well as symbols like asterisks, ampersands, hashtags, dollar signs, and various other characters used for specific purposes in writing, coding, or communication."],
    metrics.numbers: [" number of numbers", "Numbers are symbols or words used to represent quantities, values, or positions in a numerical system."],
    metrics.blanks: [" number of blanks", "Blanks refer to the empty spaces or gaps between words, sentences, or characters."],
    metrics.number_of_words: [" number of words", "Words refer to sequences of characters that are separated by spaces or punctuation marks and convey meaning."],
    metrics.average_length_of_words: [" average length of words", "Average length of the word typically refers to the mean number of characters in the words of a given text. It's calculated by dividing the total number of characters in all the words by the total number of words in the text."],
    metrics.number_of_propositions: [" number of propositions", "Proposition is used to refer to individual segments of text that are separated by common sentence-ending punctuation marks (periods, exclamation marks, and question marks)."],
    metrics.average_length_of_propositions: [" average length of propositions", "Average length of propositions refers to the mean number of characters in the propositions or sentences within a given text. To calculate the average length of propositions, you'd first need to identify and isolate each proposition in the text, then compute the average length of characters across all propositions."],
    metrics.punctuation_characters: [" number of punctuation characters", "Punctuation characters are symbols used in writing to aid in understanding and interpreting the text by indicating pauses, boundaries, emphasis, and intonation."],
    metrics.lowercase_words: [" number of lowercase words", "Lowercase words in a text are words that are written using lowercase letters."],
    metrics.uppercase_words: [" number of uppercase words", "Uppercase words in a text are words that are written using uppercase or capital letters."],
    metrics.vocabulary_richness: [" number of vocabulary richness", "Vocabulary Richness is the length of the text without duplicated words."],
    metrics.number_of_urls: [" number of urls", "URL is a specific type of text string used to identify the location of a resource on the internet."],
    metrics.flesch_kincaid_grade_level: [" flesch kincaid grade level", "The formula for calculating Flesch Kincaid Grade Level is 0.39*(E)+11.8*(G)-15.59, where G is the average number of syllable per word, while E is the average number of words per proposition."],
    metrics.flesch_reading_ease: [" flesch reading ease", "The formula for calculating Flesch Reading Ease is 206.835-(84.6*G)-(1.015*E), where G is the average number of syllable per word, while E is the average number of words perproposition."],
    metrics.dale_chall_readability: [" dale chall readability", "The formula for calculating Dale Chall Readability is 0.1579*(PDW)+0.0496*ASL, where PDW is the percentage of difficult words (words that do not appear on a specially designed list of common words familiar to most 4th-grade students), while ASL is the average length of a proposition in words."],
    metrics.automated_readability_index: [" automated readability index", "The formula for calculating Automated Readability Index is 4.71*C/W+0.5*W/P-21.43, where W is the number of words contained in the text, C is the number of the total amount of characters in the text, while P is the number of propositions in the text."],
    metrics.coleman_liau_index: [" coleman liau index", "The formula for calculating Coleman Liau Index is 0.0588*L-0.296*S-15.8, where S is the average number of propositions per 100 words while L is the average number of letters per 100 words."],
    metrics.gunning_fog: [" gunning fog", "The formula for Gunning Fog is 0.4*(W/P+100*DW/W), where W is the number of words contained in the text, DW is the number of words consisting of three or more syllables, while P is the number of propositions in the text."],
    metrics.smog_index: [" smog index", "The formula for SMOG index is 1.0430*sqrt(DW*30/P)+3.1391, where DW is the number of words consisting of three or more syllables while P is the number of propositions in the text."],
    metrics.linsear_write_index: [" linsear write index", "The definition for Lineaser Write is for each word with two or less syllables an index is increased by 1, while for each word with more than three syllables, the index is increased by 3. Finally, the resulting number is divided by the number of propositions. If the result is greater than 20 it is divided by 2, otherwise it is divided by 2 and 1is subtracted from this number."],
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
        definition = ""
        prompt_instructions = "Based on the following instruction: "
        for pair in pairs:
            if not prompt_instructions.endswith("instruction: "):
                prompt_instructions += ", "
            prompt_instructions += f'{pair[1]} {metric_to_instructions[pair[0]][0]}'
            definition += f'{metric_to_instructions[pair[0]][1]}'
        if IS_DEFINITION_INCLUDED:
            prompt_instructions = definition + " " + prompt_instructions
        print(prompt_instructions)
        prompt = PromptTemplate(
            input_variables=["user_story", "prompt_instructions"],
            template="{prompt_instructions}.  Paraphrase the following user story and output only paraphrased version: \n{user_story}",
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