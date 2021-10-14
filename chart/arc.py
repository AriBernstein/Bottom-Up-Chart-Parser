from cfg.cfg_utils import get_pos_ordering
from part_of_speech import PartOfSpeech as pos

class CompleteArc:
    
    def __init__(self, words:str, pos:pos, input_str_start_index:int,
                 input_str_end_index:int, root=False, leaf=False,
                 subsequence=None, ordering_index:int=None,
                 _subsequence_pos_ordering=None, height=0):
        self._words = words
        self._pos = pos
        self._start_index = input_str_start_index
        self._end_index = input_str_end_index
        self._root = root
        self._leaf = leaf
        self._height = height
        
        self._subsequence = subsequence
        self._ordering_index = ordering_index
        self._subsequence_pos_ordering = _subsequence_pos_ordering
        if not leaf and (ordering_index == None or _subsequence_pos_ordering == None):
            raise Exception("Only word parts of speech may have None \
                ordering_index or pos_ordering.")
    
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
    
    def _visualize_helper(self, cur_root, result_dict:dict,
                          max_height:list, cur_level:int=0):
            
            if cur_level > max_height[0]:
                max_height[0] = cur_level
            
            if cur_level not in result_dict:
                result_dict[cur_level] = []
            
            result_dict[cur_level].append(cur_root)
            subsequences = cur_root.get_subsequence()
            if (subsequences):
                for arc in subsequences:
                    self._visualize_helper(arc, result_dict,
                                           max_height, cur_level + 1)
    
    def visualize(self) -> str:
        heights = {}
        h = [0]
        self._visualize_helper(self, heights, h)        
        
        chart_height = h[0]
                
        ret = ""        
        for i in range(chart_height + 1):
            for a in heights[i]:
                ret += f" {a} |"
            ret = ret[:-1] + "\n"
        
        return ret
    
    def __str__(self) -> str:
        if not self._leaf:
            return f"{str(self._pos).upper()} - {self._subsequence_pos_ordering}"
        else:
            return f"{str(self._pos).upper()} - {self._words}"
        
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
    def __init__(self, pos:pos, cur_order:int, input_str_start_index:int) -> None:
        self._pos = pos
        self._cur_order = cur_order
        self._start_index = input_str_start_index
        
        # List of completed_arcs
        self._subsequence_pos_ordering = get_pos_ordering(self._pos, cur_order)
        self._subsequence = [None] * len(self._subsequence_pos_ordering)
        self._subsequence_index = 0


    def get_pos(self):
        return self._pos
    
    def add_to_subsequence(self, child:CompleteArc):
        if self.terminal():
            raise Exception("Cannot add to subsequence of terminal active arc")
        self._subsequence[self._subsequence_index] = child
        self._subsequence_index += 1
        
    def next_expected_pos(self) -> pos:
        return self._subsequence_pos_ordering[self._subsequence_index]
    
    def empty(self) -> bool:
        return self._subsequence_index == 0
    
    def terminal(self) -> bool:
        return self._subsequence[0] != None and self._subsequence[-1] != None

    def start_index(self) -> int:
        return self._subsequence[0].start_index()
    
    def end_index(self) -> int:
        if len(self._subsequence) == 0:
            raise Exception("Well this should never happen.")
        
        return self._subsequence[self._subsequence_index - 1].end_index()
    
    def make_complete(self, sentence:list[str]) -> CompleteArc:
        if not self.terminal():
            raise Exception("Cannot convert non-terminal incomplete arc to complete arc.")
        
        complete_arc_str = sentence[self.start_index():self.end_index() + 1]
        completed_arc = CompleteArc(complete_arc_str, self._pos, self.start_index(),
                                    self.end_index(), self._pos==pos.SENTENCE, False,
                                    self._subsequence, self._cur_order, self._subsequence_pos_ordering)
        return completed_arc
        
    def is_complete() -> bool:
        return False
        
    def __str__(self) -> str:
        return f"POS: {self._pos} - Ordering: {self._cur_order} - Location: {self._subsequence_index}"
    
    def __repr__(self) -> str:
        return str(self)