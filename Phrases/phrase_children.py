from typing import List
from part_of_speech import PartOfSpeech
from phrase import Phrase

class PhraseChildren:
    def __init__(self, ordering:List[Phrase]) -> None:
        self.ordering = ordering
        
    def __iter__(self):
        for ph in self.ordering:
            yield ph
    
    def __add__(self, o):
        if o is type(list):
            ret = self.ordering[:]
            ret.extend(o)
            return ret
        elif o is type(PhraseChildren):
            ret = self.ordering[:]
            ret.extend(o.ordering)
            return ret
        else:
            raise Exception("adding invalid type: " + str(type(o)))
        
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