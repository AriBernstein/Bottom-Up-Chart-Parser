from CFG.cfg import RULES_DICT
from part_of_speech import PartOfSpeech as pos

class CompleteArc:
    
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
    
    def get_start_index(self):
        return self.start_index
    
    def get_end_index(self):
        return self.end_index
        
    def get_children(self):
        return self.children
    
    def is_complete() -> bool:
        return True
    
    def __str__(self) -> str:
        return f"{str(self.pos).upper()} ({self.words})"
        
    def __repr__(self) -> str:
        return str(self)
    
    def __len__(self) -> int:
        return len(self.children)
    
    
class ActiveArc:
    def __init__(self, pos:pos, cur_order:int, cur_loc:int,
                 input_str_start_index:int) -> None:
        self.pos = pos
        self.cur_order = cur_order
        self.cur_loc = cur_loc
        self.start_index = input_str_start_index
        self.children = []  # List of constituents
        
    def add_ordering(self, child:CompleteArc):
        self.children.append(child)
        
    def expected_pos(self) -> pos:
        return RULES_DICT[self.pos].get_order(self.cur_order)[self.cur_loc]
    
    def empty(self) -> bool:
        return self.cur_loc == 0
    
    def terminal(self) -> bool:
        ordering_list = RULES_DICT[self.pos].get_order(self.cur_order)
        return self.cur_loc == len(ordering_list) - 1
    
    def advance(self):  # When terminal, if validated, parent becomes complete constituent
        if self.terminal():
            raise Exception("Incomplete Constituent is terminal. No constituent to advance" + str(self))
        else:
            self.cur_loc += 1
    
    def get_start_index(self):
        return self.start_index
    
    def get_end_index(self):
        if len(self.children) == 0:
            raise Exception("Well this should never happen.")
        
        return self.children[-1].get_end_index()
            
    def complete(self, sentence:list[str], input_string_end_index:int) -> CompleteArc:
        constituent_str = sentence[self.start_index:input_string_end_index + 1]
        completed_constituent = CompleteArc(constituent_str, self.pos, self.start_index,
                                                    input_string_end_index, self.pos==pos.SENTENCE, False,
                                                    self.children, self.cur_order)
        return completed_constituent
        
    def is_complete() -> bool:
        return False
        
    def __str__(self) -> str:
        return f"POS: {self.pos} - Ordering: {self.cur_order} - Location: {self.cur_loc}"
    
    def __repr__(self) -> str:
        return str(self)