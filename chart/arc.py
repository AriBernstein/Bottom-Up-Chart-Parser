from cfg.cfg_utils import get_pos_ordering
from pos_constants import PartOfSpeechConstants as pos
from chart.arc_visualizer import visualize_complete_arc_tree

class CompleteArc:
    """
    A complete phrase with 0 or many subphrases. If subsequence is none, then
    this complete arc represents a single word. 
    
    Globals:
        _pos: the part of speech this arc is validating
        
        _ordering_index: the index of the list in the ordering object that  
            his active arc is trying to complete
        
        _start_index: the index of the word in the initial sentence where this
            phrase begins
        
        _subsequence_pos_ordering: list of POS objects that represent the
            ordering this active arc is trying to complete
        
        _subsequence: list of completeArc objects representing phrases from the
            sentence whose POSs match those in _subsequence_pos_ordering
        
        _subsequence_index: lowest empty index of _subsequence """
    
    def __init__(self, words:list[str], pos:pos, input_str_start_index:int,
                 input_str_end_index:int, leaf=False, subsequence=None, 
                 ordering_index:int=None, subsequence_pos_ordering=None):
        
        self._words = words
        self._pos = pos
        self._start_index = input_str_start_index
        self._end_index = input_str_end_index
        self._leaf = leaf
        
        self._subsequence = subsequence
        self._ordering_index = ordering_index
        self._subsequence_pos_ordering = subsequence_pos_ordering
        if not leaf and (ordering_index == None or subsequence_pos_ordering == None):
            raise Exception("Only word parts of speech may have None \
                ordering_index or pos_ordering.")
    
    def get_pos(self) -> pos:
        return self._pos
    
    def get_subsequence(self) -> list:
        return self._subsequence
    
    def start_index(self) -> int:
        return self._start_index
    
    def end_index(self) -> int:
        return self._end_index
    
    def visualize(self, simple:bool=False) -> str:
        """
        Returns:
            str: each line contains the parts of speech, and subsequence 
                 orderings / words, that make up the parse tree at each level.
        """
        return visualize_complete_arc_tree(self, simple_list=simple)
    
    def __str__(self) -> str:
        if not self._leaf:
            return f"{str(self._pos).upper()} {self._subsequence_pos_ordering}"
        else:
            return f"{str(self._pos).upper()} {self._words}"
        
    def __repr__(self) -> str:
        return str(self)
    
    def __len__(self) -> int:
        return len(self._subsequence)
        
    
class ActiveArc:
    """
    An incomplete phrase with at least one subphrase (complete ard). The 
    start_index method return is final; the end_index method return changes each
    time a complete arc is added to the subsequence.
    
    Globals:
        _pos: the part of speech this arc is validating
        
        _ordering_index: the index of the list in the ordering object that  
            his active arc is trying to complete
        
        _start_index: the index of the word in the initial sentence where this
            phrase begins
        
        _subsequence_pos_ordering: list of POS objects that represent the
            ordering this active arc is trying to complete
        
        _subsequence: list of completeArc objects representing phrases from the
            sentence whose POSs match those in _subsequence_pos_ordering
        
        _subsequence_index: lowest empty index of _subsequence
    """
    def __init__(self, pos:pos, ordering_index:int,
                 input_str_start_index:int) -> None:
        self._pos = pos
        self._ordering_index = ordering_index
        self._start_index = input_str_start_index
        
        self._subsequence_pos_ordering = get_pos_ordering(pos, ordering_index)
        self._subsequence = [None] * len(self._subsequence_pos_ordering)
        self._subsequence_index = 0

    def get_pos(self) -> pos:
        return self._pos
    
    def add_to_subsequence(self, new_subphrase:CompleteArc) -> None:
        """
        Adds new complete arc to subsequence.
        
        Args:
            new_subphrase (CompleteArc): CompleteArc to be added to subsequence.
        """
        if self.validate():
            raise Exception("Cannot add to subsequence of validated active arc")
        self._subsequence[self._subsequence_index] = new_subphrase
        self._subsequence_index += 1
        
    def next_expected_pos(self) -> pos:
        """
        Returns:
            pos: the pos of the active arc for the next open space in the
                 subsequence.
        """
        return self._subsequence_pos_ordering[self._subsequence_index]
    
    def start_index(self) -> int:
        """
        Returns:
            int: the sentence index of the start of the first arc in the
                 subsequence, which correlates to a key in the
                 chart.complete_starts dictionary. """
        return self._subsequence[0].start_index()
    
    def end_index(self) -> int:
        """
        Returns:
            int: the sentence index of the end of the last-added arc in the
                 subsequence, which correlates to a key in the
                 chart.complete_ends dictionary. """
        if len(self._subsequence) == 0:
            raise Exception("Well this should never happen.")
        
        return self._subsequence[self._subsequence_index - 1].end_index()
    
    def validate(self) -> bool:
        """
        When the subsequence is fully populated, the arc is validated and can be
        converted into a CompleteArc object.
        
        Returns:
            bool: true if the subsequence of this arc is fully populated and it
                is ready to be converted into a CompleteArc. False otherwise.
        """
        # return self._subsequence_index == len(self._subsequence_pos_ordering)
        return self._subsequence[0] != None and self._subsequence[-1] != None
        
    def make_complete(self, sentence:list[str]) -> CompleteArc:
        """
        Args:
            sentence (list[str]): the list of words in the sentence that make up
                this arc.

        Returns:
            CompleteArc: The CompleteArc object from the POS, location and 
                subsequence of this Active Arc """
                
        if not self.validate():
            raise Exception("Cannot convert non-validated incomplete arc to \
                complete arc.")
        
        complete_arc_words = sentence[self.start_index():self.end_index() + 1]
        completed_arc = CompleteArc(complete_arc_words, self._pos,
                                    self.start_index(), self.end_index(),
                                    False, self._subsequence,
                                    self._ordering_index, 
                                    self._subsequence_pos_ordering)
        return completed_arc
        
    def __str__(self) -> str:
        return f"POS: {self._pos} - Ordering: {self._ordering_index} - \
            Location: {self._subsequence_index}"
    
    def __repr__(self) -> str:
        return str(self)