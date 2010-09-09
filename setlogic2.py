def tunnel_to_destination(path, into={}):
    this_section=into
    for index in path:
        if index not in this_section:
            this_section[index]={}
        this_section=this_section[index]
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
    Properly structured dicts will return something similar to the following:
        {0: {1: 2, 3: {4: 5}}, 6: 7} -> {(0, 1): 2, (0, 3, 4): 5, (6,): 7}
    """
    for k,v in d.items():
        if isinstance(v, type({})):
            for iterable in create_paths(v, path+(k,)):
                yield iterable
        else:
            yield path+(k,),v

def dict_diff(a, b, path=[]):
    def create_subdict_from_path(segment={}, path=[]):
        for leaf in path[::-1]:
            segment={leaf:segment}
        return segment
    def remainder_of(source, condition):
        return {k:v for k,v in source.items() if condition(k,v)}
    def is_iterable(v):
        iterable_types=[type(c) for c in ((), [], {}, set())]
        return type(v) in iterable_types
    def fix_types(t):
        if type(t) in (type(c) for c in ((), [], set())):
            return {k:v for k,v in enumerate(t)}
        else:
            return t
    a,b=fix_types(a),fix_types(b)
    non_iterable_a=remainder_of(a, lambda k,v: not is_iterable(v))
    non_iterable_b=remainder_of(b, lambda k,v: not is_iterable(v))
    iterable_a=remainder_of(a, lambda k,v: is_iterable(v))
    iterable_b=remainder_of(b, lambda k,v: is_iterable(v))
    non_iterable_diff=non_iterable_a.items()^non_iterable_b.items()
    added_non_iterables=dict(non_iterable_diff&non_iterable_b.items())
    removed_non_iterables=dict(non_iterable_diff&non_iterable_a.items())
    all_removed=create_subdict_from_path(removed_non_iterables, path)
    all_added=create_subdict_from_path(added_non_iterables, path)
    if iterable_a.keys() | iterable_b.keys():
        for key in iterable_a.keys() | iterable_b.keys():
            removed, added=dict_diff(iterable_a.get(key, {}), iterable_b.get(key, {}), path+[key])
            dict_insert(all_added, added)
            dict_insert(all_removed, removed)
        return all_removed, all_added
    else:
        return all_removed, all_added

sa={'a':'b', 'b':'c', 'd':[1,2,3,4, {'haha':'this is some nested shit', 'lol':['its', 'really', 'nested']}], 'e':{'f':'g', 'h':'l'}, 'f':'g'}
sb={'a':'b', 'b':'b', 'd':[1,3,2], 'e':{'f':'f'}, 'g':'i'}

