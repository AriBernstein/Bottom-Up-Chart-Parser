import re
from queue import SimpleQueue
from nltk.corpus import wordnet as wn

from part_of_speech import PartOfSpeech as pos
from CFG import cfg
from CFG.word_constants import aux_verbs, modal_verbs, determiners, \
                           pronouns
from chart.chart_agenda import Chart, Agenda
from chart.arc import CompleteArc, ActiveArc


def get_parts_of_speech(word:str) -> set:
    # n    noun 
    # v    verb 
    # a    adjective 
    # s    adjective satellite 
    # r    adverb
    # x    auxillary verb
    # m    modal verb
    # d    determiner
    # p    pronoun

    word_data = wn.synsets(word)
    part_of_speech_set = set()
    
    if word in aux_verbs:
        part_of_speech_set.add(pos.AUXILLARY_VERB)
        
        if word in modal_verbs:
            part_of_speech_set.add(pos.MODAL_VERB)
            
    if word in determiners:
        part_of_speech_set.add(pos.DETERMINER)
        
    if word in pronouns:
        part_of_speech_set.add(pos.PRONOUN)

    for i in word_data:
        p = str(i.pos())
        
        if p == 'n':
            part_of_speech_set.add(pos.NOUN)
        elif p == 'v':
            part_of_speech_set.add(pos.VERB)
        elif p == 'a':
            part_of_speech_set.add(pos.ADJECTIVE)
        elif p == 's':
            part_of_speech_set.add(pos.ADJECTIVE)
        elif p == 'r':
            part_of_speech_set.add(pos.ADVERB)
        else:
            raise Exception(f"Cannot find POS for tag: {p}, word: {word}.")
        
    return part_of_speech_set


def lower_case_plain_text(phrase_str:str) -> str:
    return re.sub(r"[:;!?/,]", "", phrase_str).lower()


def phrase_string_to_word_list(phrase_str:str) -> list[str]:
    return lower_case_plain_text(phrase_str).split(' ')


def get_initial_agenda(sentence:str) -> Agenda:    
    starting_arcs = SimpleQueue()
    for i, word in enumerate(phrase_string_to_word_list(sentence)):
        for pos in get_parts_of_speech(word.lower()):
            starting_arcs.put(
                CompleteArc(word, pos, i, i, False, True))
    
    return Agenda(starting_arcs)


def incomplete_arcs_starting_with(pos:pos, current_index, ending_with=False) -> list[ActiveArc]:
    """
    Given a part of speech, find all definitions in the grammar that being with it,
    For each one, instantiate a new ActiveArc
    """
    ret = []
    for pos_ordering in cfg.POS_PHRASE_SET:
        for i, ordering_list in enumerate(pos_ordering.all_orderings()):
            if ordering_list[-1 if ending_with else 0] == pos:
                ret.append(
                    ActiveArc(pos_ordering.pos, i, 0, current_index))
    return ret


def incomplete_arcs_ending_with(pos:pos, current_index) -> list[ActiveArc]:
    """
    Given a part of speech, find all definitions in the grammar that end with it,
    For each one, instantiate a new ActiveArc
    """
    return incomplete_arcs_starting_with(pos, current_index, ending_with=True)