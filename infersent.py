#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 13:52:19 2021

@author: micaelavieira
"""

from deep_translator import GoogleTranslator
from infersent_data.models import InferSent
from sklearn.metrics.pairwise import cosine_similarity
import torch
from typing import Tuple

#load model and word embeddings
V = 2
MODEL_PATH = 'infersent_data/infersent%s.pkl' % V
params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048,
                'pool_type': 'max', 'dpout_model': 0.0, 'version': V}
infersent = InferSent(params_model)
infersent.load_state_dict(torch.load(MODEL_PATH))
W2V_PATH = 'infersent_data/glove.840B.300d.txt'
infersent.set_w2v_path(W2V_PATH)

def infersent_score(single_sentence: str, list_of_sentences: list, list_of_categories: list) -> Tuple[float, str, str]:
    """
    Purpose
    -------
    Find the most similar sentence to a target sentence with the infersent method. Return the similarity score.

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
    #translate sentences to english
    translated_sentences = [GoogleTranslator(source='auto', target='en').translate(sent) for sent in list_of_sentences]
    infersent.build_vocab(list_of_sentences, tokenize=True)
    vectorised_single_sentence = infersent.encode(GoogleTranslator(source='auto', target='en').translate(single_sentence))[0]
    score_most_similar_sentence = 0
    best_index = 0
    sentence_index = 0
    for sentence in translated_sentences:
        vectorised_sentence = infersent.encode([sentence])[0]
        similarity = cosine_similarity([vectorised_single_sentence], [vectorised_sentence])[0][0]
        if similarity > score_most_similar_sentence:
            score_most_similar_sentence = similarity
            best_index = sentence_index
        sentence_index += 1
    score_most_similar_sentence = round(score_most_similar_sentence, 2)
    most_similar_sentence = list_of_sentences[best_index]
    most_similar_sentence_category = list_of_categories[best_index]
    return score_most_similar_sentence, most_similar_sentence, most_similar_sentence_category