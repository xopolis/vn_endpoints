"""
Extract text from within html tags
"""
import re
from bs4 import BeautifulSoup
# from ner_text_tokeniser import NERTextConversion

class ProcessIndeedHTML:# pylint:disable=R0903
    """
    extract tokens from Indeed HTML texts
    """
    # @staticmethod
    # def process_html(html):
        # texts = ProcessIndeedHTML.get_content(html)
        # return super(ProcessIndeedHTML, ProcessIndeedHTML).convert_text(texts)

    @staticmethod
    def get_content(html_text):
        """get texts from leaf html nodes"""
        html = html_text
        soup = BeautifulSoup(html,'html.parser')
        body_ = soup.find_all(
        'div',{'id':'jobDescriptionText','class':'jobsearch-jobDescriptionText'}
        )

        texts = []
        for i in body_:
            texts.extend(i.findAll(text=True, recursive=True))

        # convert BeautifulSoup tags to text
        texts_ = list(map(str, texts))

        # text cleaning

        # 1. split text by new line, \n and newline like \\n

        splitted_texts = []
        for text_ in texts_:
            splitted_texts.extend(re.split(r'\n|\\n', text_))

        # 2. strip sentences
        splitted_texts = list(map(str.strip, splitted_texts))

        # 3. filter out empty strings, which contain only whitespaces
        splitted_texts = list(filter(lambda x : bool(x), splitted_texts))# pylint:disable=W0108

        return splitted_texts
