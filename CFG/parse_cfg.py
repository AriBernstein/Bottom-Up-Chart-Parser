import re

from phrase import Phrase, PhraseChildren
from utils import initial_phrase_pos_permutations
import part_of_speech as pos
import cfg

def _build_tree_helper(permutation_set:set(list), complete_tree_set:set(Phrase)) -> Phrase:
    for permutation in permutation_set:
        if len(permutation) == 1:
            complete_tree_set.add(permutation[0])
    
        # for pos_phrase in permutation:
            
    
def build_tree(sentence:str, valid_pos:set) -> Phrase:
    
    # Instantiate lists of permutations of word phrases
    valid_permutations = initial_phrase_pos_permutations(sentence)
    
    sentences = set()
    
    _build_tree_helper(valid_permutations, sentences)