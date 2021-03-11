""" filter_sents.py """


class FilterSents:
    """ FilterSents """
    def __init__(self):
        self.nlp = None
        self.cleaned_sents_tokens = []
        self.stopwords = []
        self.path_to_stopwords = 'phraser/data/stopwords_v2.csv'
        self.load_stopwords()

    def load_stopwords(self):
        """ load_stopwords """
        with open(self.path_to_stopwords) as file_path:
            data = file_path.read().split('\n')
            self.stopwords = set(data)
            self.stopwords.update([','])

    def filter_sents(self, sents, lemma=True, has_stopwords=False):
        """ filter_sents """
        # alway start with empty list
        cleaned_sents_tokens = []
        if self.nlp is None:
            print('nlp model missing')
            raise
        if lemma:
            docs = self.nlp.pipe(sents)
            # just lemmatize inluding stopwords
            if has_stopwords:
                _ = [cleaned_sents_tokens.append([token.lemma_ for token in doc]) for doc in docs]
            # lemmatize and remove stopwords
            else:
                for _doc in docs:
                    _ = [cleaned_sents_tokens.append([token.lemma_ for token in doc if token.text not in self.stopwords]) for doc in docs]
        else:
            # just tokenisation
            if has_stopwords:
                _ = [cleaned_sents_tokens.append([token for token in sent.split()]) for sent in sents]
            # removing stopwords
            else:
                _ = [cleaned_sents_tokens.append([token for token in sent.split() if token not in self.stopwords]) for sent in sents]
        return cleaned_sents_tokens
