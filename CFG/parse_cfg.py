from phrase import Phrase, IncompletePhrase
from utils import get_parts_of_speech, phrase_string_to_word_list
from part_of_speech import PartOfSpeech as pos
from CFG import cfg
from parse_tree import ParseTree

def _initial_phrase_pos_permutations(sentence:str) -> set[list[Phrase]]:
    permutations = [[]]
    
    starts, ends = {}, {}
    
    for i, word in enumerate(phrase_string_to_word_list(sentence)):
        word_pos = get_parts_of_speech(word.lower())
        updated_permutations = []
        starts[i] = []
        ends[i] = []

        for pos in word_pos:
            new_word_phrase = Phrase(word, pos, i, i, False, True)
            starts[i].append(new_word_phrase)
            ends[i].append(new_word_phrase)
            for perm in permutations:
                updated_ordering = perm.copy()
                new_word_phrase = Phrase(word, pos, i, i, False, True)
                updated_ordering.append(new_word_phrase)
                updated_permutations.append(updated_ordering)
                
        permutations = updated_permutations
    
    return permutations, ParseTree(starts, ends, sentence)


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


def _all_permutations(new_permutations: list[set[Phrase]]) -> list[list[Phrase]]:
    """
    Ordered set by where phrases start
    """

    all_permutations = []
    seen_permutations = set()
    
    current_order = []
    

def _build_tree_helper(permutation_set:set[list[Phrase]],
                       incomplete_phrases:list[IncompletePhrase],
                       sentences:set[Phrase],
                       current_tree:ParseTree) -> Phrase:
    """
    Permutation set -> set of lists containing existing orderings of phrases
    Incomplete Phrases -> sets of incomplete phrases in the process of being constructed
    """
    # List of sets of phrases, each index correlates to 
    discovered_phrases = []
    for permutation in permutation_set: # Iterate through lists of Phrase objects
        terminated_phrase_set_buffer = None
        
        for phrase in permutation:  # Iterate through phrase objects
                    
            # Add new potentials phrases to set
            incomplete_phrases.update(
                [_incomplete_phrases_starting_with(phrase.pos, phrase.input_str_start_index)])
            
            terminating_phrase_set_buffer = set()
            
            cur_discovered_phrases = set()
            
            # For each incomplete phrase, remove if invalid, update otherwise
            for incomplete_phrase in incomplete_phrases.copy():
                if incomplete_phrase.expected_phrase() != Phrase:
                    incomplete_phrases.remove(incomplete_phrase)
                    continue
                
                incomplete_phrase.add_ordering(Phrase)
                
                if incomplete_phrase.empty():
                    incomplete_phrase.set_prev(terminated_phrase_set_buffer)
                
                if incomplete_phrase.terminal():
                    newly_validated_phrase = incomplete_phrase.complete()

                    terminating_phrase_set_buffer.add(newly_validated_phrase)
                    if newly_validated_phrase.pos == pos.SENTENCE:
                        sentences.add(newly_validated_phrase)
                    cur_discovered_phrases.add(newly_validated_phrase)
                        
                    incomplete_phrases.remove(incomplete_phrase)
                    continue
                
                incomplete_phrase.advance()
            
            terminated_phrase_set_buffer = terminating_phrase_set_buffer
            
            discovered_phrases.append(
                sorted(cur_discovered_phrases, key=lambda phr: len(phr)))
                    
    
def build_tree(sentence:str) -> Phrase:
    
    # Instantiate lists of permutations of word phrases
    valid_permutations, current_tree = _initial_phrase_pos_permutations(sentence)
    perms = current_tree.get_permutations()
    for i in perms:
        print(i)
        
    # print("-------")
    # for i in valid_permutations:
    #     print(i)
        
    print("---------------")
    print(current_tree.starts)
    
    print(current_tree.ends)
    # n = len(valid_permutations[0])
    
    # sentences = set()
    
    # _build_tree_helper(valid_permutations, sentences)