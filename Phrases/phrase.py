from part_of_speech import PartOfSpeech
from phrase_children import PhraseChildren
class Phrase:
    
    def __init__(self, phrase:str, pos:PartOfSpeech, root=False):
        self.phrase = phrase   
        self.root = root
        self.pos = pos
        
        # SET of lists of PhraseChildren
        # self.syntactic_reps  = construct_bottom_up_parse_trees(phrase)
        
        