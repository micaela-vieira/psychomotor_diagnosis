#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 12:17:30 2021

@author: micaelavieira
"""

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
#import nltk
#nltk.download('punkt')
from typing import Tuple

def doc2vec_score(single_sentence: str, list_of_sentences: list, list_of_categories: list) -> Tuple[float, str, str]:
    """
    Purpose
    -------
    Find the most similar sentence to a target sentence with the doc2vec method. Return the similarity score.

    Parameters
    ----------
    single_sentence : str
        Target sentence.
    list_of_sentences : list
        List containing sentences as strings among which to find the most similar to single_sentence.
    list_of_categories : list
        List containing categories of the sentences in list_of_sentences.

    Returns
    -------
    score_most_similar_sentence : float
        Score between single_sentence and the sentences with the highest similarity in list_of_sentences.
    most_similar_sentence : str
        Sentence in list_of_sentences with the highest similarity to single_sentence.
    most_similar_sentence_category : str
        Category of the most_similar_sentence.
    """
    tokenized_lowecase_sentences = [word_tokenize(sentence.lower()) for sentence in list_of_sentences]
    model = Doc2Vec([TaggedDocument(d, [i]) for i, d in enumerate(tokenized_lowecase_sentences)], 
                    vector_size = 20, window = 4, min_count = 1, epochs = 100)
    vectorised_sentence = model.infer_vector(word_tokenize(single_sentence.lower()))
    score_most_similar_sentence = round(model.dv.most_similar(positive = [vectorised_sentence])[0][1], 2)
    index_most_similar_sentence = model.dv.most_similar(positive = [vectorised_sentence])[0][0]
    most_similar_sentence = list_of_sentences[index_most_similar_sentence]
    most_similar_sentence_category = list_of_categories[index_most_similar_sentence]
    return score_most_similar_sentence, most_similar_sentence, most_similar_sentence_category