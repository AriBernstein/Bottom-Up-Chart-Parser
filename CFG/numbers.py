import re
from word_constants import \
    cardinal_number_sets, ordinal_number_set, cardinal_numbers_zero_nineteen, \
        cardinal_numbers_twenty_ninety, cardinal_numbers_hundred_trillion

def is_cardinal_number(phrase:str) -> bool:
    # regex to find space characters and dashes
    phrase_lst = re.split(" |-", phrase)
    for word in phrase_lst:
        if not word.isnumeric() or not word in cardinal_number_sets:
            return False
    return True

def is_ordinal_number(phrase:str) -> bool:
    
    def is_ordinal_digit(digit:str) -> bool:
        if digit in ordinal_number_set:
            return True
        
        if len(digit > 2):  # eleventh -> eleven
            if (digit[-2:]) == "th":
                temp = digit[0:-2]
                if temp in cardinal_numbers_zero_nineteen:
                    return True
                if temp in cardinal_numbers_hundred_trillion:
                    return True
        
        if len(digit) > 4:  # "twentieth" -> "twenty"
            if (digit[-4:]) == "ieth":
                temp = digit[0:-4]
                temp += 'y'
                if temp in cardinal_numbers_twenty_ninety:
                    return True
        
        return False
    
    phrase_lst = re.split(" |-", phrase)
    
    for i in reversed(range(len(phrase_lst))):
        word = phrase_lst[i]
        if i == len(phrase_lst) - 1:
            if not is_ordinal_digit(word):
                return False
        else:
            if not is_cardinal_number(word):
                return False
    
    return True