from flask import abort, jsonify
import spacy

nlp = spacy.load("en_core_web_sm")

# Tags collected from https://spacy.io/api/annotation#pos-tagging
SPACY_POS_MAPPING = {
    'adjective': ['ADJ'],
    'verb': ['VERB', 'AUX'],
    'noun': ['NOUN', 'PROPN'],
    'pronoun': ['PRON'],
    'adverb': ['ADV'],
    'preposition': ['ADP'],
    'conjunction': ['CONJ', 'CCONJ', 'SCONJ'],
    'interjection': ['INTJ'],
    'determiner': ['DET'],
    'number': ['NUM'],
    'symbol': ['SYM'],
    'other': ['X', 'PUNCT', 'SPACE', 'PART']
}


def getPOS(input_json):
    """
    This service extracts one given part-of-speech from given text
    :param input_json: a dictionary that contains the text to analyze and
                       a tag that specifies which part-of-speech to look for (regular word, not the actual POS code)
    :return: All the words in the text that match the part-of-speech to look for
    """
    blob, tag = None, None
    try:
        text = nlp(input_json['text'])
        tag = input_json['tag']
    except KeyError:
        abort(400, "Please provide a JSON with \'text\' and a \'tag\' to search for.")
    pos = [(token.text, token.pos_) for token in text]
    return jsonify(result=[word[0] for word in pos if word[1] in
                           [tag] + (SPACY_POS_MAPPING.get(tag) or [])])


def getSimilarity(input_json):
    """
    This service gives the cosine similarity between any two given texts
    NOTE: this service uses small spaCy model because of AWS EC2 RAM constraints, so results are different compared
          compared to the larger models.
    :param input_json: a dictionary that contains strings "text1" and "text2"
    :return: THe cosine similarity of two given text strings
    """
    s1, s2 = None, None
    try:
        s1 = input_json['text1']
        s2 = input_json['text2']
    except KeyError:
        abort(400, "Please provide a JSON with \'text1\' and \'text2\' to calculate the similarity of.")
    return jsonify(result=nlp(s1).similarity(nlp(s2)))

