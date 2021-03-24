"""
Provides utilities for entity replacement, split texts sentences
"""
import itertools
import spacy
import json

class NERTextConversion:
    """
    input: "Salary: $43,000.00 to $48,000.00 /year"
    output: ['Salary', ':', '$', 'MONEY', 'to', '$' 'MONEY', '/year']
    """

    #load spacy language models
    nlp = spacy.load("en_core_web_lg",disable = ['textcat'])
    nlp.add_pipe("sentencizer", before='parser')
    
    assert nlp

    @staticmethod
    def convert_texts(texts):
        """convert texts to sentences"""
        nlp_sents = NERTextConversion.split_to_nlp_sents(texts)
        # transformed_sents = NERTextConversion.replace_ner_labels(nlp_sents)
        return [str(i) for i in nlp_sents]

    @staticmethod
    def convert_text(text):
        """convert texts to sentences"""
        texts = [text]
        return NERTextConversion.convert_texts(texts)

    @staticmethod
    def split_to_nlp_sents(elemental_texts):
        """convert text to nlp_sents"""
        docs = NERTextConversion.nlp.pipe(elemental_texts)
        nlp_sents = [list(doc.sents) for doc in docs]
        return list(itertools.chain.from_iterable(nlp_sents))

    @staticmethod
    def replace_ner_labels(nlp_sents):
        """replace noise NER phrases, MONEY, TIME, DATE, PERSON with labels in a sentence"""
        transformed_sents = []
        for sent in nlp_sents:
            prev = 0
            transformed_sent = []

            arr = [[(e.start,e.end),e.label_]
                        for e in sent.ents if e.label_ in ['MONEY','PERSON','TIME','DATE']]

            for position_tuple,label in arr:
                if position_tuple[0]>=prev:
                    for i in sent[prev:position_tuple[0]]:
                        transformed_sent.append(i.lemma_ if i.lemma_ != '-PRON-' else i.text)
                transformed_sent.append(label)
                prev = position_tuple[1]

            if prev<len(sent):
                for i in sent[prev:]:
                    transformed_sent.append(i.lemma_ if i.lemma_ != '-PRON-' else i.text)

            transformed_sents.append(transformed_sent)
        return transformed_sents
