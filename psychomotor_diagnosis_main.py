#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 11:40:37 2021

@author: micaelavieira
"""

"""
Code to perform computer-aided exercises in psychomotor diagnosis.
"""

import argparse
from preprocessing import get_expert_statements_and_categories, get_student_statements
import numpy as np

#define parser
parser = argparse.ArgumentParser(description='Main code for computer-aided exercises in psychomotor diagnosis.')
parser.add_argument('-A', '--algorithm', choices=['sentencebert', 'doc2vec', 'infersent'], nargs='?', default='sentencebert', help='Algorithm to use (default: sentencebert)')
parser.add_argument('-c', '--category', choices=['anamnese', 'spielsituation'], nargs='?', default='anamnese', help='Category to look at (default: anamnese)')
parser.add_argument('-s', '--subcategory', choices=['beobachtungen', 'herausforderungen', 'ressourcen'], nargs='?', default='beobachtungen', help='Subcategory to look at (default: beobachtungen)')
parser.add_argument('-a', '--abbreviations', default='["d.h.", "s.a.", "u.a.", "z.B."]', help='List of abbreviations not to preprocess (default: ["d.h.", "s.a.", "u.a.", "z.B."])')
parser.add_argument('-p', '--patient', default='Andreas', help='Patient name (default: Andreas)')
group = parser.add_mutually_exclusive_group()
group.add_argument('-f', '--filename_student', help='Filename containing the student answers')
group.add_argument('-w', '--write_sentence', action='store_true', help='Enter student answers directly in command line')
parser.add_argument('-o', '--outfile', action='store_true', help='Store scores, most similar sentences, and sentences\' categories to file')
args = vars(parser.parse_args())

#import algorithm to calculate sentence similarity
algorithm_to_use = args['algorithm']
if algorithm_to_use == 'doc2vec':
    from doc2vec import doc2vec_score as algorithm
elif algorithm_to_use == 'sentencebert':
    from sentencebert import sentencebert_score as algorithm
elif algorithm_to_use == 'infersent':
    from infersent import infersent_score as algorithm

#get expert sentences and categories
category = args['category']
subcategory = args['subcategory']
abbreviations = args['abbreviations'].replace('"', '').replace('[', '').replace(']', '').split(', ')
patient_name = args['patient']
expert_sentences, expert_categories = get_expert_statements_and_categories(category, subcategory, abbreviations, patient_name)

#define threshold above which the most similar expert sentence is displayed by default
threshold = 0.9

#define dictionary to accomodate scores of most similar sentences divided for categories
categories_and_scores_most_similar_sentences = {}

#get student sentences if argument -f was chosen
if args['filename_student']:
    #create outfile if argument -o was chosen
    if args['outfile']:
        outname = args['filename_student'][:-4]+'_outfile.txt'
        with open(outname, 'w') as out:
            out.write('Student_sentence \t Similarity_score \t Most_sililar_sentence \t Category\n')
    student_sentences = get_student_statements(args['filename_student'], subcategory, abbreviations, patient_name)
    for sent in student_sentences:
        score_most_similar_sentence, most_similar_sentence, most_similar_sentence_category = algorithm(sent, expert_sentences, expert_categories)
        if most_similar_sentence_category in categories_and_scores_most_similar_sentences:
            categories_and_scores_most_similar_sentences[most_similar_sentence_category].append(score_most_similar_sentence)
        else:
            categories_and_scores_most_similar_sentences[most_similar_sentence_category] = [score_most_similar_sentence]
        #print result on screen depending on threshold
        if score_most_similar_sentence >= threshold:
            print(sent, '\t', score_most_similar_sentence, '\t', most_similar_sentence, '\n')
        else:
            print(sent, '\t', score_most_similar_sentence, '\n')
        #store results to outfile if argument -o was chosen
        if args['outfile']:
            with open(outname, 'a') as out:
                to_print = sent + '\t' + str(score_most_similar_sentence) + '\t' + most_similar_sentence + '\t' + most_similar_sentence_category + '\n'
                out.write(to_print)
#use student input from command line if argument -w was chosen
elif args['write_sentence']:
    #create outfile if argument -o was chosen
    if args['outfile']:
        outname = 'command_line_sentences_outfile.txt'
        with open(outname, 'w') as out:
            out.write('Student_sentence \t Similarity_score \t Most_sililar_sentence \t Category\n')
    while True:
        sent = input('Statement (write Stop to end the program):\t')
        if sent == 'Stop':
            break
        else:
            score_most_similar_sentence, most_similar_sentence, most_similar_sentence_category = algorithm(sent, expert_sentences, expert_categories)
            if most_similar_sentence_category in categories_and_scores_most_similar_sentences:
                categories_and_scores_most_similar_sentences[most_similar_sentence_category].append(score_most_similar_sentence)
            else:
                categories_and_scores_most_similar_sentences[most_similar_sentence_category] = [score_most_similar_sentence]
            #print result on screen depending on threshold
            if score_most_similar_sentence >= threshold:
                print(score_most_similar_sentence, '\t', most_similar_sentence, '\n')
            else:
                print(score_most_similar_sentence, '\n')
            #store results to outfile if argument -o was chosen
            if args['outfile']:
                with open(outname, 'a') as out:
                    to_print = sent + '\t' + str(score_most_similar_sentence) + '\t' + most_similar_sentence + '\t' + most_similar_sentence_category + '\n'
                    out.write(to_print)

print('\n\n***************************************************************************************')
print('FINAL REPORT')
print('***************************************************************************************')
print ("{:^30s} {:^30s} {:^30s}".format('CATEGORY', 'NR. ELEMENTS', 'AVERAGE'))
for key, value in categories_and_scores_most_similar_sentences.items():
    print ("{:^30s} {:^30s} {:^30s}".format(key, str(len(value)), str(round(np.average(value),3))))
print('***************************************************************************************')

