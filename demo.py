from nltk.corpus import wordnet as wn
from parse_tree.bottom_up_parser import build_tree


if __name__ == "__main__":
    # for w in ["he", "runs", "home"]:
    #     lst = wn.synsets(w)
    #     for i in range(len(lst)):
    #         print(str(lst[i].pos()))
    #     print('============')


    # pe = initial_phrase_pos_permutations("Book that flight!")
    # # print(pe)
    # for i in pe:
    #     print(i)
    
    complete_tree = build_tree("I give you a gift.")
    print(complete_tree.visualize(simple=True))
