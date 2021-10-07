from CFG.parse_cfg import build_tree
from nltk.corpus import wordnet as wn

if __name__ == "__main__":
    # lst = wn.synsets('morning')
    # for i in range(len(lst)):
    #     print(str(lst[i].pos()))


    # pe = initial_phrase_pos_permutations("Book that flight!")
    # # print(pe)
    # for i in pe:
    #     print(i)
    
    build_tree("Book that flight")
