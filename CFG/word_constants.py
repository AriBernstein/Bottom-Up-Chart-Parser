aux_verbs = set(
    ["be", "can", "could", "dare", "do", "have", "may", "might",
     "must", "need", "ought", "shall", "should", "will", "would"])

modal_verbs = set(
    ["can", "could", "may", "might", "must", "shall", "should",
     "will", "would"])

determiners = set(
    ["few", "fewer", "fewest", "every", "most", "that", "little",
     "half", "much", "the", "other", "her", "my", "a", "an", "his",
     "neither", "these", "all", "its", "no", "this", "any","those",
     "both", "least", "our", "their", "what", "each", "less",
     "several", "which", "either", "many","some", "whose", "enough",
     "more", "such", "your"])

pronouns = set(
    ["I", "we", "you", "he", "she", "it", "they", "me", "us", "you",
     "her", "him", "it", "them"])


# Numbers:
# Cardinal Numbers:
cardinal_numbers_zero_nineteen = set(
    ["zero", "one", "two", "three", "four", "five", "six", "seven", 
     "eight", "nine", "ten", "eleven", "twelve", "thirteen",
     "forteen", "fifteen", "sixteen", "seventeen", "eighteen",
     "nineteen"])

cardinal_numbers_twenty_ninety = set(
    ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", 
     "eighty", "ninety"])

cardinal_numbers_hundred_trillion = set(
    ["hundred", "thousand", "million", "billion", "trillion"])

cardinal_number_sets = set.union(
    [cardinal_numbers_zero_nineteen,
     cardinal_numbers_twenty_ninety,
     cardinal_numbers_hundred_trillion])

# Ordinal numbers
ordinal_number_set = set(
    ["first", "second", "third", "forth", "fifth", "sixth", "seventh",
     "eighth", "ninth"])