# import re

# from phrase import Phrase, PhraseChildren
# from utils import get_parts_of_speech
# import part_of_speech as pos
# from cfg import *

# def tree_helper(sentence_subset:list[str], current_phrase_ordering:list) -> Phrase:
     
# def build_tree(phrase:str, valid_pos:set) -> Phrase:
    
#     # First pass - instantiate list of word phrases
#     for word in phrase.split(sep=' '):  # Remove commas, colons, semicolons, slashes
#         word_pos = get_parts_of_speech(re.sub(r'[,:;/]',"", word))
#         leaves.append(Phrase(word, word_pos))
            
    
#     # Second pass - build tree of Phrase orderings. When an ordering hits a terminal, 
#     valid_trees = []
#     for word, i in enumerate(leaves):
        