from phrase import Phrase, PhraseChildren, IncompletePhrase
from utils import initial_phrase_pos_permutations
import part_of_speech as pos
from CFG import cfg

def incomplete_phrases_starting_with(pos:pos) -> list[IncompletePhrase]:
    ret = []
    for pos_ordering in cfg.POS_PHRASE_SET:
        for i, ordering_list in enumerate(pos_ordering.all_orderings()):
            if ordering_list[0] == pos:
                ret.append(
                    IncompletePhrase(pos_ordering.pos, i, 0)
                )
                
    return ret

# def _build_tree_helper(permutation_set:set[list],
#                        incomplete_phrases:set[list[IncompletePhrase]],
#                        complete_tree_set:set[Phrase]) -> Phrase:
#     """
#     Permutation set -> set of lists containing existing orderings of phrases
#     Incomplete Phrases -> sets of incomplete phrases in the process of being constructed
#     """
#     for permutation in permutation_set:
#         new_permutations = []
        
#         for phrase in permutation:
            
        
    
#         # for pos_phrase in permutation:
            
    
# def build_tree(sentence:str, valid_pos:set) -> Phrase:
    
#     # Instantiate lists of permutations of word phrases
#     valid_permutations = initial_phrase_pos_permutations(sentence)
    
#     sentences = set()
    
#     _build_tree_helper(valid_permutations, sentences)