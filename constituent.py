from CFG.cfg import RULES_DICT
from part_of_speech import PartOfSpeech as pos

class Constituent:
    
    def __init__(self, words:str, pos:pos, input_str_start_index:int,
                 input_str_end_index:int, root=False, leaf=False,
                 children=None, ordering_index:int=None):
        self.words = words
        self.pos = pos
        self.start_index = input_str_start_index
        self.end_index = input_str_end_index
        self.root = root
        self.leaf = leaf
        self.children = children
        self.ordering_index = ordering_index
        
        if not leaf and ordering_index == None:
            raise Exception("Only word parts of speech may have None ordering_index.")
        
    def get_order(self) -> list[pos]:
        ret = []
        for ph in self.ordering:
            ret.append(ph.pos)
        return ret
    
    def get_words(self):
        return self.words
    
    def is_word(self):
        return self.leaf
    
    def get_children(self):
        return self.children
    
    def is_complete() -> bool:
        return True
    
    def __str__(self) -> str:
        return f"{str(self.pos).upper()} ({self.words})"
        
    def __repr__(self) -> str:
        return str(self)
    
    def __len__(self):
        return len(self.children)
    
    
class IncompleteConstituent:
    def __init__(self, pos:pos, cur_order:int, cur_loc:int,
                 input_str_start_index:int) -> None:
        self.phrase_type = pos
        self.cur_order = cur_order
        self.cur_loc = cur_loc
        self.start_index = input_str_start_index
        self.children = []  # List of completed phrases
        
    def add_ordering(self, child:Constituent):
        self.children.append(child)
        
    def expected_phrase(self) -> pos:
        return RULES_DICT[self.phrase_type].get_order(self.cur_order)[self.cur_loc]
    
    def empty(self) -> bool:
        return self.cur_loc == 0
    
    def terminal(self) -> bool:
        ordering_list = RULES_DICT[self.phrase_type].get_order(self.cur_order)
        return self.cur_loc == len(ordering_list) - 1
    
    def advance(self):  # When terminal, if validated, parent becomes phrase
        if self.terminal():
            raise Exception("No next subphrase for phraseProgress" + str(self))
        else:
            self.cur_loc += 1
            
    def complete(self, sentence:list[str], input_string_end_index:int) -> Constituent:
        phrase_str = sentence[self.start_index:input_string_end_index + 1]
        new_phrase = Constituent(phrase_str, self.phrase_type,
                            self.start_index,
                            input_string_end_index,
                            self.phrase_type==pos.SENTENCE, False,
                            self.children, self.cur_order)
        return new_phrase
    
    def is_complete() -> bool:
        return False
        
    def __str__(self) -> str:
        return f"POS: {self.phrase_type} - Ordering: {self.cur_order} - Location: {self.cur_loc}"
    
    def __repr__(self) -> str:
        return str(self)