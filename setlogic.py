def tunnel_to_destination(path, into={}):
    this_section=into
    for index in path:
        if index not in this_section:
            this_section[index]={}
        this_section=this_section[index]
    return into

def dict_remove_from_paths(into, *paths):
    """
    Dictionary removal that accepts slices as arguments. Useful for dumping 
    out sub-dimensions of a dictionary when managing a huge structure.
        - Create a path for each key to be removed
        - Ensure entire path exists within structure
        - Remove path
    >>> dict_remove_from_paths({0:1, 1:{1:2, 2:3}, 2:{1:2, 2:3}}, (0,2))
    {1: {1: 2, 2: 3}}
    >>> dict_remove_from_paths({0:1, 1:{1:2, 2:3}, 2:{1:2, 2:3}}, (1,2), (1,))
    {0: 1, 1: {2: 3}, 2: {2: 3}}
    """
    def paths_from_list(paths, sofar=()):
        if paths:
            for path in paths[0]:
                for x in paths_from_list(paths[1:], sofar+(path,)):
                    yield x
        else:
            yield sofar
    def ensure_subpath_exists(into, path):
        this_subsection=into
        for elem in path:
            if elem in this_subsection:
                this_subsection=this_subsection[elem]
            else:
                return False
        return True
    for path in paths_from_list(paths):
        if ensure_subpath_exists(into, path):
            this_subsection=into
            for elem in path[:-1]:
                this_subsection=this_subsection[elem]
            del this_subsection[path[-1]]
    return into

def dict_remove(into, _from):
    """
    Dict-remove that removes a dict from another dict, less usable than slice
    remove for personal use but for removing diffs this is what is necessary.
    >>> dict_remove({0:1, 1:{1:2, 2:3}, 2:{1:2, 2:3}}, {1:{1:2}})
    {0: 1, 1: {2: 3}, 2: {1: 2, 2: 3}}
    >>> dict_remove({0:1, 1:{1:2, 2:3}, 2:{1:2, 2:3}}, {1:{1:2, 2:3}, 2:{1:2}})
    {0: 1, 1: {}, 2: {2: 3}}
    """
    for path, val in create_paths(_from):
        this_section=into
        for index in path[:-1]:
            if index not in this_section:
                break
            this_section=this_section[index]
        if this_section[path[-1]]==val:
            del this_section[path[-1]]
    return into

def dict_insert(into, _from):
    """
    Proper dictionary insert that inserts at the deepest possible level as
    opposed to the lowest possible level as is with dict.update().
    For example, {0: {1: 2}}.update({0: {3: 4}}) completely removes the {1: 2}
    pair in favour of {3: 4}. Insert overwrites values at the deepest level such
    that {0: {1: 2}}.insert({0: {1: 3}}) would still replace {1: 2} with {1: 3} 
    but in the case of the initial example, would instead return 
    {0: {1: 2, 3: 4}}.
    >>> dict_insert({0:{1:2}}, {0:{3:4}})
    {0: {1: 2, 3: 4}}
    >>> dict_insert({0:{1:2}}, {0:{1:3}})
    {0: {1: 3}}
    >>> dict_insert({0:{1:2}}, {0:{1:3, 3:4}})
    {0: {1: 3, 3: 4}}
    """
    for path, val in create_paths(_from):
        this_section=into
        for index in path[:-1]:
            if index not in this_section:
                this_section[index]={}
            this_section=this_section[index]
        this_section.update({path[-1]:val})
    return into

def create_paths(d, path=()):
    """
    Breaks a dict into path - value pairs.
    Recursively descends into a dict structure yielding path-value pairs as
    they are discovered for every leaf in the structure. This has the quality
    of returning nothing for a dict with no leaves such as {0: {1: {}}}.
    >>> dict(create_paths({0: {1: {5: {20: {}}}}}))
    {}
    >>> dict(create_paths({0: {1: 2, 3: {4: 5}}, 6: 7}))
    {(0, 1): 2, (0, 3, 4): 5, (6,): 7}
    """
    for k,v in d.items():
        if isinstance(v, type({})):
            for iterable in create_paths(v, path+(k,)):
                yield iterable
        else:
            yield path+(k,),v
