import string
import re
from collections import Counter
import math

def total_characters(text):
    return len(text)

def uppercase_characters(text):
    return sum(1 for char in text if char.isupper())

def lowercase_characters(text):
    return sum(1 for char in text if char.islower())

def special_characters(text):  # to verify
    return sum(1 for char in text if not char.isalnum() and char != ' ')

def numbers(text):
    return sum(1 for char in text if char.isdigit())

def blanks(text): # to verify (maybe to use .isspace()?)
    return sum(1 for char in text if char == ' ')

def number_of_words(text): # what if (word - word)
    return len(text.split())

def average_length_of_words(text): # depends on the previous one
    words = text.split()
    if words:
        return sum(len(word) for word in words) / len(words)
    else:
        return 0

def number_of_propositions(text): # I think incorrect
    propositions = re.split(r'[.!?]+', text)
    return len([prop for prop in propositions if prop.strip()])

def average_length_of_propositions(text): # related to the previous one
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

def vocabulary_richness(text): # i guess all words should be converted to he lowercase
    words = text.split()
    return len(set(words))

def number_of_urls(text):
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    return len(urls)

# def flesch_kincaid_grade_level(avg_syllables_per_word, avg_words_per_prop):
#     return 0.39 * avg_words_per_prop + 11.8 * avg_syllables_per_word - 15.59

# def flesch_reading_ease(avg_syllables_per_word, avg_words_per_prop):
#     return 206.835 - (84.6 * avg_syllables_per_word) - (1.015 * avg_words_per_prop)

# def dale_chall_readability(difficult_words_percentage, avg_prop_length):
#     return 0.1579 * difficult_words_percentage + 0.0496 * avg_prop_length

# def automated_readability_index(total_words, total_characters, total_propositions):
#     return 4.71 * (total_characters / total_words) + 0.5 * (total_words / total_propositions) - 21.43

# def coleman_liau_index(avg_prop_per_100_words, avg_letters_per_100_words):
#     return 0.0588 * avg_letters_per_100_words - 0.296 * avg_prop_per_100_words - 15.8

# def gunning_fog(total_words, difficult_words, total_propositions):
#     return 0.4 * ((total_words / total_propositions) + 100 * (difficult_words / total_words))

# def smog_index(difficult_words, total_propositions):
#     return 1.0430 * math.sqrt((difficult_words * 30 / total_propositions)) + 3.1291

# def linsear_write_index(words_with_two_or_less_syllables, words_with_more_than_three_syllables, total_propositions):
#     lw = (words_with_two_or_less_syllables + 3 * words_with_more_than_three_syllables) / total_propositions
#     return lw / 2 if lw > 20 else (lw - 1) / 2

# Example usage:
# text = "Hello - my friend"
# total_chars = total_characters(text)
# upper_chars = uppercase_characters(text)
# lower_chars = lowercase_characters(text)
# special_chars = special_characters(text)
# nums = numbers(text)
# blanks_count = blanks(text)
# words_count = number_of_words(text)
# avg_word_length = average_length_of_words(text)
# prop_count = number_of_propositions(text)
# avg_prop_length = average_length_of_propositions(text)
# punctuation_chars = punctuation_characters(text)
# lowercase_words_count = lowercase_words(text)
# uppercase_words_count = uppercase_words(text)
# vocab_richness = vocabulary_richness(text)
# urls_count = number_of_urls(text)

# print("Total Characters:", total_chars)
# print("Uppercase Characters:", upper_chars)
# print("Lowercase Characters:", lower_chars)
# print("Special Characters:", special_chars)
# print("Numbers:", nums)
# print("Blanks:", blanks_count)
# print("Words:", words_count)
# print("Average Word Length:", avg_word_length)
# print("Propositions:", prop_count)
# print("Average Proposition Length:", avg_prop_length)
# print("Punctuation Characters:", punctuation_chars)
# print("Lowercase Words:", lowercase_words_count)
# print("Uppercase Words:", uppercase_words_count)
# print("Vocabulary Richness:", vocab_richness)
# print("URLs:", urls_count)
