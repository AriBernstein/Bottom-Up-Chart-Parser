
def _visualize_helper(cur_root, result_dict:dict, highest_level_index:list, 
                      cur_level:int=0):
    """
    DFS to populate result_dict with:
        key -> level index [0, tree height - 1]
        pair -> ordered list of CompleteArc objects

    Args:
        cur_root ([type]): the current CompleteArc that represent a node in 
            the tree we are traversing
        
        result_dict (dict): keeps track of nodes found in traversal
        
        highest_level (list): accumulates such that, after the traversal, 
            stores the height of the tree (0 indexed). Stored as list with
            one element representing the height, such that it can be stored    
            as a reference.
        
        cur_level (int): The level of the tree in which cur_root is located.
    """
    if cur_level > highest_level_index[0]:
        highest_level_index[0] = cur_level
    
    if cur_level not in result_dict:
        result_dict[cur_level] = []
    
    result_dict[cur_level].append(cur_root)
    subsequences = cur_root.get_subsequence()
    if (subsequences):
        for arc in subsequences:
            _visualize_helper(arc, result_dict, highest_level_index, 
                              cur_level + 1)


def pad_str(this_str:str, total_length:int) -> str:
    n = len(this_str)
    
    if total_length < n:
        raise Exception(f"Total length ({total_length}) must be greater than \
            or equal to length of input string ({len(this_str)}.")
    
    if total_length == n:
        return this_str
    
    dif = total_length - n
    l_padding = r_padding = dif // 2
    if dif%2 == 1:
        r_padding += 1
    return (' ' * l_padding) + this_str + (' ' * r_padding)


def visualize_complete_arc_tree(arc, sep:str = " <||> ", 
                                simple_list:bool=False) -> str:
    """
    Constructs a string with each line displaying the parts of speech and
    their subsequence orderings that make up the parse tree at each level.
    Ordered such that children can be matched with their parents.

    Returns:
        str: each line contains the parts of speech, and subsequence 
                orderings / words, that make up the parse tree at each level.
                Ordered such that children can be matched with their parents.
    """
    heights_arcs = {}
    tree_height_index_ref = [0]
    _visualize_helper(arc, heights_arcs, tree_height_index_ref)        
    chart_height = tree_height_index_ref[0] + 1
    
    ret = ""        
    for i in range(chart_height):
        for a in heights_arcs[i]:
            ret += f"{a}{sep}"
        ret = ret[:-1 * len(sep)] + "\n\n"
    return ret
    
    
    # if simple_list:
    #     ret = ""        
    #     for i in range(chart_height):
    #         for a in heights_arcs[i]:
    #             ret += f"{a}{sep}"
    #         ret = ret[:-1 * len(sep)] + "\n"
    #     return ret
        
    # heights_lengths = {}
    # longest_arc_len = 0
    # logest_level_len = 0
    # for i in range(chart_height):
    #     len_list = []
    #     for a in heights_arcs[i]:
    #         this_arc_len = len(str(a))
    #         longest_arc_len = this_arc_len if \
    #             this_arc_len > longest_arc_len else longest_arc_len 
    #         len_list.append(this_arc_len)
    #     heights_lengths[i] = len_list
    #     longest_level_len = len(len_list) if \
    #         len(len_list) > longest_level_len else logest_level_len
    
    