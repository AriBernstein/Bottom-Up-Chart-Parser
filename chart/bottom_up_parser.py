from collections import deque

from cfg.cfg import POS_PHRASE_SET
from cfg.cfg_utils import phrase_string_to_word_list, get_parts_of_speech
from chart.chart_agenda import Agenda, Chart, Chart
from chart.arc import ActiveArc, CompleteArc

def _get_initial_agenda(sentence:str) -> Agenda:    
    starting_arcs = []
    for i, word in enumerate(phrase_string_to_word_list(sentence)):
        for pos in get_parts_of_speech(word.lower()):
            starting_arcs.append(
                CompleteArc(word, pos, i, i, False, True))
    
    return Agenda(deque(list(reversed(starting_arcs))))

def _active_arcs_starting_with(initial_arc:CompleteArc, ending_with=False) -> list[ActiveArc]:
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
    for pos_ordering in POS_PHRASE_SET:
        for i, ordering_list in enumerate(pos_ordering.all_orderings()):
            subsequence_index = len(ordering_list) - 1 if ending_with else 0
            
            if ordering_list[subsequence_index] == initial_arc.get_pos():                
                new_active_arc = ActiveArc(pos_ordering.pos, i, subsequence_index, 
                                           initial_arc.end_index() if ending_with \
                                               else initial_arc.end_index())
                new_active_arc.add_to_subsequence(initial_arc)
                ret.append(new_active_arc)
    return ret


def _generate_arcs(agenda:Agenda, chart:Chart) -> None:
    # Dequeue a completed arc this_arc from the Agenda, add it to the Chart
    this_arc = agenda.pop()
    chart.add_complete_arc(this_arc)
    newly_completed_arcs = set()
    
    # Bottom-up arc addition
    for new_arc in _active_arcs_starting_with(this_arc):
        
        # Given rule whose orderings end with type this_arc, add this_arc to new incomplete arc A.
        if new_arc.terminal():
            # Check if A is terminal (ie. only child is this_arc and no longer incomplete).
            # If so, convert A to complete arc and add it to the chart as such
            newly_completed_arc = new_arc.complete(chart.sentence_lst)
            newly_completed_arcs.add(newly_completed_arc)
        else:   # Add A to chart as incomplete arc
            chart.add_active_arc(new_arc)
        
    # Active Arc extension - find active arcs with expected_pos equal to this_arc.pos . Search in
    # range of incomplete arcs with end index of 1 + this_arc.end_index to this_arc.start_index
    for active_arc in chart.incomplete_ends[this_arc.start_index()].copy():
        # Moving through an incomplete arc from last to first element in subsequence, check:
        # 1. if start location of last-added complete arc in subsequence is immediately after
        #    end location of this_arc
        # 2. if active_arc is looking for a complete arc of the same pos as this_arc
        if active_arc.expected_pos() == this_arc.get_pos():
            prev_end_index = active_arc.end_index()
            active_arc.add_to_subsequence(this_arc)
            
            if active_arc.terminal():
                chart.remove_active_arc(this_arc)
                newly_completed_arc = active_arc.complete(chart.sentence_lst)
                newly_completed_arcs.add(newly_completed_arc)
            else:
                chart.update_active_arc(active_arc, prev_end_index)

    # Arc completion
    for newly_completed_arc in newly_completed_arcs:
        agenda.push(newly_completed_arc)
           
    
def build_tree(sentence:str) -> Chart:
    agenda = _get_initial_agenda(sentence)
    chart = Chart(sentence)
    
    while not agenda.empty():
        _generate_arcs(agenda, chart)

    if chart.has_root():
        return chart
    else:
        raise Exception("Could not find root for parse tree.")