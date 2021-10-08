from nltk.corpus import wordnet as wn
from chart.bottom_up_parser import build_tree

if __name__ == "__main__":
    # lst = wn.synsets('morning')
    # for i in range(len(lst)):
    #     print(str(lst[i].pos()))


    # pe = initial_phrase_pos_permutations("Book that flight!")
    # # print(pe)
    # for i in pe:
    #     print(i)
    
    build_tree("Book that flight")
