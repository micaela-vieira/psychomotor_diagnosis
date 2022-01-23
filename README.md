# Computer-assisted training software for psychomotor diagnostics

## Abstract
*Context:* As in any other area of medicine, diagnoses play a fundamental role also in psychomotricity. In fact, only with a correct diagnosis it is possible to provide an adequate therapy to patients. Diagnostic is a skill that is refined with practice. Between 2014 and 2016, the Institute of Computational Linguistics at the University of Zurich and the Interkantonale Hochschule für Heilpädagogik carried out a project aimed at creating a software that would give psychomotor students the possibility to practice their diagnostic skills autonomously. This software, in German language, did not reach a development stage suitable for practical use.

*Aims:* Using the Python programming language, we resume the initial project by integrating new features and implementing state-of-the-art techniques.

*Results:* We created a code that uses semantic similarity to quantify how close the remarks of a student's diagnosis are to those of experts' diagnoses. Semantic similarity is built on top of sentence embeddings. We implemented three algorithms to embed remarks: doc2vec, SentenceBERT and InferSent. It is found that SentenceBERT performs best. We also made some preprocessing steps on the remarks. There are still caveats which are mainly due to the language of the project. In particular, a German model for contextual spelling correction is missing. Nevertheless, this work can surely be the starting point for the creation of a highly-performant real-world interface.
