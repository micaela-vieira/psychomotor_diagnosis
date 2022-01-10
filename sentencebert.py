#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 12:18:36 2021

@author: micaelavieira
"""

import numpy as np
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('gbert-large')
from sklearn.metrics.pairwise import cosine_similarity
from typing import Tuple

def sentencebert_score(single_sentence: str, list_of_sentences: list, list_of_categories: list) -> Tuple[float, str, str]:
    """
    Purpose
    -------
    Find the most similar sentence to a target sentence with the sentenceBERT method. Return the similarity score.

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
    sentences_embeddings = model.encode(list_of_sentences)
    encoded_sentence = model.encode([single_sentence])
    score_most_similar_sentence = max(cosine_similarity(encoded_sentence, sentences_embeddings)[0])
    index_most_similar_sentence = np.where(cosine_similarity(encoded_sentence, sentences_embeddings)[0] == score_most_similar_sentence)[0][0]
    most_similar_sentence = list_of_sentences[index_most_similar_sentence]
    score_most_similar_sentence = round(score_most_similar_sentence, 2)
    most_similar_sentence_category = list_of_categories[index_most_similar_sentence]
    return score_most_similar_sentence, most_similar_sentence, most_similar_sentence_category