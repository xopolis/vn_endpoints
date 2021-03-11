""" models.py loads all our files and models into memory """

import pickle
import spacy
import pandas as pd


class LoadModels:
    """ LoadModels """
    def __init__(self):
        self.path_to_wv_model = \
            "./phraser/data/wv_model_improved_phraser_large2.pickle"
        self.path_to_extended_skill_list = \
            "./phraser/data/skill_clusters_km_1000_r2_Cleaned.csv"
        self.path_to_cluster_means = \
            './phraser/data/cluster_means_km_1000_r2.csv'
        self.extended_skill_set = None
        self.extended_skill_dict = None
        self.wv_model = None
        self.cluster_means = None
        self.nlp = None
        self.load_cluster_means()
        self.load_extended_skill_set()
        self.load_nlp()

    def load_wv_model(self):
        """ load_wv_model """
        with open(self.path_to_wv_model, 'rb') as file_path:
            wv_model = pickle.load(file_path)
            self.wv_model = wv_model

    def load_extended_skill_set(self):
        """ load_extended_skill_set """
        extended_skill_df = pd.read_csv(self.path_to_extended_skill_list)
        self.extended_skill_set = set(extended_skill_df['Skill'])
        self.extended_skill_dict = dict(
            zip(extended_skill_df['Skill'], extended_skill_df['Cluster'])
        )

    def load_cluster_means(self):
        """ load_cluster_means """
        cluster_means = pd.read_csv(self.path_to_cluster_means)
        self.cluster_means = cluster_means.set_index('Cluster')

    def load_nlp(self):
        """ load_nlp """
        self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
