from CFG.cfg import RULES_DICT
from part_of_speech import PartOfSpeech as pos

class CompleteArc:
    
    def __init__(self, words:str, pos:pos, input_str_start_index:int,
                 input_str_end_index:int, root=False, leaf=False,
                 children=None, ordering_index:int=None):
        self._words = words
        self._pos = pos
        self._start_index = input_str_start_index
        self._end_index = input_str_end_index
        self._root = root
        self._leaf = leaf
        self.children = children
        self.ordering_index = ordering_index
        
        if not leaf and ordering_index == None:
            raise Exception("Only word parts of speech may have None ordering_index.")
    
    def get_pos(self) -> pos:
        return self._pos
    
    def get_order(self) -> list[pos]:
        ret = []
        for ph in self.ordering:
            ret.append(ph.pos)
        return ret
    
    def get_words(self) -> str:
        return self._words
    
    def is_word(self) -> bool:
        return self._leaf
    
    def start_index(self) -> int:
        return self._start_index
    
    def end_index(self) -> int:
        return self._end_index
        
    def get_children(self) -> list:
        return self.children
    
    def is_complete() -> bool:
        return True
    
    def __str__(self) -> str:
        return f"{str(self._pos).upper()} ({self._words})"
        
    def __repr__(self) -> str:
        return str(self)
    
    def __len__(self) -> int:
        return len(self.children)
    
    
class ActiveArc:
    def __init__(self, pos:pos, cur_order:int, cur_loc:int,
                 input_str_start_index:int) -> None:
        self._pos = pos
        self._cur_order = cur_order
        self._cur_loc = cur_loc
        self._start_index = input_str_start_index
        self._children = []  # List of constituents

    def get_pos(self):
        return self._pos
    
    def add_ordering(self, child:CompleteArc):
        self._children.append(child)
        
    def expected_pos(self) -> pos:
        return RULES_DICT[self._pos].get_order(self._cur_order)[self._cur_loc]
    
    def empty(self) -> bool:
        return self._cur_loc == 0
    
    def terminal(self) -> bool:
        ordering_list = RULES_DICT[self._pos].get_order(self._cur_order)
        return self._cur_loc == len(ordering_list) - 1
    
    def advance(self):  # When terminal, if validated, parent becomes complete constituent
        if self.terminal():
            raise Exception("Incomplete Constituent is terminal. No constituent to advance" + str(self))
        else:
            self._cur_loc += 1
    
    def get_start_index(self):
        return self._start_index
    
    def get_end_index(self):
        if len(self._children) == 0:
            raise Exception("Well this should never happen.")
        
        return self._children[-1].get_end_index()
            
    def complete(self, sentence:list[str], input_string_end_index:int) -> CompleteArc:
        constituent_str = sentence[self._start_index:input_string_end_index + 1]
        completed_constituent = CompleteArc(constituent_str, self._pos, self._start_index,
                                                    input_string_end_index, self._pos==pos.SENTENCE, False,
                                                    self._children, self._cur_order)
        return completed_constituent
        
    def is_complete() -> bool:
        return False
        
    def __str__(self) -> str:
        return f"POS: {self._pos} - Ordering: {self._cur_order} - Location: {self._cur_loc}"
    
    def __repr__(self) -> str:
        return str(self)