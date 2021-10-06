from typing import List
from CFG.cfg import RULES_DICT
from part_of_speech import PartOfSpeech as pos

class Phrase:
    
    def __init__(self, phrase:str, pos:pos, root=False, leaf=False, child_ordering=None):
        self.phrase = phrase   
        self.root = root
        self.pos = pos
        self.leaf = leaf
        self.next = None
        self.prev = None
        self.children = child_ordering
        
    def get_order(self) -> list[pos]:
        ret = []
        for ph in self.ordering:
            ret.append(ph.pos)
        return ret
    
    def is_word(self):
        return self.leaf
    
    def get_children(self):
        return self.children
    
    def __str__(self) -> str:
        return f"{str(self.pos).upper()}({self.phrase})>"
        
    def __repr__(self) -> str:
        return str(self)
    
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
        
class PhraseProgress:
    def __init__(self, phrase_type:pos, cur_order:int, cur_loc:int) -> None:
        self.phrase_type = phrase_type
        self.cur_order = cur_order
        self.cur_loc = cur_loc
        self.children = []  # List of completed phrases
        self.current_child = None
        
    def add_ordering(self, child:Phrase):
        self.children.append(child)
    
    def set_current_child(self, child):
        self.current_child = child
        
    def terminal(self):
        ordering_list = RULES_DICT[self.phrase_type].get_ordering(self.cur_order)
        return self.cur_loc == len(ordering_list) - 1
    
    def advance(self):  # When terminal, if validated, parent becomes phrase
        if self.terminal():
            raise Exception("No next subphrase for phraseProgress" + str(self))
        else:
            self.cur_loc += 1
    
    def phrase_text(self):
        ret = ""
        for ph in self.children:
            ret += ph.phrase + ' '
        
    def get_phrase(self) -> Phrase:
        return Phrase(self.phrase_text(), self.phrase_type==pos.SENTENCE, self.phrase_type)
        
    def __str__(self) -> str:
        return f"POS: {self.phrase_type}\tOrdering: {self.cur_order}\tLocation: {self.cur_loc}"