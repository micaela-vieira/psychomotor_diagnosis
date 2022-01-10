#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 09:42:58 2021

@author: micaelavieira
"""

import enchant
german_dictionary = enchant.Dict("de_DE")
import pandas as pd
from spellchecker import SpellChecker
german_spellchecker = SpellChecker(language='de')
import splitter
import string

def token_preprocessing(token: str) -> str:
    """
    Purpose
    -------
    If token is neither in the German dictionary, nor a compound of subtokens present
    in the German dictionary, substitute the initial token with the closest one
    according to the Levenshtein distance (default distance of 2).

    Parameters
    ----------
    token : str
        Token to preprocess.

    Returns
    -------
    output_token : str
        Preprocessed token.
    """
    #if token is in dictionary, we are fine
    if german_dictionary.check(token):
        output_token = token
    #otherwise 
    else:
        #if the token is a compound and all elements of it are in the dictionary, we are fine
        compounds = splitter.split(token, 'de_de')
        if len(compounds) > 0 and all(german_dictionary.check(i) for i in compounds):
            output_token = token
        #otherwise try to fix the typo using the Levenshtein distance
        else:
            output_token = german_spellchecker.correction(token)
    return output_token

def sentence_preprocessing(sentence: str, subcategory: str, abbreviation_list: list, substitution_name: str) -> str:
    """
    Purpose
    -------
    Preprocess a sentence.

    Parameters
    ----------
    sentence : str
        Sentence to preprocess.
    subcategory : str
        Subcategory to which the sentence belong (beobachtungen, herausforderungen, or ressourcen).
    abbreviation_list : list
        List of abbreviations to keep unchanged.
    substitution_name : str
        Name to use to substitute the initial character of the real name of the patient.

    Returns
    -------
    preprocessed_sentence : str
        Preprocessed sentence.
    """
    #replace ’ with '
    sentence = sentence.replace("’", "'")
    splitted_sentence = sentence.split()
    #remove labels that an expert put at the beginning of its sentences
    if subcategory == 'herausforderungen':
            if splitted_sentence[0] in ['P.', 'P:']:
                splitted_sentence.pop(0)
    elif subcategory == 'ressourcen':
            if splitted_sentence[0] in ['R.', 'R:']:
                splitted_sentence.pop(0)
    token_index = 0
    for token in splitted_sentence:
        #substitute Th. or Th.: to Therapeut
        if token in ['Th.', 'Th.:']:
            splitted_sentence[token_index] = 'Therapeut'
        #substitute initial character of the real name of the patient
        #substitute single uppercase characters (e.g., C)
        elif len(token) == 1 and token.isalpha() and token.isupper():
            splitted_sentence[token_index] = substitution_name
        #substitute uppercase characters with punctuation (e.g., C.)
        elif len(token) == 2 and token[0].isupper() and token[1] in string.punctuation and token not in abbreviation_list:
            splitted_sentence[token_index] = substitution_name
        #substitute uppercase characters with punctuation and s (e.g., C's)
        elif len(token) == 3 and token[0].isupper() and token[1] in string.punctuation and token not in abbreviation_list:
            splitted_sentence[token_index] = substitution_name + "'s"
        #substitute uppercase characters with point, punctuation and s (e.g., C.'s)
        elif len(token) == 4 and token[0].isupper() and token[1] == '.' and token[2] in string.punctuation and token not in abbreviation_list:
            splitted_sentence[token_index] = substitution_name + "'s"
        #substitute typos
        elif token not in abbreviation_list and token.isalpha():
            correct_token = token_preprocessing(token)
            splitted_sentence[token_index] = correct_token
        token_index += 1
    preprocessed_sentence = ' '.join(splitted_sentence)
    return preprocessed_sentence

def get_expert_statements_and_categories(category: str, subcategory: str, abbreviation_list: list, substitution_name: str) -> tuple[list, list]:
    """
    Purpose
    -------
    Extract from a file the experts statements and corresponding categories, preprocess the former and return a list.

    Parameters
    ----------
    category : str
        Category we are interested in (either anamnese or spielsituation).
    subcategory : str
        Subcategory we are interested in (beobachtungen, herausforderungen, or ressourcen).
    abbreviation_list : list
        List of abbreviations to keep unchanged during preprocessing.
    substitution_name : str
        Name to use to substitute the initial character of the real name of the patient.

    Returns
    -------
    expert_sentences : list
        List containing the preprocessed experts statements.
    expert_categories : list
        List containing the categories of the extracted sentences.
    
    """
    filename = 'experts/' + category + '_' + subcategory + '.tsv'
    expert_data = pd.read_csv(filename, sep='\t', header=None, names=['expert_ID', 'statement', 'category_ID', 'category_main', 'category_sub'], encoding='utf-8')
    expert_categories = expert_data['category_main'].tolist()
    extracted_sentences = expert_data['statement'].tolist()
    #preprocessing
    expert_sentences = []
    for sent in extracted_sentences:
        expert_sentences.append(sentence_preprocessing(sent, subcategory, abbreviation_list, substitution_name))
    return expert_sentences, expert_categories

def get_student_statements(filename: str, subcategory: str, abbreviation_list: list, substitution_name: str) -> list:
    """
    Purpose
    -------
    Extract from a file the student statements, preprocess them and return a list.

    Parameters
    ----------
    filename : str
        Name of the file containing the student sentences.
    subcategory : str
        Subcategory we are interested in (beobachtungen, herausforderungen, or ressourcen).
    abbreviation_list : list
        List of abbreviations to keep unchanged during preprocessing.
    substitution_name : str
        Name to use to substitute the initial character of the real name of the patient.

    Returns
    -------
    student_sentences : list
        List containing the preprocessed student statements.
    """
    student_data = pd.read_csv(filename, sep='\t', header=None, names=['beobachtungen', 'herausforderungen', 'ressourcen', 'other'], encoding='utf-8')
    extracted_sentences = student_data[subcategory].tolist()
    #remove empty cells
    extracted_sentences = [sent for sent in extracted_sentences if sent == sent]
    #preprocessing
    student_sentences = []
    for sent in extracted_sentences:
        student_sentences.append(sentence_preprocessing(sent, subcategory, abbreviation_list, substitution_name))
    return student_sentences