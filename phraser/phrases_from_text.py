""" phrases_from_text.py """

import pickle
import pandas as pd
from phraser.futils import merge_lists
from collections import Counter

class PhrasesFromText:
    """ PhrasesFromText """
    def __init__(self):
        self.phraser_model = None
        self.skill_set = set()
        self.path_to_skillset = \
            'phraser/data/skill_clusters_km_1000_r2_Cleaned.csv'
        self.load_skillset()
        # self.path_to_phraser_model = \
        #     "phraser/data/phraser_good_split_phraser.pickle"
        self.path_to_phraser_model = \
            "phraser/data/PhraserModel_HTML_Feb16_small.pickle"

        self.load_phraser_model()

    def load_phraser_model(self):
        """ load_phraser_model """
        with open(self.path_to_phraser_model, 'rb') as file_path:
            self.phraser_model = pickle.load(file_path)

    def load_skillset(self):
        """ load_skillset """
        skill_set = pd.read_csv(self.path_to_skillset)
        self.skill_set = set(skill_set['Skill'])

    def phrase_from_text(self, cleaned_tokens_lol, mode, opt_in):
        """ phrase_from_text """
        phraser_on_sents = []
        for sent in cleaned_tokens_lol:
            phraser_on_sents.append(self.phraser_model[sent])

        job_tokens = merge_lists(phraser_on_sents)
        # greedy phrases
        matched_word_phrases = self.greedy(
            job_tokens, mode=mode, opt_in=opt_in)

        # remove duplicates
        matched_word_phrases = dict(Counter(list(matched_word_phrases)))
        
        return matched_word_phrases

    def greedy(self, arr, mode, opt_in=False):
        """ takes in list of tokens and returns greedy matched word phrases """
        greedy_match = []
        i = 0
        while i < len(arr):
            pr, i = self.match(arr, i, mode, opt_in)
            if pr:
                greedy_match.append(pr)
        return greedy_match

    def match(self, arr, start, mode, opt_in):
        key = arr[start]
        while True:
            try:
                if key+'_'+arr[start+1] in self.skill_set:
                    start = start+1
                    key = key+'_'+arr[start]
                else:
                    break
            except:
                break

        if mode == 'match':
            return key, start+1

        if mode == 'filter':
            if key in self.skill_set or ((opt_in) and ('_' in key)):
                return key, start+1
            else:
                return None, start+1
        
