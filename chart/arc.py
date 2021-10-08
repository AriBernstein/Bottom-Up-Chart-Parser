from CFG.cfg_utils import get_pos_ordering
from part_of_speech import PartOfSpeech as pos

class CompleteArc:
    
    def __init__(self, words:str, pos:pos, input_str_start_index:int,
                 input_str_end_index:int, root=False, leaf=False,
                 subsequence=None, ordering_index:int=None):
        self._words = words
        self._pos = pos
        self._start_index = input_str_start_index
        self._end_index = input_str_end_index
        self._root = root
        self._leaf = leaf
        self._subsequence = subsequence
        self._ordering_index = ordering_index
        
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
        
    def get_subsequence(self) -> list:
        return self._subsequence
    
    def is_complete() -> bool:
        return True
    
    def __str__(self) -> str:
        return f"{str(self._pos).upper()} ({self._words})"
        
    def __repr__(self) -> str:
        return str(self)
    
    def __len__(self) -> int:
        return len(self._subsequence)
    
    
class ActiveArc:
    """
    
    
    Globals:
        _pos (pos): [description]
        _cur_order (int): [description]
        _cur_loc (int): [description]
        _end_index (int): [description]
    """
    def __init__(self, pos:pos, cur_order:int, cur_loc:int,
                 input_str_end_index:int) -> None:
        self._pos = pos
        self._cur_order = cur_order
        self._cur_loc = cur_loc
        self._end_index = input_str_end_index
        
        # List of completed_arcs
        self._subsequence = [None] * len(get_pos_ordering(self._pos, cur_order))

    def get_pos(self):
        return self._pos
    
    def add_to_subsequence(self, child:CompleteArc):
        if self.terminal():
            raise Exception("Cannot add to subsequence of terminal active arc")
        self._subsequence[self._cur_loc] = child
        self._advance()
        
    def expected_pos(self) -> pos:
        return get_pos_ordering(self.get_pos(), self._cur_order)[self._cur_loc]
        # return RULES_DICT[self._pos].get_order(self._cur_order)[self._cur_loc]
    
    def empty(self) -> bool:
        return self._cur_loc == len(self._subsequence) - 1
    
    def terminal(self) -> bool:
        return self._cur_loc == 0 and self._subsequence[0] != None
    
    def _advance(self):  # When terminal, if validated, parent becomes complete constituent
        if self.terminal():
            raise Exception("Active Arc is terminal. No constituent to advance" + str(self))
        else:
            self._cur_loc -= 1
    
    def start_index(self):
        return self._subsequence[self._cur_loc + 1].start_index()
    
    def end_index(self):
        if len(self._subsequence) == 0:
            raise Exception("Well this should never happen.")
        
        return self._subsequence[-1].end_index()
    
    def complete(self, sentence:list[str]) -> CompleteArc:
        if not self.terminal():
            raise Exception("Cannot convert non-terminal incomplete arc to complete arc.")
        
        constituent_str = sentence[self.start_index:self.end_index() + 1]
        completed_constituent = CompleteArc(constituent_str, self._pos, self.start_index(),
                                            self.end_index(), self._pos==pos.SENTENCE, False,
                                            self._subsequence, self._cur_order)
        return completed_constituent
        
    def is_complete() -> bool:
        return False
        
    def __str__(self) -> str:
        return f"POS: {self._pos} - Ordering: {self._cur_order} - Location: {self._cur_loc}"
    
    def __repr__(self) -> str:
        return str(self)