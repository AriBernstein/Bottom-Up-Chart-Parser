from phrase import Phrase, PhraseChildren
from utils import get_parts_of_speech
import part_of_speech as pos
import cfg

class InProgressPhrase:
    
    def __init__(self, word_pos:pos, former_word:Phrase, parent_phrase:Phrase=None) -> None:
        self.word_pos = word_pos
        self.former_word = former_word
       
       
# def tree_helper(sentence_subset:list[str], current_phrase_ordering:list) -> Phrase:
     
     

def build_tree(phrase:str, valid_pos:set) -> Phrase:
    phrase_l = phrase.split(sep=' ')
    
    tree_root = tree_helper(pos.Sentence)
    
    for word, i in enumerate(phrase_l):
        word_pos = get_parts_of_speech(word)
        if word_pos in valid_pos:
            this_phrase = Phrase(word, word_pos)