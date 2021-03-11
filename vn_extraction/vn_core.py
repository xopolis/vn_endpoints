"""
This module contains functions to extract verb noun pairs from various formats
like text, indeed-html, spacy-doc objects.

Define and find verb phrase and noun phrase with Matcher
"""

import re
from spacy.matcher import Matcher
from spacy.util import filter_spans
from vn_extraction.indeed_html_processer import ProcessIndeedHTML
from vn_extraction.ner_text_tokeniser import NERTextConversion

class VerbNounPairExtractor:
    """define verb phrases"""

    # pattern for identification of verb-phrase
    verb_phrase_pattern = [
        [{'POS': {'IN':['ADV']}, 'OP':'?'}],
        [{'POS': 'VERB'}],
    ]
    verb_matcher = Matcher(NERTextConversion.nlp.vocab)
    verb_matcher.add("Verb phrase", verb_phrase_pattern)
    # valid dependency path connecting verb and noun
    vn_dep_valid_path = set(
    ['pobj', 'dobj', 'conj', 'prep', 'advmod', 'xcomp', 'nsubjpass', 'nsubj', 'ccomp']
    )

    # canditate for forming pairs, verb-noun, verb-adjective, verb-proper_noun
    valid_noun_forms  = set(['NOUN'])

    # stop if a prohibited token is present in dependency vn path
    prohibited_tokens = set(['with', 'in','of', 'on', 'at', 'to', 'for']) # & set()

    @staticmethod
    def vn_html(html):
        """vn pairs from indeed html"""
        verb_noun_pairs = []
        html_sents = VerbNounPairExtractor.process_html(html)
        for html_sent in html_sents:
            html_sent_ = html_sent.as_doc()
            noun_indexs = VerbNounPairExtractor.construct_noun_indexs(html_sent_)
            verb_indexs = VerbNounPairExtractor.construct_verb_indexs(html_sent_)
            vns_= VerbNounPairExtractor\
                .extract_verb_noun_pairs_from_doc(html_sent_, verb_indexs, noun_indexs)
            verb_noun_pairs.extend(vns_)
        return verb_noun_pairs

    @staticmethod
    def clean_text(text):
        """cleans text"""
        text=re.sub(r'\\u[0-9a-z]{4}', '-', text)
        text=re.sub(r'\\', ' ', text)
        return text

    @staticmethod
    def clean_texts(texts):
        """clean multiple texts"""
        texts = [VerbNounPairExtractor.clean_text(text_) for text_ in texts]
        return texts

    @staticmethod
    def vn_text(text):
        """vn pairs from a text"""
        text = VerbNounPairExtractor.clean_text(text)
        nlp_docs = NERTextConversion.split_to_nlp_sents([text])
        return VerbNounPairExtractor.vn_docs(nlp_docs)

    @staticmethod
    def vn_texts(texts):
        """vn pairs from a text"""
        texts = VerbNounPairExtractor.clean_texts(texts)
        return VerbNounPairExtractor.vn_docs(NERTextConversion.split_to_nlp_sents(texts))

    @staticmethod
    def vn_doc(doc_span):
        """vn pairs form single doc"""
        doc = doc_span.as_doc()
        verb_indexs = VerbNounPairExtractor.construct_verb_indexs(doc)
        noun_indexs = VerbNounPairExtractor.construct_noun_indexs(doc)
        return VerbNounPairExtractor.extract_verb_noun_pairs_from_doc(doc, verb_indexs, noun_indexs)

    @staticmethod
    def vn_docs(doc_sents):
        """vn pairs from list of nlp sents"""
        verb_noun_pairs = []
        for doc_sent in doc_sents:
            vns_ = VerbNounPairExtractor.vn_doc(doc_sent)
            verb_noun_pairs.extend(vns_)
        return verb_noun_pairs

    @staticmethod
    def process_html(html):
        """html to nlp sents"""
        html_tag_texts = ProcessIndeedHTML.get_content(html)
        html_tag_texts = VerbNounPairExtractor.clean_texts(html_tag_texts)
        html_nlp_sents = NERTextConversion.split_to_nlp_sents(html_tag_texts)
        return html_nlp_sents

    @staticmethod
    def construct_verb_indexs(doc):
        '''verb phrase indexs in doc'''
        verb_matches = VerbNounPairExtractor.verb_matcher(doc)
        spans = [doc[start:end] for _, start, end in verb_matches]
        filtered_verb_phrases = filter_spans(spans)

        verb_chunk_token_indices = [[token.i for token in vp] for vp in filtered_verb_phrases]
        # print(verb_chunk_token_indices)

        verb_indexes_dict = {}
        for vp_idxs_i in  verb_chunk_token_indices:
            for i in vp_idxs_i:
                if doc[i].pos_ == 'VERB':
                    verb_indexes_dict[i] = vp_idxs_i
        return verb_indexes_dict

    @staticmethod
    def construct_noun_indexs(doc):
        '''noun phrase index in doc'''
        noun_indexes_dict = {
            nc.root.i:
                [token.i for token in nc if token.lemma_ != '-PRON-'] for nc in doc.noun_chunks\
            if nc.root.pos_ in VerbNounPairExtractor.valid_noun_forms
        }
        # print(noun_indexes_dict)
        return noun_indexes_dict

    @staticmethod
    def extract_verb_noun_pairs_from_doc(doc, verb_indexes_dict, noun_indexes_dict):
        """extract verb pair and noun pair form doc"""
        verb_noun_pairs = []
        sent_root_index = doc[:].root.i
        for token in doc:
            if (token.pos_ in VerbNounPairExtractor.valid_noun_forms)\
                and (token.i in noun_indexes_dict):
                token_prev = token
                token_ = token.head

                while (token.i != sent_root_index) and\
                        (token_.i != sent_root_index) and\
                        (token_.pos_ != 'VERB') and\
                        (token_prev.dep_ in VerbNounPairExtractor.vn_dep_valid_path) and\
                        (token_.lemma_ not in VerbNounPairExtractor.prohibited_tokens):
                    token_prev = token_
                    token_ = token_.head

                verb_noun_pairs_ = VerbNounPairExtractor.evaluate_verb_noun_phrases(
                                        doc, token, token_, verb_indexes_dict, noun_indexes_dict
                                    )

                if verb_noun_pairs_:
                    verb_noun_pairs.append(verb_noun_pairs_)
                    del token_prev
                else:
                    continue
        return verb_noun_pairs

    @staticmethod
    def evaluate_verb_noun_phrases(
        doc,
        token,
        token_,
        verb_indexes_dict,
        noun_indexes_dict
        ):
        """Helper funtion to find the verb phrses and noun phrases"""
        if token_.pos_ == 'VERB' and token.dep_ in VerbNounPairExtractor.vn_dep_valid_path:
            noun = token
            noun_phrase = token
            if token.i in noun_indexes_dict:
                ids = noun_indexes_dict[token.i]
                noun_phrase = doc[ids[0]:ids[-1]+1]
                del ids

            verb = token_
            verb_phrase = token_
            if token_.i in verb_indexes_dict:
                ids = verb_indexes_dict[token_.i]
                verb_phrase = doc[ids[0]:ids[-1]+1]
                del ids

            verb_noun_pairs_ = {
                'verb_phrase':verb_phrase.lemma_,
                'noun_phrase':noun_phrase.lemma_,
                'verb':verb.lemma_,
                'noun':noun.lemma_,
                }
            return verb_noun_pairs_
        return None
