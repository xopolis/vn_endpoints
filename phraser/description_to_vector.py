""" description_to_vector.py """

from collections import Counter
import pandas as pd
import numpy as np


class DescriptionToVector:
    """ desc,extended_skill_set,mode """
    def __init__(self):
        # wv_model and cluster_means are both set to empty string
        # this process looks unfinished
        self.wv_model = ""
        self.cluster_means = ""
        self.extended_skill_set = None
        self.extended_skill_dict = None

    def desc2vec(self, phrases):
        """ desc2vec """
        if any(v is None for v in [
                self.wv_model, self.cluster_means,
                self.extended_skill_set, self.extended_skill_dict]):
            print("variable got none in desc2vec")
            raise

        # make phrsase list to a pandas df
        tokens = pd.DataFrame(
            Counter(phrases).items(),
            columns=['word', 'count']
        )

        # filter only vocabulary present in extended skill set
        tokens_in_vocab = tokens[tokens['word'].isin(self.extended_skill_set)]

        # map each skill to apprropriate cluster label
        tokens_in_vocab['mapped_cluster'] = tokens_in_vocab['word'].map(
            self.extended_skill_dict
        )

        # find words not present in skill list and try to
        # assign a nearest cluster
        tokens_outof_vocab = tokens[~tokens['word'].isin(
            self.extended_skill_set
        )]
        if not tokens_outof_vocab.empty:
            wv_matrix = self.wv_outof_vocab(tokens_outof_vocab['word'])
            token_dotproduct = self.cluster_means.dot(wv_matrix)
            best_cluster = token_dotproduct.idxmax(skipna=False)
            tokens_outof_vocab['mapped_cluster'] = best_cluster.values

        # combine both word clusters
        tokens = pd.concat([tokens_in_vocab, tokens_outof_vocab], sort=False)

        # find final count of cluster groups
        cummulative_best_clusters = tokens.groupby(
            'mapped_cluster'
        )['count'].sum()
        dimension_vector = dict(cummulative_best_clusters)
        return dimension_vector

    def wv_outof_vocab(self, tokens):
        """ wv_outof_vocab """
        wv_matrix = []
        try:
            for word in tokens:
                try:
                    wv_matrix.append(self.wv_model.wv[word])
                except:
                    wv_matrix.append(np.zeros(300))
            return np.array(wv_matrix).T
        except:
            wv_matrix.append(np.zeros(300))
            return np.array(wv_matrix).T
