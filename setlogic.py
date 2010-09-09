a=set([1, 2, 3])
b=set([1, 2])

class BigboySets(set):
    def own(self, other):
        diff=self^other
        return {'removed':self&diff, 'added':other&diff}

welp=BigboySets([1,2,3,4])


def _own_xor(sa,sb):
    """
    We need to make some assumptions; everything is a dict- or should be a dict.
    Lists get transformed into dictlist which is just an enumerated .items()
    We can then step through this process. 
        diff keys and create two categories:
            different keys, same keys
        Diff same keys' vals to get two more categories:
            different vals, same vals
        Should now have three distinct categories:
            different keys
            different vals
            same key (and val)
    """
    a,b=sa.copy(),sb.copy()
    same_keys={k:v for k,v in sa.keys() if k in sb.keys()}
    different_keys={k:v for k,v in sa.keys() if k not in sb.keys()}


class OwnDict(dict):
    def __xor__(self, other):
        try:
            return self.items()^other.items()
        except:
            return 'welpfuck'

def differ(a,b):
    result={}
    for elem in a:
        if not b.get(elem) or b.get(elem)!=a.get(elem):
            result[elem]=a.get(elem)
    return result

def both(a, b, path=[]):
    def diff_from_source(diff, source, *sources):
        source=source.copy()
        for s in sources:
            source.update(s)
        return dict(zip(diff, (source.get(k) for k in diff)))
    def create_subdict_from_path(segment={}, path=[]):
        for leaf in path[::-1]:
            segment={leaf:segment}
        return segment
    def remainder_of(source, condition):
        return {k:v for k,v in source.items() if condition(k,v)}
    def is_iterable(v):
        iterable_types=[type(c) for c in ((), [], {})]
        return type(v) in iterable_types
    def fix_types(t):
        if type(t) in (type(c) for c in ((), [], set())):
            return {k:v for k,v in enumerate(t)}
        else:
            return t
    a,b=fix_types(a),fix_types(b)
    keydiff=a.keys()^b.keys()
    key_and_val_diff=diff_from_source(keydiff, a, b)
    added_keydict=diff_from_source(keydiff&b.keys(), b)
    removed_keydict=diff_from_source(keydiff&a.keys(), a)
    remainder_a=remainder_of(a, lambda k,v: k not in keydiff)
    remainder_b=remainder_of(b, lambda k,v: k not in keydiff)
    non_iterable_a=remainder_of(remainder_a, lambda k,v: not is_iterable(v))
    non_iterable_b=remainder_of(remainder_b, lambda k,v: not is_iterable(v))
    print(non_iterable_a)
    print(non_iterable_b)
    ta,tb=remainder_of(a, lambda k,v: not is_iterable(v)), remainder_of(b, lambda k,v: not is_iterable(v))
    print('ta tb:', ta,tb)
    print('ta xor tb: ', ta.items()^tb.items())
    iterable_a=remainder_of(remainder_a, lambda k,v: is_iterable(v))
    iterable_b=remainder_of(remainder_b, lambda k,v: is_iterable(v))
    non_iterable_diff=non_iterable_a.items()^non_iterable_b.items()
    added_non_iterables=dict(non_iterable_diff&non_iterable_b.items())
    removed_non_iterables=dict(non_iterable_diff&non_iterable_a.items())
    all_removed, all_added={}, {}
    print('removed: ', removed_non_iterables, removed_keydict)
    print('added: ', added_non_iterables, added_keydict)
    for remove in (r for r in (removed_non_iterables, removed_keydict) if r):
        all_removed.update(create_subdict_from_path(remove, path))
    for add in (a for a in (added_non_iterables, added_keydict) if a):
        all_added.update(create_subdict_from_path(add, path))
    print('a: ', a)
    print('b: ', b)
    print('all_removed: ', all_removed)
    print('all_added: ', all_added)
    if iterable_a.keys()&iterable_b.keys():
        for key in iterable_a.keys()&iterable_b.keys():
            removed, added=both(iterable_a.get(key, {}), iterable_b.get(key, {}), path+[key])
            all_added.update(added)
            all_removed.update(removed)
        return all_removed, all_added
    else:
        return all_removed, all_removed





aa=OwnDict({'a':'b'})
bb=OwnDict({'c':'d'})

sa={'a':'b', 'b':'c', 'd':[1,2,3,4], 'e':{'f':'g', 'h':'l'}, 'f':'g'}
sb={'a':'b', 'b':'b', 'd':[1,3,2], 'e':{'f':'f'}, 'g':'i'}

