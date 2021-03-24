from flask import Flask, jsonify, request
from vn_extraction.vn_core import VerbNounPairExtractor
from vn_extraction.ner_text_tokeniser import NERTextConversion
from vn_extraction.vn_conjuct import ConjugateSearch
from phraser.phrase_preprocessor import PhrasePreprocessor

preprocessor = PhrasePreprocessor()

app = Flask(__name__)

@app.route('/verbnoun', methods=['GET', 'POST'])
def verbnoun_text():
    """end point for verb noun extraction"""
    content = request.get_json()
    text = content['text']
    response = VerbNounPairExtractor.vn_text(text)
    return jsonify(response)

@app.route('/phrases', methods=['GET', 'POST'])
def generate_phrase_from_text():
    """end point for phrase extraction"""
    content = request.get_json()
    text = content['text']
    response = preprocessor.get_phrases(text)
    return jsonify(response)

@app.route('/sentences', methods=['GET', 'POST'])
def split_texts():
    content = request.get_json()
    text = content['text']
    response = NERTextConversion.convert_text(text)
    return jsonify(response)
    
@app.route('/vn_generation_conjugate', methods=['GET', 'POST'])
def vn_generation_conjugate():
    content = request.get_json()
    sentence = content['text']
    conser = ConjugateSearch(sentence)
    response = conser.drive_execute_return()
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7001, debug=False, use_reloader=False)