from cfg.cfg import POS_PHRASE_SET
from cfg.cfg_utils import phrase_string_to_word_list, get_parts_of_speech
from parse_tree.chart_agenda import Agenda, Chart
from parse_tree.arc import ActiveArc, CompleteArc

def _get_initial_agenda(sentence:str) -> Agenda:    
    starting_arcs = []
    for i, word in enumerate(phrase_string_to_word_list(sentence)):
        for pos in get_parts_of_speech(word):
            starting_arcs.append(
                CompleteArc(words=[word], pos=pos, input_str_start_index=i,
                            input_str_end_index=i, leaf=True))
    
    return Agenda(list(reversed(starting_arcs)))

def _active_arcs_starting_with(initial_arc:CompleteArc) -> list[ActiveArc]:
    """
    Given a complete arc initial_arc, find all phrases and orderings whose first
    element = pos of initial_arc . For each such pos-ordering, create a new 
    active arc populated only by initial_arc of said pos with ordering pointing 
    to the 0th index.
    
    Args:
        initial_arc (CompleteArc): initial complete arc, look for its POS at the
            start of all POS orderings

    Returns:
        list[ActiveArc]: list of activeArcs, each containing only initial_arc as
            the first or final element in their subsequences
    """
    ret = []
    for pos_ordering in POS_PHRASE_SET:
        for i, ordering_list in enumerate(pos_ordering.all_orderings()):
            if ordering_list[0] == initial_arc.get_pos():                
                new_active_arc = ActiveArc(pos_ordering.pos, i,
                                           initial_arc.start_index())
                new_active_arc.add_to_subsequence(initial_arc)
                ret.append(new_active_arc)
    return ret


def _generate_arcs(agenda:Agenda, chart:Chart) -> None:
    """
    Takes a newly-completed arc from the agenda and uses it to:
        1. Bottom-up arc addition - create new active arcs which start with the
           POS of the newly-completed arc.
        
        2. Active Arc extension - continue to populate the subsequences of
           active arcs.
        
        3. Arc completion - for all of the Complete Arcs created during steps 1
           and/or 2, and add them to the agenda.
    
    Args:
        agenda (Agenda): stack of newly-created complete arcs
        chart (Chart): stores the parse tree
    """

    cur_complete_arc = agenda.pop()    
    chart.add_complete_arc(cur_complete_arc)
    newly_completed_arcs = set()
    
    # Bottom-up arc addition
    for new_arc in _active_arcs_starting_with(cur_complete_arc):
        
        if new_arc.validate():
            newly_completed_arc = new_arc.make_complete(chart._sentence_lst)
            newly_completed_arcs.add(newly_completed_arc)
        else:
            chart.add_active_arc(new_arc)
        
    # Active Arc extension
    if cur_complete_arc.start_index() > 0:
        
        for active_arc in chart.incomplete_ends[cur_complete_arc.start_index() - 1].copy():
            
            if active_arc.next_expected_pos() == cur_complete_arc.get_pos():
                
                # Use a copy so that the current state can be maintained in the
                # case of another valid CompleteArc 
                active_arc = active_arc.copy()
                                
                # Changes complete_arc.end_index() return
                active_arc.add_to_subsequence(cur_complete_arc)
                
                if active_arc.validate():
                    newly_completed_arc = active_arc.make_complete(chart._sentence_lst)
                    newly_completed_arcs.add(newly_completed_arc)
                else:
                    chart.update_active_arc(active_arc)

    # Arc completion
    for newly_completed_arc in newly_completed_arcs:
        agenda.push(newly_completed_arc)
           
    
def build_tree(sentence:str) -> Chart:
    """
    Given the string prepresentation of a sentence, break it down into terminal
    CompleteArcs, create the initial Agenda using new CompleteArcs, and use this
    to iteratively populate a chart. Stop when every possible CompleteArc has
    been found.

    Args:
        sentence (str): Input sentence to be parsed into parse tree.

    Raises:
        exception: If, after discovering every possible CompleteArc, cannot find
                   one which spans the entire sentence.

    Returns:
        Chart: a populated chart whose roots represent interpretations of the
               parse tree for sentence.
    """
    agenda = _get_initial_agenda(sentence)
    chart = Chart(sentence)
    
    while not agenda.empty():
        _generate_arcs(agenda, chart)
    
    if chart.has_root():
        return chart
    else:
        raise Exception("Could not find root for parse tree.")