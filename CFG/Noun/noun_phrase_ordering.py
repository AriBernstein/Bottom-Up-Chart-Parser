from CFG.cfg_utils import *
from part_of_speech import PartOfSpeech as pos



PRE_DETERMINER = Ordering(pos.PRE_DETERMINER)

DETERMINER = Ordering(pos.DETERMINER)

POST_DETERMINER = Ordering(pos.POST_DETERMINER, set(
    []))

ADJECTIVE = Ordering

HEAD_NOUN = Ordering(pos.HEAD_NOUN, None)

POST_MODIFIER = Ordering

# WITHIN POST_MODIFIER
NON_FINITE_POST_MODIFIER = Ordering
# WITHIN NON FINITE POST MODIFIER
# GERUNDIVE - VERB Phrase
GERUNDIVE_ING = Ordering
GERUNDIVE_ED = Ordering
# AFTER ^
# POST_NOMINAL_RELATIVE_CLAUSE

NOUN_PHRASE
