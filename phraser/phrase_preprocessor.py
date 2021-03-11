""" phrase_preprocessor.py """
import sys
sys.path.append('./phraser')
import time
from phraser.models import LoadModels
from phraser.phrases_from_text import PhrasesFromText
from phraser.description_to_vector import DescriptionToVector
from phraser.text_cleaner import TextCleaner
from phraser.filter_sents import FilterSents


class PhrasePreprocessor:
    """ PhrasePreprocessor """
    def __init__(self):
        self.text_cleaner = TextCleaner()
        self.pft = PhrasesFromText()
        self.models = LoadModels()

        self.filter_sents = FilterSents()
        self.filter_sents.nlp = self.models.nlp

        self.desc_vector = DescriptionToVector()
        self.desc_vector.extended_skill_set = self.models.extended_skill_set
        self.desc_vector.extended_skill_dict = self.models.extended_skill_dict

    def get_phrases(self, desc):
        """ get phrases description"""
        self.text_cleaner.camlecase_splitter(desc)
        self.text_cleaner.rem_unicode()
        self.text_cleaner.rem_punct()
        self.text_cleaner.rem_extra_space()
        self.text_cleaner.pattern_splitter()
        sent_tokens = self.filter_sents.filter_sents(
            self.text_cleaner.sents,
            has_stopwords=False,
            lemma=True
        )
        greed_tokens = self.pft.phrase_from_text(
            sent_tokens,
            mode='filter',
            opt_in=False
        )
        return greed_tokens

    def get_vector(self, phrases):
        """get vector from phrases"""
        vector_ = self.desc_vector.desc2vec(phrases)
        vector_ = {i: int(vector_[i]) for i in vector_}
        return vector_

    def get_metadata(self, raw_id, desc):
        """ get_metadata returns the phrases and vector as well as logs the
            time
        """
        tik = time.perf_counter()
        phrases_ = self.get_phrases(desc)
        vector_ = self.get_vector(phrases_)
        tok = time.perf_counter()
        print("{} took {}".format(raw_id, tok-tik))
        return phrases_, vector_

    def preprocess_resume(self, raw_id, work_experiences):
        """ preprocess_resume """
        works_preprocessed = []
        if work_experiences:
            for work in work_experiences:
                if 'description' not in work:
                    return {
                        'phrases': [],
                        'vector': {}
                    }
                phrases_, vector_ = self.get_metadata(raw_id, work['description'])
                work_prep = {
                    'phrases': phrases_,
                    'vector': vector_
                }
                works_preprocessed.append(work_prep)

        record = {
            'raw_id': raw_id,
            'work_experience': works_preprocessed
        }

        return record

    def preprocess_jobpost(self, raw_id, body):
        """ preprocess_jobpost """
        phrases_, vector_ = self.get_metadata(raw_id, body)

        record = {
            'job_post_id': raw_id,
            'phrases': phrases_,
            'job_vector': vector_
        }

        return record
