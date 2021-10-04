from Phrases.noun_phrase import NounPhrase
from part_of_speech import PartOfSpeech as pos
    

class Ordering():
    def __init__(self, part_of_speech:pos, valid_orderings: set=None,
                 many:bool=False, word:bool=True) -> None:
        self.valid_orderings = valid_orderings
        self.many = many
        self.pos = part_of_speech
        self.word = word


HEAD_NOUN = Ordering(pos.HEAD_NOUN)
NOUN = Ordering(pos.NOUN)
VERB = Ordering(pos.VERB)
ADJECTIVE = Ordering(pos.ADJECTIVE)
ADVERB = Ordering(pos.ADVERB)
AUXILLARY_VERB = Ordering(pos.AUXILLARY_VERB)
MODAL_VERB = Ordering(pos.MODAL_VERB)
DETERMINER = Ordering(pos.DETERMINER)
PRONOUN = Ordering(pos.PRONOUN)
GERUNDIVE = Ordering(pos.GERUNDIVE)
PREPOSITION = Ordering(pos.PREPOSITION)
WH_WORD = Ordering(pos.WH)
CARDINAL_NUMBER = Ordering(pos.CARDINAL_NUMBER)
ORDINAL_NUMBER = Ordering(pos.ORDINAL_NUMBER)
QUANTIFIER = Ordering(pos.QUANTIFIER)

PRE_DETERMINER = Ordering(pos.PRE_DETERMINER, word=True)
POST_DETERMINER = Ordering(pos.POST_DETERMINER, set([
    [CARDINAL_NUMBER],
    [ORDINAL_NUMBER],
    [QUANTIFIER]
    ]), word=False)
POST_MODIFIER = Ordering(pos.POST_MODIFIER, word=False)
POST_MODIFIER_NON_FINITE = Ordering(pos.POST_MODIFIER_NON_FINITE, word=False)
POST_NOMINAL_RELATIVE_CLAUSE = Ordering(pos.POST_NOMINAL_RELATIVE_CLAUSE, word=False)


NOUN_PHRASE = Ordering(pos.NOUN_PHRASE, valid_orderings=set([
    [NOUN],
    [DETERMINER, NOUN],
    [DETERMINER]
    ]), many=True, word=False)


PREPOSITION_PHRASE = Ordering(pos.PREPOSITION_PHRASE, set(
    [PREPOSITION, NOUN_PHRASE]
), word=False)

VERB_PHRASE = Ordering(pos.VERB_PHRASE, set([
    [VERB, 'VERB_PHRASE'],
    [VERB, NOUN_PHRASE],
    [VERB, NOUN_PHRASE, PREPOSITION_PHRASE],
    [VERB, PREPOSITION_PHRASE],
    [VERB, NOUN_PHRASE]
    ]), True, False)


SENTENCE = Ordering(pos.SENTENCE, set(
    [VERB_PHRASE],
    [NOUN_PHRASE, VERB_PHRASE],
), word=False)

AUX_SENTENCE_QUESTION = Ordering(pos.SENTENCE, set([
    [AUXILLARY_VERB, NOUN_PHRASE, VERB_PHRASE]
]), word=False)

WH_SUBJECT_QUESTION = Ordering(pos.SENTENCE, set([
    [WH_WORD, NOUN_PHRASE, VERB_PHRASE]
]), word=False)

WHY_NON_SUBJECT_QUESTION = Ordering(pos.SENTENCE, set([
    [WH_WORD, NOUN_PHRASE, AUXILLARY_VERB, NOUN_PHRASE, VERB_PHRASE]
]))

VERB_PHRASE.pos.update([
    [VERB_PHRASE, SENTENCE],
    [VERB_PHRASE, NOUN_PHRASE, SENTENCE]
])