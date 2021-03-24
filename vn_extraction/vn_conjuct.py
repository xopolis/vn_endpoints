"""
This module contains functions to extract verb noun pairs from various formats
like text, indeed-html, spacy-doc objects.

Define and find verb phrase and noun phrase with Matcher
"""

import re
from spacy.matcher import Matcher
from spacy.util import filter_spans
from collections import defaultdict
import itertools
from vn_extraction.ner_text_tokeniser import  NERTextConversion

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
        nlp_doc = NERTextConversion.nlp(text)
        return VerbNounPairExtractor.vn_doc(nlp_doc)

    @staticmethod
    def vn_doc(doc):
        """vn pairs form single doc"""
        verb_indexs = VerbNounPairExtractor.construct_verb_indexs(doc)
        noun_indexs = VerbNounPairExtractor.construct_noun_indexs(doc)
        return VerbNounPairExtractor.extract_verb_noun_pairs_from_doc(doc, verb_indexs, noun_indexs)

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
        if token_.pos_ == 'VERB' and token.dep_ in VerbNounPairExtractor.vn_dep_valid_path and (not token_.conjuncts):
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



subject_clause = "he should "

class ConjugateSearch:
    def __init__(self, sentence):
        self.conjugate_dict = defaultdict(list)
        self.visited_nodes = set()
        self.doc = NERTextConversion.nlp(sentence)
        self.conj_clusters = None
        self.verb_clusters = None
        self.vns2 = None
        self.unfolded_sents = None

    def drive_execute_return(self):
        self.find_conjugate(self.doc[:].root)
        self.rectify()
        self.identify_verb_clusters(bypass=False)
        if len(self.verb_clusters)>0:            
            self.unfold_sents()
            self.extract_vn_from_unfolded()
            return self.vns2
        else:
            if 'nsubj' not in set(token.dep_ for token in self.doc):
                text_ = subject_clause+self.doc.text.strip()
                return VerbNounPairExtractor.vn_text(text_)
            else:
                return VerbNounPairExtractor.vn_doc(self.doc)

    def find_conjugate(self, root, index=-1):
        if not root:
            return
        if root.i not in self.visited_nodes:
            self.visited_nodes.add(root.i)
            for child in root.children:
                if child.dep_ == 'conj':
                    if index == -1:
                        index = root.i
                    self.conjugate_dict[index].append(child.i)
                    self.find_conjugate(child, index)
                else:
                    self.find_conjugate(child, index=-1)
    def rectify(self):
        conj_clusters = []
        for key in self.conjugate_dict:
            indices = [key]+self.conjugate_dict[key]
            conj_clusters.append(indices)
        self.conj_clusters = conj_clusters


    def identify_verb_clusters(self, bypass=False):
        if bypass:
            self.verb_clusters = self.conj_clusters
            return

        verb_clusters = []
        for cluster in self.conj_clusters:
            for i in cluster:
                if self.doc[i].pos_ == 'VERB':
                    verb_clusters.append(cluster)

        # remove duplicates
        verb_clusters =list(k for k,_ in itertools.groupby(verb_clusters))
        self.verb_clusters = verb_clusters
        if len(self.verb_clusters) == 0:
            print("No conjugate verbs found")

    def unfold_sents(self):
        unfolded_sents = []
        for vc in self.verb_clusters:
            min_ind = min(vc)
            max_ind = max(vc)
            for ind in vc:
                text2 = self.doc[:min_ind].text +' '+ self.doc[ind].text +' '+self.doc[max_ind+1:].text
                unfolded_sents.append(text2.strip())
        self.unfolded_sents = unfolded_sents

    def extract_vn_from_unfolded(self):
        vns_list = []
        for text in self.unfolded_sents:
            doc = NERTextConversion.nlp(text)
            if 'nsubj' not in set(token.dep_ for token in doc):
                text_ = subject_clause+text.strip()
                vns = VerbNounPairExtractor.vn_text(text_)
            else:
                vns = VerbNounPairExtractor.vn_doc(doc)
            vns_list.append(vns)

        # generate vns from multiple sents
        vns2 = list(itertools.chain.from_iterable(vns_list))
        # deduplicate multiple vnpairs
        vns2 = [dict(t) for t in {tuple(d.items()) for d in vns2}]
        self.vns2 = vns2