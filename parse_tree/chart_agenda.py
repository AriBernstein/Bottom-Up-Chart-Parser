from collections import deque

from parse_tree.arc import CompleteArc, ActiveArc
from pos_constants import PartOfSpeechConstants as pos

class Chart:
    """
    Chart representation of a parse tree.
    
    Stores all known phrases (CompleteArcs) in sentences in a set of two
    dictionaries which contain references to the same CompleteArcs:
        complete_starts: key -> sentence index
                         pair -> list of CompleteArcs which begin at key
        
        complete_ends: key -> sentence index
                       pair -> list of CompleteArcs which end at key 
                       
    Stores all potential phrases (ActiveArcs) in another set of two
    dictionaries which share references to the same ActiveArcs:
        incomplete_starts: key -> sentence index
                           pair -> list of ActiveArcs which begin at key
                           
        incomplete_ends: key -> sentence index
                         pair -> list of ActiveArcs which end at key
                         
    Other fields:
        _sentence_str (str): the complete sentence in string form
        
        _sentence_lst (list[str]): a list with each index containing a word in
            the sentence (with punctuation/symbols left intact)
       
        _num_words (int): number of words in the sentence
       
        _roots (set[CompleteArc]): a set of completeArc objects which have a POS
            of sentence and span the entire sentence.
    
    """
    def __init__(self, sentence:str) -> None:
        self._sentence_str = sentence
        self._sentence_lst = sentence.split(' ')
        self._num_words = len(self._sentence_lst)
        self._roots = set()
        
        self.complete_starts = {}
        self.complete_ends = {}
        self.incomplete_starts = {}
        self.incomplete_ends = {}
        
        for i in range(self._num_words):
            self.complete_starts[i] = set()
            self.complete_ends[i] = set()
            self.incomplete_starts[i] = set()
            self.incomplete_ends[i] = set()
        
    def arcs_starting_at_index(self, index:int) -> list[CompleteArc]:
        return self.complete_starts[index]

    def get_roots(self) -> CompleteArc:
        return self._roots
    
    def add_root(self, root:CompleteArc) -> None:
        self._roots.add(root)
        
    def has_root(self) -> bool:
        return len(self._roots) > 0
    
    def word_length(self) -> int:
        return len(self._sentence_lst)
    
    def add_complete_arc(self, arc:CompleteArc) -> None:
        """
        Add a new complete arc to the chart. Check if root.
        
        Args:
            arc (CompleteArc): newly validated/created CompleteArc 
        """
        self.complete_starts[arc.start_index()].add(arc)
        self.complete_ends[arc.end_index()].add(arc)
        if arc.get_pos() == pos.SENTENCE and \
            arc.start_index() == 0 and arc.end_index() == self._num_words - 1:
            self.add_root(arc)
    
    def add_active_arc(self, arc: ActiveArc) -> None:
        """
        Add a new active arc to the chart

        Args:
            arc (ActiveArc): newly created ActiveArc
        """
        self.incomplete_starts[arc.start_index()].add(arc)
        self.incomplete_ends[arc.end_index()].add(arc)
        
    def update_active_arc(self, arc: ActiveArc, old_end_index:int):
        """
        Moves reference to arc from set at incomplete_ends[old_end_index] to
        to the set at incomplete_ends[arc.end_index()]. Only ever called after 
        arc has been updated (which will update the return value of calls to its
        end_index method). 

        Args:
            arc (ActiveArc): the arc to move
            old_end_index (int): the key in incomplete_ends at which to find arc
        """
        self.incomplete_ends[old_end_index].remove(arc)
        self.incomplete_ends[arc.end_index()].add(arc)
        
    def remove_active_arc(self, arc: ActiveArc, end_index:int):
        """
        Once validated, we can remove the "completed" ActiveArc from the 
        incomplete arc dictionaries
        
        Args:
            arc (ActiveArc): the arc to remove
            end_index (int): the key in incomplete_ends at which to find arc
        """
        self.incomplete_starts[arc.start_index()].remove(arc)
        self.incomplete_ends[end_index].remove(arc)
    
    def visualize(self, simple:bool = False) -> str:
        """
        For each complete arc in root, append the output of said complete arc's
        visualize method to a string.

        Returns:
            str: a string with visualizations stemming from every Complete Arc 
                 in the roots set.
        """
        
        ret = f"\nInput:\t{self._sentence_str}\n\n"
        for r in self._roots:
            ret += f"{r.visualize(simple=simple)}\n--------------\n"    
        return ret
    
    def __str__(self) -> str:
        ret = ""
        for sentence in self.get_roots():
            ret += str(sentence) + "\n"
        return ret
    
        
class Agenda:
    """
    Stack containing newly-completed CompleteArcs to be used in constructing 
    parse tree.
    """
    def __init__(self, word_arcs:list[CompleteArc]) -> None:
        self._arc_stack = deque(word_arcs)
        
    def push(self, new_arc:CompleteArc) -> None:
        self._arc_stack.append(new_arc)
        
    def pop(self) -> CompleteArc:
        return self._arc_stack.pop()
    
    def empty(self) -> bool:
        return len(self._arc_stack) == 0
    
    def __str__(self) -> str:
        return str(self._arc_stack)