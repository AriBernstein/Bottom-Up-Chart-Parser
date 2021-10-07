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
                       incomplete_phrases:list[IncompletePhrase]=[]) -> Phrase:
    """
    Permutation set -> set of lists containing existing orderings of phrases
    Incomplete Phrases -> sets of incomplete phrases in the process of being constructed
    """
    # List of sets of phrases, each index correlates to 
    discovered_phrases = []
    for permutation in permutation_set: # Iterate through lists of Phrase objects
        
        for cur_phrase in permutation:  # Iterate through phrase objects
                    
            # Add new potentials phrases to set
            incomplete_phrases.extend(
                _incomplete_phrases_starting_with(cur_phrase.pos, cur_phrase.start_index))
            
            # For each incomplete phrase, remove if invalid, update otherwise
            for incomplete_phrase in incomplete_phrases.copy():
                if incomplete_phrase.expected_phrase() != cur_phrase:
                    incomplete_phrases.remove(incomplete_phrase)
                    continue
                
                incomplete_phrase.add_ordering(cur_phrase)
                
                if incomplete_phrase.terminal():
                    newly_validated_phrase = incomplete_phrase.complete(cur_phrase.end_index)
                    current_tree.add_phrase(newly_validated_phrase)
                        
                    incomplete_phrases.remove(incomplete_phrase)
                    continue
                
                incomplete_phrase.advance()
            
            
            discovered_phrases.append(
                sorted(cur_discovered_phrases, key=lambda phr: len(phr)))
                    
    
def build_tree(sentence:str) -> Phrase:
    
    # Instantiate lists of permutations of word phrases
    current_tree = _get_base_tree(sentence)
    valid_permutations = current_tree.get_permutations()
    for i in valid_permutations:
        print(i)
    
    # n = len(valid_permutations[0])
    
    # sentences = set()
    
    
    _build_tree_helper(valid_permutations, )