from CFG.Noun.noun_phrase_ordering import POST_MODIFIER
from enum import Enum

class PartOfSpeech(Enum):
    SENTENCE = "sentence"
    NOUN = 'noun'
    NOUN_PHRASE = 'noun_phrase'
    VERB_PHRASE = 'verb_phrase'
    PREPOSITION_PHRASE= "preposition_phrase"
    VERB = 'verb'
    ADJECTIVE = 'adjective'
    ADVERB = 'adverb'
    AUXILLARY_VERB = 'auxillary_verb'
    MODAL_VERB = 'modal_verb'
    DETERMINER = 'determiner'
    PRONOUN = 'pronoun'
    HEAD_NOUN = 'head_noun'
    PRE_DETERMINER = "pre_determiner"
    POST_DETERMINER = "post_determiners"
    POST_MODIFIER = "post_modifier"
    POST_MODIFIER_NON_FINITE = "post_modifier_non_finite"
    POST_NOMINAL_RELATIVE_CLAUSE = "post_nominal_relative_clause"
    GERUNDIVE = "gerundive"
    PREPOSITION = "preposition"
    WH = "wh_word"
    CARDINAL_NUMBER = "cardinal_number"
    ORDINAL_NUMBER = "ordinal_number"
    QUANTIFIER = "quantifier"