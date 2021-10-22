# Python Implementation of a Bottom-Up-Chart-Parser

Given a valid English sentence, the bottom up chart parser will use the context-free grammar to construct a parse tree starting at its leaves and ending at its root.

## Methodology:
### Context-Free Grammar (CFG):
A context-free grammar is a set of recursively-defined rules, each representing a *variation* of a part of speech. Each rule is a key-pair value; the key represents a POS; the pair an ordered sequence of POSs that *validate* the POS of the key (in arc-form, these sequences are referred to as subsequences). Some rules are terminal; they have no children and generally represent a single word, and as such do not have sequences. For non-terminal rules, there is a one to many relationship between POSs and validating ordered sequences. In other words, in most CFGs designed to represent English, there will be multiple rules for the same POS, each correlating with a unique validating sequence.

### Chart Parsing:
Chart parsing is the process of converting a sentence into one or many parse trees. Parse tree nodes correlate to CFG rules. Each node is contains a POS and ordered list of children (referred to as its subsequence). The number of children is equal to the number of POSs in the ordered sequence of its rule. Leaves have no children and represent individual words (terminal CFG rules).

Given a CFG, there are two primary methods for parsing a phrase into a parse tree: top-down chart parsing and bottom-up chart parsing. Bottom-up chart parsing builds the tree beginning with the leaves and ending at the root. While less intuitive than top-down parsing, it is known to be faster and avoids issues like left-recursion.

## Implementation:

### Some terminology:
- **Arc:** A structure which represents a substring in the initial sentence in the context of a specific grammar rule. Arcs can be either complete or active. Note: complete arcs can be used as nodes in the parse tree.
    - Complete Arc: an arc which represents a grammar rule that is known to exist over a substring of the input sentence (ie. its subsequence is populated). Complete arcs are used when constructing Active Arcs.
    - Active Arc: an arc which represents a grammar rule for which some of its subsequence has been discovered.
- **Chart:** A structure which stores, for a given sentence, all possible parse trees as well as all discovered parts of speech that did not make it into rooted trees.
    - Rooted Tree: A Complete Arc which spans the entire sentence and is of POS sentence.
- **Agenda:** A stack which temporarily stores newly-completed arcs. It is used to avoid repetition. 
- **Word-index:** Given a sentence in the form of an ordered list such that each element represents a word in the string, a word-index means the location of a given word in its greater sentence.


### pos_constants.py
A tuple containing all labels for all parts of speech recognized by the context free grammar. Instances of this class will be hereafter referred to as POS.

### demo&#46;py
Just a file with a main and a sentence string that prints a visualization of the parse tree.

### CFG:
**cfg&#46;py**
- Defines *Ordering* class:
    - Represents a grammar rule; a POS which can be created using multiple subsequences of POSs. It can also be a terminal rule such that it represents a single word and does not contain any subsequences.
    - Contains a POS P, which represents the POS created using one of the subsequences.
    - Contains a list of lists of POSs; each 2nd-level list represents a subsequence which would validate this rule.
- Contains a script which builds orderings that define the rules for the CFG. These rules are added to dictionaries for fast comparison when parsing a sentence. 

**cfg_utils.py** 
- Contains helpful methods for parsing the string-format sentence into initial terminal complete (single-word) arcs.

**numbers&#46;py**
- Utilities to recognize numeric parts of speech.
- Uses sets from word_constants to look for characters or substrings that indicate different numeric types.
- Numeric types recognized:
    - Cardinal numbers, ex. "4", "four", "forty-four", "4 million, two hundred and twenty thousand, five hundred.".
    - Ordinal numbers, ex. "1st", "first", "3rd", "third", "4th", "fourth", "forty-fifth", "10 millionth ".

**word_constants.py**
- Contains hard coded sets of words that correlate with terminal parts of speech.

### Chart:
**arc_visualizer.py**
- Contains methods for visualization of a parse tree rooted at a given CompleteArc.

**arc&#46;py**
- Contains classes CompleteArc and ActiveArc
- CompleteArc:
    - Contains a POS object.
    - Contains rule-ordering information.
    - Contains complete or nonexistent (if terminal) subsequence of CompleteArc objects.
    - Methods for getting its location in the initial sentence string.
- ActiveArc:
    - Contains a POS object.
    - Contains rule-ordering information.
    - Contains an incomplete but non-empty subsequence.
    - Methods for getting its current location in initial string (end-index is dynamic; it changes when a the subsequence is updated).
    - Methods for validation (checking subsequence completeness) and conversion to CompleteArc.

**chart_agenda.py**
- Contains classes Chart and Agenda
- Chart:
    - Contains two sets of two dictionaries, one for complete arcs, the other for active arcs. In each set, one dictionary has keys correlating with the starting word-index of CompleteArcs and pairs that are sets of all such CompleteArcs, the other dictionary is similar except that the keys correlate with ending word-indexes. In the other set, the same is true but the sets contain ActiveArcs.
    - Contains methods for updating ActiveArcs - ie. moving them from one location in the ending-index dictionary to another.
- Agenda:
    - A stack of newly created CompleteArcs. See bottom_up_parser.py section.

**bottom_up_parser.py**
- Contains methods for constructing the parse tree. Instantiates an Agenda with all of the terminal parts of speech created from individual words in the input sentence. Instantiates an empty chart. Uses the CompletedArcs in the Agenda to build ActiveArcs, complete ActiveArcs, and parse sentence into tree.
