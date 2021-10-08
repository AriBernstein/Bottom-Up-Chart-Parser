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


def get_pos_ordering(pos:pos, ordering_index:int) -> list[pos]:
    return cfg.RULES_DICT[pos].get_order(ordering_index)


def get_initial_agenda(sentence:str) -> Agenda:    
    starting_arcs = SimpleQueue()
    for i, word in enumerate(phrase_string_to_word_list(sentence)):
        for pos in get_parts_of_speech(word.lower()):
            starting_arcs.put(
                CompleteArc(word, pos, i, i, False, True))
    
    return Agenda(starting_arcs)

def incomplete_arcs_starting_with(initial_arc:CompleteArc, ending_with=False) -> list[ActiveArc]:
    """
    Given a complete arc initial_arc, find all phrases and orderings whose first element = pos
    of initial_arc . For each such pos-ordering, create a new active arc populated only by
    initial_arc of said pos with ordering pointing to the 0th index.
    
    Args:
        initial_arc (CompleteArc): initial complete arc, look for its POS at the start/end
                                   of all POS orderings
        ending_with (bool, optional): If true, look instead for POS orderings that end
                                      with pos of initial_arc, create active arc with 
                                      initial_arc at the end of its subsequence with cur
                                      index as the final index of subsequence

    Returns:
        list[ActiveArc]: list of activeArcs, each containing only initial_arc as the first or
                         final element in their subsequences
    """
    ret = []
    for pos_ordering in cfg.POS_PHRASE_SET:
        for i, ordering_list in enumerate(pos_ordering.all_orderings()):
            ordering_index = len(ordering_list) - 1 if ending_with else 0
            if ordering_list[ordering_index] == initial_arc.get_pos():
                
                # Check that new ordering will fit into string (still might not)
                if initial_arc.end_index() >= len(ordering_list) - 1:
                    new_active_arc = ActiveArc(pos_ordering.pos, i, ordering_index, initial_arc.end_index())
                    new_active_arc.add_to_subsequence(initial_arc)
                    ret.append(new_active_arc)
    return ret


def incomplete_arcs_ending_with(initial_arc:CompleteArc) -> list[ActiveArc]:
    """
    Given a complete arc first_arc, find all phrases and orderings whose last element = pos
    of initial_arc . For each such pos-ordering, create a new active arc populated only by
    initial_arc of said pos with ordering pointing to the final index of its subsequence.

    Args:
        initial_arc (CompleteArc): initial complete arc, look for its POS at the end
                                   of all POS orderings

    Returns:
        list[ActiveArc]: [description]
    """
    return incomplete_arcs_starting_with(initial_arc, ending_with=True)