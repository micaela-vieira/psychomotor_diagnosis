#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 16:57:55 2022

@author: micaelavieira
code written following https://www.sbert.net/docs/training/overview.html (retrieved on January 15 2022)
"""

from sentence_transformers import InputExample, losses, SentenceTransformer
from torch.utils.data import DataLoader

def get_train_examples(filename: str) -> list:
    """
    Purpose
    -------
    Extract from tsv file expert remarks, students remarks, and similarity ratings
    and store everything into a list of training examples.

    Parameters
    ----------
    filename : str
        Name of the tsv file.

    Returns
    -------
    list
        train_examples : list
        List containing the training examples.
    """
    train_examples = []
    last_expert_sentence = ''
    with open(filename, 'r') as infile:
        for line in infile:
            splitted_line = line.split('\t')
            if splitted_line[0] != '':
                last_expert_sentence = splitted_line[1]
            student_sentence = splitted_line[3]
            #try-except block to disregard elements without rating
            try:
                #to have a rating between 0 and 1, we divide it by the maximum possible value, i.e., 5
                rating = int(splitted_line[4].strip())/5
                single_example = InputExample(texts=[last_expert_sentence, student_sentence], label=rating)
                train_examples.append(single_example)
            except:
                pass
    return train_examples
           
def main():
    model = SentenceTransformer('gbert-large')
    train_ex = get_train_examples('AnamBeob_Ratings.tsv')
    train_dataloader = DataLoader(train_ex, shuffle=True, batch_size=4)
    train_loss = losses.CosineSimilarityLoss(model)
    model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=1, warmup_steps=20)

if __name__ == '__main__':
    main()


