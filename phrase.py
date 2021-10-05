from typing import List
from part_of_speech import PartOfSpeech

class Phrase:
    
    def __init__(self, phrase:str, pos:PartOfSpeech, root=False, terminal=False):
        self.phrase = phrase   
        self.root = root
        self.pos = pos
        terminal = False
        if terminal:
            pass
        else:
            self.child_orderings = None
        
    def get_order(self) -> list[PartOfSpeech]:
        ret = []
        for ph in self.ordering:
            ret.append(ph.pos)
            
        return ret
    
    
class PhraseChildren:
    def __init__(self, ordering:List[Phrase]) -> None:
        self.ordering = ordering
        
    def __iter__(self):
        for ph in self.ordering:
            yield ph
            
    def __str__(self) -> str:
        ret = ""
        for i, phrase in enumerate(self.ordering):
            ret = ret + str(phrase)
            if i < len(self.ordering) - 1:
                ret = ret + " -> "
        return ret
    
class PhraseSet:
    def __init__(self, children_set=set()) -> None:
        self.children = children_set