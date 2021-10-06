from parse_tree import ParseTree
from phrase import Phrase
import re
from nltk.corpus import wordnet as wn
from part_of_speech import PartOfSpeech
from word_constants import aux_verbs, modal_verbs, determiners, \
                           pronouns

def lower_case_plain_text(phrase_str:str) -> str:
    return re.sub(r"[:;!?/,]", "", phrase_str).lower()

def phrase_string_to_word_list(phrase_str:str) -> list[str]:
    return lower_case_plain_text(phrase_str).split(' ')

def get_parts_of_speech(word:str) -> set:
    # n    noun 
    # v    verb 
    # a    adjective 
    # s    adjective satellite 
    # r    adverb
    # x    auxillary verb
    # m    modal verb
    # d    determiner
    # p    pronoun
    
    # Remove commas, colons, semicolons, slashes
    word = re.sub(r'[,:;/!]',"", word)

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
            raise Exception(f"Cannot find POS for tag: {p}, word: {word}.")
        
    return part_of_speech_set

def initial_phrase_pos_permutations(sentence:str) -> set[list[Phrase]]:
    permutations = [[]]
    
    starts, ends = {}, {}
    
    for i, word in enumerate(sentence.split(sep=' ')):
        word = re.sub(r"[:;!?/,]", "", word).lower()
        word_pos = get_parts_of_speech(word.lower())
        updated_permutations = []
        starts[i] = []
        ends[i] = []
        # For each existing permutation, add 
        for pos in word_pos:
            for perm in permutations:
                updated_ordering = perm.copy()
                new_word_phrase = Phrase(word, pos, i, i, False, True)
                updated_ordering.append(new_word_phrase)
                updated_permutations.append(updated_ordering)
                starts[i].append(new_word_phrase)
                ends[i].append(new_word_phrase)
                
        permutations = updated_permutations
    
    return permutations, ParseTree(starts, ends)

if __name__ == "__main__":
    # lst = wn.synsets('morning')
    # for i in range(len(lst)):
    #     print(str(lst[i].pos()))


    # pe = initial_phrase_pos_permutations("Book that flight!")
    # # print(pe)
    # for i in pe:
    #     print(i)
        
    # x = incomplete_phrases_starting_with(PartOfSpeech.VERB_PHRASE)
    # for i in x:
    #     print(i)
    pass