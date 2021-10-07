

from utils import phrase_string_to_word_list
from phrase import Phrase

class ParseTree:
    
    def __init__(self, start_dict:dict, end_dict:dict, sentence:str) -> None:
        self.starts = start_dict
        self.ends = end_dict
        self.sentence_str = sentence
        self.sentence_lst = phrase_string_to_word_list(sentence)
        self.root = None
        self.length = len(self.sentence_lst)
        
    def _find_root(self) -> Phrase:
        pass
        
    def phrases_starting_at_index(self, index:int) -> list[Phrase]:
        return self.starts[index]
    
    def phrases_ending_at_index(self, index:int) -> list[Phrase]:
        return self.ends[index]
    
    def get_root(self) -> Phrase:
        return self.root
    
    def set_root(self, root:Phrase) -> None:
        self.root = root
        
    def has_root(self) -> bool:
        return self.root != None
    
    def add_phrase(self, phr:Phrase) -> None:
        self.starts[phr.start_index].append(phr)
        self.ends[phr.end_index].append(phr)
        if phr.start_index == 0 and phr.end_index == self.length - 1:
            self.root = phr
            
    def _traversal_helper(self, current_phrase:Phrase,
                          current_permutation:list[Phrase]=[]) -> list[list[Phrase]]:
        
        end_index = current_phrase.end_index
        
        current_permutation = current_permutation.copy()
        current_permutation.append(current_phrase)
        
        # If there is nothing to the right
        if end_index == len(self.sentence_lst) - 1:
            return [current_permutation]
 
 
        # Else, for each phrase starting to the index one after the end of our current
        # phrase, add a permutation
        current_phrase_permutations = []
        for next_phr in self.ends[end_index + 1]:   # For each of the phrases that start immediately after this ends
            following_permutations = self._traversal_helper(next_phr, current_permutation)  # Get list of permutations (list of phrases) 
            current_phrase_permutations.extend(following_permutations)
            
        return current_phrase_permutations
        
    
    def get_permutations(self) -> list[list[Phrase]]:
        
        permutations = []
        
        for starter_phrase in self.starts[0]:
            permutations.extend(
                self._traversal_helper(starter_phrase)
            )
            
        return permutations