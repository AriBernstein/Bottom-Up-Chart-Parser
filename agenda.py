from bisect import insort

from utils import phrase_string_to_word_list
from constituent import CompleteConstituent

class Agenda:
    
    def __init__(self, start_dict:dict, end_dict:dict, sentence:str) -> None:
        self.starts = start_dict
        self.ends = end_dict
        self.sentence_str = sentence
        self.sentence_lst = phrase_string_to_word_list(sentence)
        self.root = None
        self.num_words = len(self.sentence_lst)
        
    def constituents_starting_at_index(self, index:int) -> list[CompleteConstituent]:
        return self.starts[index]
    
    def constituents_ending_at_index(self, index:int) -> list[CompleteConstituent]:
        return self.ends[index]
    
    def get_root(self) -> CompleteConstituent:
        return self.root
    
    def set_root(self, root:CompleteConstituent) -> None:
        self.root = root
        
    def has_root(self) -> bool:
        return self.root != None
    
    
    def _insert_constituent_into_dictionary(start:bool, const:CompleteConstituent):
        pass
    
    
    def add_constituent(self, phr:CompleteConstituent) -> None:
        self.starts[phr.start_index].append(phr)
        self.ends[phr.end_index].append(phr)
        if phr.start_index == 0 and phr.end_index == self.num_words - 1:
            self.set_root(phr)
            
    def _traversal_helper(self, current_constituent:CompleteConstituent,
                          current_permutation:list[CompleteConstituent]=[]) -> list[list[CompleteConstituent]]:
        
        end_index = current_constituent.end_index
        
        current_permutation = current_permutation.copy()
        current_permutation.append(current_constituent)
        
        # If there is nothing to the right
        if end_index == len(self.sentence_lst) - 1:
            return [current_permutation]
 
 
        # Else, for each constituent starting to the index one after the end of our current
        # constituent, add a permutation
        current_constituent_permutations = []
        for next_phr in self.ends[end_index + 1]:   # For each of the constituents that start immediately after this ends
            following_permutations = self._traversal_helper(next_phr, current_permutation)  # Get list of permutations (list of phrases) 
            current_constituent_permutations.extend(following_permutations)
            
        return current_constituent_permutations
        
    
    def get_permutations(self) -> list[list[CompleteConstituent]]:
        
        permutations = []
        
        for opening_constituent in self.starts[0]:
            permutations.extend(
                self._traversal_helper(opening_constituent)
            )
            
        return permutations