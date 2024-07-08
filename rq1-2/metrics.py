import string
import re
import textstat

def total_characters(text):
    return len(text)

def uppercase_characters(text):
    return sum(1 for char in text if char.isupper())

def lowercase_characters(text):
    return sum(1 for char in text if char.islower())

def special_characters(text):
    special_chars = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    return sum(1 for char in text if char in special_chars)

def numbers(text):
    return sum(1 for char in text if char.isdigit())

def blanks(text):
    return sum(1 for char in text if char.isspace())

def number_of_words(text):
    # print(text)
    return len(text.split())

def average_length_of_words(text):
    words = text.split()
    total_length = sum(len(word) for word in words)
    num_words = len(words)
    if num_words == 0:
        return 0
    return total_length / num_words

def number_of_propositions(text):
    propositions = re.split(r'[.!?]+', text)
    return len([prop for prop in propositions if prop.strip()])

def average_length_of_propositions(text):
    propositions = re.split(r'[.!?]+', text)
    lengths = [len(prop.strip().split()) for prop in propositions if prop.strip()]
    if lengths:
        return sum(lengths) / len(lengths)
    else:
        return 0

def punctuation_characters(text): 
    return sum(1 for char in text if char in string.punctuation)

def lowercase_words(text):
    words = text.split()
    return sum(1 for word in words if word.islower())

def uppercase_words(text):
    words = text.split()
    return sum(1 for word in words if word.isupper())

def vocabulary_richness(text):
    words = text.lower().split()
    unique_words = set(words)
    dw = len(unique_words)
    return dw

def number_of_urls(text):
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    return len(urls)

def flesch_kincaid_grade_level(text):
    return textstat.flesch_kincaid_grade(text)

def flesch_reading_ease(text):
    return textstat.flesch_reading_ease(text)

def dale_chall_readability(text):
    return textstat.dale_chall_readability_score(text)

def automated_readability_index(text):
    return textstat.automated_readability_index(text)

def coleman_liau_index(text):
    return textstat.coleman_liau_index(text)

def gunning_fog(text):
    return textstat.gunning_fog(text)

def smog_index(text):
    return textstat.smog_index(text)

def linsear_write_index(text):
    return textstat.linsear_write_formula(text)

import pandas as pd

FILENAME = "Synthetic User Stories.xlsx"
SHEETNAME = "Dataset"

metric_functions = [
    total_characters,
    uppercase_characters,
    lowercase_characters,
    special_characters,
    numbers,
    blanks,
    number_of_words,
    average_length_of_words,
    number_of_propositions,
    average_length_of_propositions,
    punctuation_characters,
    lowercase_words,
    uppercase_words,
    vocabulary_richness,
    number_of_urls,
    flesch_kincaid_grade_level,
    flesch_reading_ease,
    dale_chall_readability,
    automated_readability_index,
    coleman_liau_index,
    gunning_fog,
    smog_index,
    linsear_write_index
]

if __name__ == '__main__':
    df = pd.read_excel(FILENAME, SHEETNAME)
    df = df[:2]
    sentence = df['User Story'][1]
    print(sentence)

    for func in metric_functions:
        print(f"{func.__name__}: {func(sentence)}")
