from typing import List
from CFG.cfg import RULES_DICT
from part_of_speech import PartOfSpeech as pos

class Phrase:
    
    def __init__(self, phrase:str, pos:pos, input_string_start_index:int,
                 input_string_end_index:int, root=False, leaf=False,
                 children=None, prev=None, ordering_index:int=None):
        self.phrase = phrase
        self.pos = pos
        self.input_str_start_index = input_string_start_index
        self.input_str_end_index = input_string_end_index
        self.root = root
        self.leaf = leaf
        self.next = set()
        self.prev = prev
        self.children = children
        self.ordering_index = ordering_index
        
        if not leaf and ordering_index == None:
            raise Exception("Only word parts of speech may have None ordering_index.")
        
    def get_order(self) -> list[pos]:
        ret = []
        for ph in self.ordering:
            ret.append(ph.pos)
        return ret
    
    def is_word(self):
        return self.leaf
    
    def get_children(self):
        return self.children
    
    def has_prev(self) -> bool:
        if self.prev != None:
            if len(self.prev) > 0:
                return True
        return False
    
    def has_next(self):
        return len(self.next) > 0
    
    def add_next(self, next_phr) -> None:
        self.next.add(next_phr)
    
    def __str__(self) -> str:
        return f"{str(self.pos).upper()} ({self.phrase}) | "
        
    def __repr__(self) -> str:
        return str(self)
    
    def __len__(self):
        return len(self.children)
    
    
class IncompletePhrase:
    def __init__(self, phrase_type:pos, cur_order:int, cur_loc:int,
                 input_str_start_index:int) -> None:
        self.phrase_type = phrase_type
        self.cur_order = cur_order
        self.cur_loc = cur_loc
        self.input_string_start_index = input_str_start_index
        self.children = []  # List of completed phrases
        self.prev = None
        self.next = None
        
    def add_ordering(self, child:Phrase):
        self.children.append(child)
        
    def expected_phrase(self) -> pos:
        return RULES_DICT[self.phrase_type].get_order(self.cur_order)[self.cur_loc]
    
    def empty(self) -> bool:
        return self.cur_loc == 0
    
    def terminal(self) -> bool:
        ordering_list = RULES_DICT[self.phrase_type].get_ordering(self.cur_order)
        return self.cur_loc == len(ordering_list) - 1
    
    def advance(self):  # When terminal, if validated, parent becomes phrase
        if self.terminal():
            raise Exception("No next subphrase for phraseProgress" + str(self))
        else:
            self.cur_loc += 1
    
    def phrase_text(self):
        ret = ""
        for ph in self.children:
            ret += ph.phrase + ' '
        
    def complete(self, end_index:int) -> Phrase:
        new_phrase = Phrase(self.phrase_text(), self.phrase_type,
                            
                            self.phrase_type==pos.SENTENCE, False,
                            self.children, self.prev, self.cur_order)
        
        # Add as next val to each of prev
        for prev_phr in new_phrase.prev:
            prev_phr.add_next(new_phrase)
            
        return new_phrase
        
    def set_prev(self, prior_phrase_set:set[Phrase]) -> None:
        self.prev = prior_phrase_set
        
    def __str__(self) -> str:
        return f"POS: {self.phrase_type} - Ordering: {self.cur_order} - Location: {self.cur_loc}|"
    
    def __repr__(self) -> str:
        return str(self)