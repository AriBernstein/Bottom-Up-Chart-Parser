from Phrases.noun_phrase import NounPhrase
from part_of_speech import PartOfSpeech as pos

class Ordering:
    def __init__(self, part_of_speech:pos, valid_orderings: set=None, word:bool=True, composite:bool = False) -> None:
        self.valid_orderings = valid_orderings
        self.pos = part_of_speech
        self.word = word
        self.composite = composite
    
class Opt: # Optional
    def __init__(self, order:Ordering, optional:bool=True) -> None:
        self.order = order
        self.optional = optional


HEAD_NOUN = Ordering(pos.HEAD_NOUN)
NOUN = Ordering(pos.NOUN)
VERB = Ordering(pos.VERB)
ADJECTIVE = Ordering(pos.ADJECTIVE)
ADVERB = Ordering(pos.ADVERB)
AUXILLARY_VERB = Ordering(pos.AUXILLARY_VERB)
MODAL_VERB = Ordering(pos.MODAL_VERB)
DETERMINER = Ordering(pos.DETERMINER)
PRONOUN = Ordering(pos.PRONOUN)
GERUNDIVE_ING = Ordering(pos.GERUNDIVE_ING)
GERUNDIVE_ED = Ordering(pos.GERUNDIVE_ED)
PREPOSITION = Ordering(pos.PREPOSITION)
WH_WORD = Ordering(pos.WH)
CARDINAL_NUMBER = Ordering(pos.CARDINAL_NUMBER)
ORDINAL_NUMBER = Ordering(pos.ORDINAL_NUMBER)
QUANTIFIER = Ordering(pos.QUANTIFIER)
CONJUNCTION = Ordering(pos.CONJUNCTION)
RECURSE = Ordering(pos.RECURSE)

# SIMPLE
VERB_PHRASE = Ordering(pos.VERB_PHRASE, set([
    [pos.VERB, pos.ADVERB]
    ]), False)

NOUN_PHRASE = Ordering(pos.NOUN_PHRASE, set([
    [pos.ADJECTIVE, pos.NOUN],
    [pos.ADJECTIVE, pos.NOUN_PHRASE]
    ]), False)

SENTENCE = Ordering(pos.SENTENCE, set([
    [pos.NOUN_PHRASE, pos.VERB_PHRASE],
    [pos.SENTENCE, pos.CONJUNCTION, pos.SENTENCE]
    ]), False)


# PREDETERMINER = Ordering(pos.PREDETERMINER, word=True)
# POSTDETERMINER = Ordering(pos.POSTDETERMINER, set([
#     [pos.CARDINAL_NUMBER],
#     [pos.ORDINAL_NUMBER],
#     [pos.QUANTIFIER]
#     [pos.ORDINAL_NUMBER, pos.QUANTIFIER]
#     ]), word=False)
# POST_MODIFIER = Ordering(pos.POSTMODIFIER, word=False)
# POST_NOMINAL_RELATIVE_CLAUSE = Ordering(pos.POSTNOMINAL_RELATIVE_CLAUSE, word=False)


# POST_MODIFIER_NON_FINITE = Ordering(pos.POSTMODIFIER_NON_FINITE, valid_orderings=set([
#     [pos.PREPOSITION_PHRASE],
#     [pos.GERUNDIVE_ING_PHRASE]
#     ]), word=False)

# NOUN_PHRASE_LEFT = Ordering(pos.NOUN_PHRASE_LEFT, set([
#     [Opt(pos.DETERMINER), Opt(pos.POSTDETERMINER), Opt(pos.ADJECTIVE), Opt(pos.NOUN_PHRASE)]
#     ]), word=False, composite=True)

# NOUN_PHRASE = Ordering(pos.NOUN_PHRASE, valid_orderings=set([
#     [Opt(pos.NOUN_PHRASE_LEFT), NOUN, Opt(pos.RECURSE), Opt(pos.GERUNDIVE_ING_PHRASE)]
#     [pos.RECURSE, pos.CONJUNCTION, pos.RECURSE]
#     ]), word=False)

# PREPOSITION_PHRASE = Ordering(pos.PREPOSITION_PHRASE, set(
#     [pos.PREPOSITION, pos.NOUN_PHRASE]
# ), word=False)


# VERB_PHRASE = Ordering(pos.VERB_PHRASE, set([
#     [pos.VERB, Opt(pos.NOUN_PHRASE), Opt(pos.PREPOSITION_PHRASE)],
#     [pos.VERB, Opt(pos.NOUN_PHRASE), pos.SENTENCE]
#     [pos.RECURSE, pos.CONJUNCTION, pos.RECURSE]
#     ]), word=False)


# GERUNDIVE_ING_PHRASE = Ordering(pos.GERUNDIVE_ING_PHRASE, valid_orderings=set([
#     [pos.GERUNDIVE_ING, pos.VERB_PHRASE]
#     ]), word=False)

# AUX_SENTENCE_QUESTION = Ordering(pos.AUX_SENTENCE_QUESTION, set([
#     [pos.AUXILLARY_VERB, pos.NOUN_PHRASE, pos.VERB_PHRASE]
# ]), word=False)

# WH_SUBJECT_QUESTION = Ordering(pos.WH_SUBJECT_QUESTION, set([
#     [pos.WH_WORD, pos.NOUN_PHRASE, pos.VERB_PHRASE]
# ]), word=False) 

# WHY_NON_SUBJECT_QUESTION = Ordering(pos.WHY_NON_SUBJECT_QUESTION, set([
#     [pos.WH_WORD, pos.NOUN_PHRASE, pos.AUXILLARY_VERB, pos.NOUN_PHRASE, pos.VERB_PHRASE]
# ]))

# SENTENCE = Ordering(pos.SENTENCE, set(
#     [Opt(pos.NOUN_PHRASE), pos.VERB_PHRASE],
#     [pos.AUX_SENTENCE_QUESTION],
#     [pos.WH_SUBJECT_QUESTION]
#     [pos.WHY_NON_SUBJECT_QUESTION]
# ), word=False)
