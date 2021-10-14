from enum import Enum
import re

class PartOfSpeech(Enum):
    SENTENCE = "sentence"
    NOUN = 'noun'
    NOUN_PHRASE = 'noun_phrase'
    NOUN_PHRASE_LEFT = 'noun_phrase_left'
    NOUN_PHRASE_RIGHT = 'noun_phrase_right'
    VERB_PHRASE = 'verb_phrase'
    PREPOSITION_PHRASE= "preposition_phrase"
    VERB = 'verb'
    NOMINAL = 'nominal'
    ADJECTIVE = 'adjective'
    ADVERB = 'adverb'
    AUXILLARY_VERB = 'auxillary_verb'
    MODAL_VERB = 'modal_verb'
    DETERMINER = 'determiner'
    PRONOUN = 'pronoun'
    HEAD_NOUN = 'head_noun'
    PREDETERMINER = "predeterminer"
    POSTDETERMINER = "postdeterminers"
    POSTMODIFIER = "postmodifier"
    POSTMODIFIER_NON_FINITE = "postmodifier_non_finite"
    POSTNOMINAL_RELATIVE_CLAUSE = "postnominal_relative_clause"
    GERUNDIVE_ING = "gerundive_ing"
    GERUNDIVE_ING_PHRASE = "gerundive_ing_phrase"
    GERUNDIVE_ED = "gerundive_ed"
    PREPOSITION = "preposition"
    WH_WORD = "wh_word"
    CARDINAL_NUMBER = "cardinal_number"
    ORDINAL_NUMBER = "ordinal_number"
    QUANTIFIER = "quantifier"
    CONJUNCTION = "conjunction"
    AUX_SENTENCE_QUESTION = "aux_sentence_question"
    WH_SUBJECT_QUESTION = "wh_subject_question"
    WHY_NON_SUBJECT_QUESTION = "why_non_subject_question"
    
    def __str__(self) -> str:
        return re.sub(r"[_]", " ", str(self.value))
    
    def __repr__(self) -> str:
        return str(self)