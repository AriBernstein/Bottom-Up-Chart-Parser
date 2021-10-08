from CFG.cfg_utils import incomplete_arcs_starting_with, incomplete_arcs_ending_with, get_initial_agenda
from chart.arc import CompleteArc, ActiveArc
from chart.chart_agenda import Agenda, Chart, Chart

def _generate_arcs(agenda:Agenda, chart:Chart) -> None:
    # Dequeue a completed arc this_arc from the Agenda, add it to the Chart
    this_arc = Agenda.dequeue()
    chart.add_complete_arc(this_arc)
    newly_completed_arcs = set()
    
    # Bottom-up arc addition
    for new_arc in incomplete_arcs_ending_with(this_arc):
        
        # Given rule whose orderings end with type this_arc, add this_arc to new incomplete arc A.
        if new_arc.terminal():
            # Check if A is terminal (ie. only child is this_arc and no longer incomplete).
            # If so, convert A to complete arc and add it to the chart as such
            newly_completed_arc = new_arc.complete(chart.sentence_lst)
            newly_completed_arcs.add(newly_completed_arc)
            chart.add_complete_arc(newly_completed_arc)
        else:   # Add A to chart as incomplete arc
            chart.add_incomplete_arc(new_arc)
        
    # # Active Arc extension - find active arcs with expected_pos equal to this_arc.pos . Search in
    # # range of incomplete arcs with end index of 1 + this_arc.end_index to this_arc.start_index
    # for sentence_index in reversed(range(this_arc.start_index(), this_arc.end_index() + 1)):
    #        active_arcs = chart.incomplete_starts[sentence_index]
    #        for active_arc in active_arcs:
    #            # Moving through an incomplete arc from last to first element in subsequence, check:
    #            # 1. if start location of last-added complete arc in subsequence is immediately after
    #            #    end location of this_arc
    #            # 2. if active_arc is looking for a complete arc of the same pos as this_arc
    #            if active_arc.start_index() == this_arc.end_index() + 1 \
    #                and active_arc.expected_pos() == this_arc.get_pos():
    #                pass
    
    # Active Arc extension - find active arcs whose last-added complete arc starts immediately after
    #                        this_arc ends. Check if they are expecting a new start of the same pos
    #                        as current_arc and, if so, add current_arc to inactive arc
    for active_arc in chart.incomplete_starts[this_arc.end_index() + 1].copy():
        if active_arc.expected_pos() == this_arc.pos():
            # Update active arc
            old_start = active_arc.start_index()
            active_arc.add_to_subsequence(this_arc) # Start is updated here
            
            # Update active_arc location within chart
            chart.update_incomplete_arc(active_arc, old_start)
            
    # Arc completion
    for newly_completed_arc in newly_completed_arcs:
        agenda.enqueue(newly_completed_arc)
           
    
def build_tree(sentence:str) -> Chart:
    agenda = get_initial_agenda(sentence)
    chart = Chart(sentence)
    n = chart.word_length()
    
    while not Agenda.empty():
        _generate_arcs(agenda, chart)

    if chart.has_root():
        return chart
    else:
        raise Exception("Could not find root for parse tree.")