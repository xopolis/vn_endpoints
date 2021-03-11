"""
contains wrapper methods for extracting verb noun pairs from
job posts and resumes
"""
from vn_extraction.vn_core import VerbNounPairExtractor

class VNWrapper:
    """
    Utility methods for extracting verb noun pairs from job posts and resumes
    -------------------------------------------------------------------------
    Read text from job post and resume, and extract verb noun pairs from
    VerbNounPairing class

    Skills and ability competencies are extracted based on verb phrases and
    noun phrases,
    Task competencies are extracted using base verb and base noun forms.
    """
    @staticmethod
    def extract_verbnoun_job_body(raw_id, body): # pylint: disable=no-self-use
        """extract job post verb noun pairs"""
        dep_vn_pairs = VerbNounPairExtractor.vn_text(body)
        entry_record = {'job_post_id' : raw_id, 'dependency_vn_pairs' : dep_vn_pairs}
        return entry_record

    @staticmethod
    def extract_verbnoun_job_html(raw_id, html): # pylint: disable=no-self-use
        """extract job post verb noun pairs"""
        dep_vn_pairs = VerbNounPairExtractor.vn_html(html)
        entry_record = {'job_post_id' : raw_id, 'dependency_vn_pairs' : dep_vn_pairs}
        return entry_record

    @staticmethod
    def extract_verbnoun_resume_body(raw_id, work_experiences): # pylint: disable=no-self-use
        """extract resume verb noun pairs"""
        works_preprocessed = []
        if work_experiences:
            for work in work_experiences:
                if 'description' not in work:
                    dep_vn_pairs = []
                else:
                    dep_vn_pairs = VerbNounPairExtractor.vn_text(work['description'])

                works_preprocessed.append({'dependency_vn_pairs' : dep_vn_pairs})

        entry_record = {
            'resume_id': raw_id,
            'work_experience': works_preprocessed
        }

        return entry_record
