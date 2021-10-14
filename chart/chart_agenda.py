from collections import deque

from chart.arc import CompleteArc, ActiveArc
from part_of_speech import PartOfSpeech as pos

class Chart:
    
    def __init__(self, sentence:str) -> None:
        self.sentence_str = sentence
        
        self.sentence_lst = sentence.split(' ')
        self.roots = set()
        
        self.num_words = len(self.sentence_lst)
        self.complete_starts = {}
        self.complete_ends = {}
        self.incomplete_starts = {}
        self.incomplete_ends = {}
        
        for i in range(self.num_words):
            self.complete_starts[i] = set()
            self.complete_ends[i] = set()
            self.incomplete_starts[i] = set()
            self.incomplete_ends[i] = set()
        
    def arcs_starting_at_index(self, index:int) -> list[CompleteArc]:
        return self.complete_starts[index]
    
    def arcs(self, index:int) -> list[CompleteArc]:
        return self.complete_ends[index]
    
    def get_roots(self) -> CompleteArc:
        return self.roots
    
    def add_root(self, root:CompleteArc) -> None:
        self.roots.add(root)
        
    def has_root(self) -> bool:
        return len(self.roots) > 0
    
    def word_length(self) -> int:
        return len(self.sentence_lst)
    
    def add_complete_arc(self, arc:CompleteArc) -> None:
        self.complete_starts[arc.start_index()].add(arc)
        self.complete_ends[arc.end_index()].add(arc)
        if arc.get_pos() == pos.SENTENCE and \
            arc.start_index() == 0 and arc.end_index() == self.num_words - 1:
            self.add_root(arc)
    
    def add_active_arc(self, arc: ActiveArc) -> None:   
        self.incomplete_starts[arc.start_index()].add(arc)
        self.incomplete_ends[arc.end_index()].add(arc)
        
    def update_active_arc(self, arc: ActiveArc, old_end_index:int):
        """
        Only ever called after arc has been updated. 

        Args:
            arc (ActiveArc): TODO
            old_end_index (int): TODO
        """
        self.incomplete_ends[old_end_index].remove(arc)
        self.incomplete_ends[arc.end_index()].add(arc)
        
    def remove_active_arc(self, arc: ActiveArc, end_index_in_chart:int):
        self.incomplete_starts[arc.start_index()].remove(arc)
        self.incomplete_ends[end_index_in_chart].remove(arc)
    
    def __str__(self) -> str:
        ret = ""
        for sentence in self.get_roots():
            ret += str(sentence) + "\n"
        return ret
    
    def visualize(self) -> str:
        ret = ""
        for r in self.roots:
            ret += f"{r.visualize()}\n\n"
            
        return ret
        
class Agenda:
    def __init__(self, word_arcs:deque[CompleteArc]) -> None:
        self._arc_stack = word_arcs
        
    def push(self, new_arc:CompleteArc) -> None:
        self._arc_stack.append(new_arc)
        
    def pop(self) -> CompleteArc:
        return self._arc_stack.pop()
    
    def empty(self) -> bool:
        return len(self._arc_stack) == 0
    
    def __sizeof__(self) -> int:
        return self._arc_stack.qsize()