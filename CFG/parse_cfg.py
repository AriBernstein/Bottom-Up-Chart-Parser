from constituent import CompleteConstituent, IncompleteConstituent
from utils import get_parts_of_speech, phrase_string_to_word_list
from part_of_speech import PartOfSpeech as pos
from CFG import cfg
from agenda import Agenda

def _get_base_tree(sentence:str) -> Agenda:    
    starts, ends = {}, {}
    
    for i, word in enumerate(phrase_string_to_word_list(sentence)):
        starts[i], ends[i] = [], []
        
        for pos in get_parts_of_speech(word.lower()):
            new_word_phrase = CompleteConstituent(word, pos, i, i, False, True)
            starts[i].append(new_word_phrase)
            ends[i].append(new_word_phrase)
    
    return Agenda(starts, ends, sentence)


def _incomplete_constituents_starting_with(pos:pos, current_index, ending_with=False) -> list[IncompleteConstituent]:
    """
    Given a part of speech, find all definitions in the grammar that being with it,
    For each one, instantiate a new IncompleteConstituent
    """
    ret = []
    for pos_ordering in cfg.POS_PHRASE_SET:
        for i, ordering_list in enumerate(pos_ordering.all_orderings()):
            if ordering_list[-1 if ending_with else 0] == pos:
                ret.append(
                    IncompleteConstituent(pos_ordering.pos, i, 0, current_index)
                )
                
    return ret


def _incomplete_constituents_ending_with(pos:pos, current_index) -> list[IncompleteConstituent]:
    """
    Given a part of speech, find all definitions in the grammar that end with it,
    For each one, instantiate a new IncompleteConstituent
    """
    return _incomplete_constituents_starting_with(pos, current_index, ending_with=True)


def _build_tree_helper(permutation_list:list[list[CompleteConstituent]],
                       current_tree:Agenda,
                       prev_starts_dict:dict, prev_ends_dict:dict) -> list[list[CompleteConstituent]]:
    """
    Permutation set -> set of lists containing existing orderings of Constituents
    Incomplete Phrases -> sets of incomplete phrases in the process of being constructed
    """
    incomplete_constituents = set()
    new_starts, new_ends = {}, {}
    
    # List of sets of constituents, each index correlates to 
    for permutation in permutation_list: # Iterate through lists of constituent objects
        
        for cur_const in permutation:  # Iterate through constituent objects
                    
            # Add new potentials constituent to set
            incomplete_constituents.update(
                _incomplete_constituents_starting_with(cur_const.pos, cur_const.start_index))
            
            # For each incomplete constituent, remove if invalid, update otherwise
            for incomplete_const in incomplete_constituents.copy():
                
                # If no match, remove form future consideration
                if incomplete_const.expected_pos() != cur_const.pos:
                    incomplete_constituents.remove(incomplete_const)
                    continue
                
                # Else, add subphrase
                incomplete_const.add_ordering(cur_const)
                
                # If just-added subphrase has completed its phrase:
                if incomplete_const.terminal():
                    completed_phrase = incomplete_const.complete(current_tree.sentence_lst,
                                                                 cur_const.end_index)
                    current_tree.add_constituent(completed_phrase)
                    incomplete_constituents.remove(incomplete_const)

                    # Add to dictionaries for new permutations                    
                    if not completed_phrase.start_index in new_starts:
                        new_starts[completed_phrase.start_index] = []
                    new_starts[completed_phrase.start_index].append(completed_phrase)
                    
                    if not completed_phrase.end_index in new_ends:
                        new_ends[completed_phrase.end_index] = []
                    new_ends[completed_phrase.end_index].append(completed_phrase)
                    
                    continue
                
                incomplete_const.advance()
    
    
    for word_index in range(current_tree.num_words):
        if not word_index in new_starts:
            new_starts[word_index] = prev_starts_dict[word_index]
        if not word_index in new_ends:
            new_ends[word_index] = prev_ends_dict[word_index]
    
    return Agenda(new_starts, new_ends, "").get_permutations()
    
    
def build_tree(sentence:str) -> Agenda:
    
    # Instantiate lists of permutations of word phrases
    current_tree = _get_base_tree(sentence)
    counter = 0
    valid_permutations = current_tree.get_permutations()
    
    previous_start_dict, previous_end_dict = current_tree.starts, current_tree.ends
    
    while(not current_tree.has_root()):
        valid_permutations = _build_tree_helper(valid_permutations, current_tree,
                                                previous_start_dict, previous_end_dict)

            
        print("================")

        if counter ==   10:
            break
        counter += 1
        
    for i in valid_permutations:
        print(i)