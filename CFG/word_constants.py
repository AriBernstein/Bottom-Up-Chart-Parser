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

relative_pronouns = set(
    ['who', 'whom', 'whose', 'which', 'that']
)

coordinators = set(
    ['for', 'and', 'nor', 'but', 'or', 'yet', 'so'])

prepositions = set(
    ['aboard', "about", "above", "across", "after", "against", "along",
     "amid", "among", "anti", "around", "as", "at", "away", "before", 
     "behind", "below", "beneath", "beside", "besides", "between", 
     "beyond", "but", "by", "concerning", "considering", "despite", 
     "down", "during", "except", "excepting", "excluding", "following", 
     "for", "from", "in", "inside", "into", "like", "minus", "near", 
     "of", "off", "on", "onto", "opposite", "outside", "over", "past",
     "per", "plus", "regarding", "round", "save", "since", "than", 
     "through", "to", "toward", "towards", "under", "underneath", 
     "unlike", "until", "up", "upon", "versus", "via", "with", "within",
     "without"])

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

cardinal_number_sets = set().union(
    *[cardinal_numbers_zero_nineteen,
      cardinal_numbers_twenty_ninety,
      cardinal_numbers_hundred_trillion])

# Ordinal numbers
ordinal_number_set = set(
    ["first", "second", "third", "forth", "fifth", "sixth", "seventh",
     "eighth", "ninth"])