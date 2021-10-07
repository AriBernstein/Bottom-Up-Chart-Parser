from phrase import Phrase, IncompletePhrase
from utils import get_parts_of_speech, phrase_string_to_word_list
from part_of_speech import PartOfSpeech as pos
from CFG import cfg
from parse_tree import ParseTree

def _get_base_tree(sentence:str) -> ParseTree:    
    starts, ends = {}, {}
    
    for i, word in enumerate(phrase_string_to_word_list(sentence)):
        starts[i], ends[i] = [], []
        
        for pos in get_parts_of_speech(word.lower()):
            new_word_phrase = Phrase(word, pos, i, i, False, True)
            starts[i].append(new_word_phrase)
            ends[i].append(new_word_phrase)
    
    return ParseTree(starts, ends, sentence)


def _incomplete_phrases_starting_with(pos:pos, current_index) -> list[IncompletePhrase]:
    """
    Given a part of speech, find all definitions in the grammar that being with it,
    For each one, instantiate a new incomplete_phrase
    """
    ret = []
    for pos_ordering in cfg.POS_PHRASE_SET:
        for i, ordering_list in enumerate(pos_ordering.all_orderings()):
            if ordering_list[0] == pos:
                ret.append(
                    IncompletePhrase(pos_ordering.pos, i, 0, current_index)
                )
                
    return ret


def _build_tree_helper(permutation_set:list[list[Phrase]],
                       current_tree:ParseTree,
                       incomplete_phrases:set[IncompletePhrase]=set(),
                       prev_starts_dict:dict=None, prev_ends_dict:dict=None) -> list[list[Phrase]]:
    """
    Permutation set -> set of lists containing existing orderings of phrases
    Incomplete Phrases -> sets of incomplete phrases in the process of being constructed
    """
    if prev_starts_dict == None:
        prev_starts_dict = current_tree.starts
    if prev_ends_dict == None:
        prev_ends_dict = current_tree.ends
    
    new_starts, new_ends = {}, {}
    
    # List of sets of phrases, each index correlates to 
    for permutation in permutation_set: # Iterate through lists of Phrase objects
        
        for cur_phrase in permutation:  # Iterate through phrase objects
                    
            # Add new potentials phrases to set
            incomplete_phrases.update(
                _incomplete_phrases_starting_with(cur_phrase.pos, cur_phrase.start_index))
            
            # For each incomplete phrase, remove if invalid, update otherwise
            for incomplete_phrase in incomplete_phrases.copy():
                
                # If no match, remove form future consideration
                if incomplete_phrase.expected_phrase() != cur_phrase.pos:
                    incomplete_phrases.remove(incomplete_phrase)
                    continue
                
                # Else, add subphrase
                incomplete_phrase.add_ordering(cur_phrase)
                
                # If just-added subphrase has completed its phrase:
                if incomplete_phrase.terminal():
                    completed_phrase = incomplete_phrase.complete(current_tree.sentence_lst,
                                                                  cur_phrase.end_index)
                    current_tree.add_phrase(completed_phrase)
                    incomplete_phrases.remove(incomplete_phrase)

                    # Add to dictionaries for new permutations                    
                    if not completed_phrase.start_index in new_starts:
                        new_starts[completed_phrase.start_index] = set()
                    new_starts[completed_phrase.start_index].add(completed_phrase)
                    
                    if not completed_phrase.end_index in new_ends:
                        new_ends[completed_phrase.end_index] = set()
                    new_ends[completed_phrase.end_index].add(completed_phrase)
                    
                    continue
                
                incomplete_phrase.advance()
    
    
    for word_index in range(current_tree.num_words):
        if not word_index in new_starts:
            new_starts[word_index] = current_tree.starts[word_index]
        if not word_index in new_ends:
            new_ends[word_index] = current_tree.ends[word_index]
    
    return ParseTree(new_starts, new_ends, "").get_permutations()
    
    
def build_tree(sentence:str) -> ParseTree:
    
    # Instantiate lists of permutations of word phrases
    current_tree = _get_base_tree(sentence)
    counter = 0
    valid_permutations = current_tree.get_permutations()
    while(not current_tree.has_root()):
        valid_permutations = _build_tree_helper(valid_permutations, current_tree)
        for i in valid_permutations:
            print(i)
            
        print("================")

        if counter == 4:
            break
        counter += 1
        
    for i in valid_permutations:
        print(i)