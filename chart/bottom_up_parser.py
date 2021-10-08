from CFG.cfg_utils import incomplete_arcs_starting_with, incomplete_arcs_ending_with, get_initial_agenda
from chart.arc import CompleteArc, ActiveArc
from chart.chart_agenda import Agenda, Chart, Chart

# def _build_tree_helper(permutation_list:list[list[CompleteArc]], current_tree:Agenda,
#                        prev_starts_dict:dict, prev_ends_dict:dict) -> list[list[CompleteArc]]:
#     """
#     Permutation set -> set of lists containing existing orderings of arcs
#     Incomplete Phrases -> sets of incomplete phrases in the process of being constructed
#     """
#     incomplete_arcs = set()
#     new_starts, new_ends = {}, {}
    
#     # List of sets of arcs, each index correlates to 
#     for permutation in permutation_list: # Iterate through lists of arc (complete) objects
        
#         for cur_arc in permutation:  # Iterate through CompleteArc objects
                    
#             # Add new potentials arc to set
#             incomplete_arcs.update(
#                 incomplete_arcs_starting_with(cur_arc.pos, cur_arc.get_start_index()))
            
#             # For each incomplete arc, remove if invalid, update otherwise
#             for incomplete_arc in incomplete_arcs.copy():
                
#                 # If no match, remove form future consideration
#                 if incomplete_arc.expected_pos() != cur_arc.pos:
#                     incomplete_arcs.remove(incomplete_arc)
#                     continue
                
#                 # Else, add subphrase
#                 incomplete_arc.add_ordering(cur_arc)
                
#                 # If just-added subphrase has completed its phrase:
#                 if incomplete_arc.terminal():
#                     completed_phrase = incomplete_arc.complete(current_tree.sentence_lst,
#                                                                  cur_arc.end_index)
#                     current_tree.add_arc(completed_phrase)
#                     incomplete_arcs.remove(incomplete_arc)

#                     # Add to dictionaries for new permutations                    
#                     if not completed_phrase.get_start_index() in new_starts:
#                         new_starts[completed_phrase.get_start_index()] = []
#                     new_starts[completed_phrase.get_start_index()].append(completed_phrase)
                    
#                     if not completed_phrase.get_end_index() in new_ends:
#                         new_ends[completed_phrase.get_end_index()] = []
#                     new_ends[completed_phrase.get_end_index()].append(completed_phrase)
                    
#                     continue
                
#                 incomplete_arc.advance()
    
    
#     for word_index in range(current_tree.num_words):
#         if not word_index in new_starts:
#             new_starts[word_index] = prev_starts_dict[word_index]
#         if not word_index in new_ends:
#             new_ends[word_index] = prev_ends_dict[word_index]
    
#     return Agenda(new_starts, new_ends, "").get_permutations()


def _generate_arcs(agenda:Agenda, chart:Chart) -> None:
    this_arc = Agenda.dequeue()
    chart.add_complete_arc(this_arc)
    
    # Bottom-up arc addition
    # for empty_arc in incomplete_arcs_starting_with(this_arc.)
    
    
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