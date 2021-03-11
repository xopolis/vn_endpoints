""" text_cleaner.py transforms text for easier processing """

import re


class TextCleaner:
    """ add english contractions, clean numericals of
        "abbrevations", "salary",
        "years of experience",
        "zipcode", "timeshifts"(6.pm to 1am)
    """
    def __init__(self):
        self.split_pattern = re.compile(r'[!\*\.\n;]')
        self.punct_pattern = r"[\"#$%&'()\+\-/:<=>?@\[\]\\^`{|}~]"
        self.cleaned_text = None
        self.text = None
        self.sents = None

    def camlecase_splitter(self, text):
        """ seperate comnied words
            AaaaBbbb -> [Aaaa,Bbbb] but ignore Abbrevation ABC -> ABC
        """
        self.cleaned_text = re.sub(
            r'((?<=[a-z])[A-Z]|[A-Z](?=[a-z]))',
            r' \1',
            text
        )

    def rem_unicode(self):
        """ rem_unicode remove unicode values from text"""
        self.cleaned_text = self.cleaned_text.encode(
            'ascii',
            'ignore'
        ).decode('utf-8')

    def to_lower(self):
        """ to_lower down cases text """
        self.cleaned_text = self.cleaned_text.lower()

    def rem_punct(self):
        """ remove PUNCTUATION and Numbers """
        self.cleaned_text = re.sub(self.punct_pattern, ' ', self.cleaned_text)

    def rem_extra_space(self):
        """ replace MULTI spaces/newline/tab with a single space """
        self.cleaned_text = re.sub(r' {2,}', ' ', self.cleaned_text)

    def pattern_splitter(self):
        """ pattern_splitter splits text via pattern """
        self.sents = re.split(self.split_pattern, self.cleaned_text)
        self.sents = [sent.strip() for sent in self.sents if len(sent.strip()) > 0]
