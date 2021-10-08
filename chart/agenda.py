from chart.arc import CompleteArc, ActiveArc

class Agenda:
    
    def __init__(self, start_dict:dict, end_dict:dict, sentence:str) -> None:
        self.starts = start_dict
        self.ends = end_dict
        self.sentence_str = sentence
        self.sentence_lst = sentence.split(' ')
        self.roots = set()
        self.num_words = len(self.sentence_lst)
        
    def arcs_starting_at_index(self, index:int) -> list[CompleteArc]:
        return self.starts[index]
    
    def arcs(self, index:int) -> list[CompleteArc]:
        return self.ends[index]
    
    def get_roots(self) -> CompleteArc:
        return self.roots
    
    def add_root(self, root:CompleteArc) -> None:
        self.roots.add(root)
        
    def has_root(self) -> bool:
        return len(self.root) > 0
    
    def add_arc(self, arc:CompleteArc) -> None:
        self.starts[arc.get_start_index()].append(arc)
        self.ends[arc.get_end_index()].append(arc)
        if arc.get_start_index() == 0 and arc.get_end_index() == self.num_words - 1:
            self.add_root(arc)
            
    def _traversal_helper(self, current_arc:CompleteArc,
                          current_permutation:list[CompleteArc]=[]) -> list[list[CompleteArc]]:
        
        end_index = current_arc.get_end_index()
        
        current_permutation = current_permutation.copy()
        current_permutation.append(current_arc)
        
        # If there is nothing to the right
        if end_index == len(self.sentence_lst) - 1:
            return [current_permutation]
 
 
        # Else, for each arc starting to the index one after the end of our current arc, add a permutation
        current_arc_permutations = []
        for next_arc in self.ends[end_index + 1]:   # For each of the arcs that start immediately after this ends
            following_permutations = self._traversal_helper(next_arc, current_permutation)  # Get list of permutations (list of phrases) 
            current_arc_permutations.extend(following_permutations)
            
        return current_arc_permutations
        
    
    def get_permutations(self) -> list[list[CompleteArc]]:
        
        permutations = []
        
        for opening_arcs in self.starts[0]:
            permutations.extend(
                self._traversal_helper(opening_arcs)
            )
            
        return permutations
    
    
class Chart(Agenda):
    
    def __init__(self, start_dict: dict, end_dict: dict, sentence: str) -> None:
        super().__init__(start_dict, end_dict, sentence)
        self.incomplete_starts = {}
        self.incomplete_ends = {}
    
    def add_complete_arc(self, arc: CompleteArc) -> None:
        return super().add_arc(arc)
    
    def add_incomplete_arc(self, arc: ActiveArc) -> None:
        start_index, end_index = arc.get_start_index(), arc.get_end_index()
        if not start_index in self.incomplete_starts:
            self.incomplete_starts[start_index] = set()
        if not end_index in self.incomplete_ends:
            self.incomplete_ends[end_index] = set()
            
        self.incomplete_starts[arc.get_start_index()].add(arc)
        self.incomplete_ends[arc.get_end_index()].add(arc)
        
    def update_incomplete_arc(self, arc: ActiveArc, old_end_index:int):
        self.incomplete_ends[old_end_index].remove(arc)
        self.incomplete_ends[arc.get_end_index()].add(arc)