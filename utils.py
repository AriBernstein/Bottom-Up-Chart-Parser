from nltk.corpus import wordnet as wn
from part_of_speech import PartOfSpeech
from CFG.word_constants import aux_verbs, modal_verbs, determiners, \
                               pronouns
    
def parts_of_speech(word:str) -> set:
    # n    noun 
    # v    verb 
    # a    adjective 
    # s    adjective satellite 
    # r    adverb
    # x    auxillary verb
    # m    modal verb
    # d    determiner
    # p    pronoun

    word_data = wn.synsets(word)
    part_of_speech_set = set()
    
    if word in aux_verbs:
        part_of_speech_set.add(PartOfSpeech.AUXILLARY_VERB)
        
        if word in modal_verbs:
            part_of_speech_set.add(PartOfSpeech.MODAL_VERB)
            
    if word in determiners:
        part_of_speech_set.add(PartOfSpeech.DETERMINER)
        
    if word in pronouns:
        part_of_speech_set.add(PartOfSpeech.PRONOUN)

    for i in word_data:
        p = str(i.pos())
        
        if p == 'n':
            part_of_speech_set.add(PartOfSpeech.NOUN)
        elif p == 'v':
            part_of_speech_set.add(PartOfSpeech.VERB)
        elif p == 'a':
            part_of_speech_set.add(PartOfSpeech.ADJECTIVE)
        elif p == 's':
            part_of_speech_set.add(PartOfSpeech.ADJECTIVE)
        elif p == 'r':
            part_of_speech_set.add(PartOfSpeech.ADVERB)
        else:
            raise Exception("NEW POS tag: " + p)
        
    return part_of_speech_set

if __name__ == "__main__":
    lst = wn.synsets('morning')
    for i in range(len(lst)):
        print(str(lst[i].pos()))