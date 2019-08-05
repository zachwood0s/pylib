import functools
import numbers
import collections
import itertools
from pylib.utils import require

class Range(object):
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def includes(self, num):
        return self.lower <= num <= self.upper

class Underscore(object):
    def __repr__(self):
        return "_"

    def __getitem__(self, key):
        return key

_ = Underscore()
PATTERNS = []
DEFAULT = (False, [])

def pattern(pat):
    def wrapper(handler):
        PATTERNS.append((pat, handler))
        return handler
    return wrapper

#################
#   Patterns    #
#################

@pattern(lambda pat: isinstance(pat, type))
def match_type(incoming, pat):
    matched = isinstance(incoming, pat)
    return matched, [incoming]


@pattern(lambda pat: isinstance(pat, numbers.Number))
def match_number(incoming, pat):
    matched = incoming == pat
    return matched, []


@pattern(lambda pat: pat == _)
def match_any(incoming, pat):
    return True, [incoming]


@pattern(lambda pat: isinstance(pat, collections.Sequence))
@require(lambda i, p: type(i) == type(p), DEFAULT)
@require(lambda i, p: len(i) == len(p), DEFAULT)
def match_sequence(incoming, pat):
    matches = [is_match(*x) for x in zip(incoming, pat)]
    matched = all(x for x, _ in matches)
    args = itertools.chain.from_iterable(x for _, x in matches)
    return matched, list(args)


@pattern(lambda pat: callable(pat))
def match_callable(incoming, pat):
    matched = pat(incoming)
    return matched, [incoming]


@pattern(lambda pat: isinstance(pat, Range))
@require(lambda i, _: isinstance(i, numbers.Number), DEFAULT)
def match_range(incoming, pat):
    matched = pat.includes(incoming)
    return matched, [incoming]


####################
#   Match Logic    #
####################

def run(handler, incoming, args):
    if callable(handler):
        if len(args) > 0:
            return handler(*args)
        return handler(incoming)
    return handler

def match(incoming, *handlers):
    for m, handler in handlers:
        matched, args = is_match(incoming, m)
        if matched:
            return run(handler, incoming, args)

def is_match(incoming, matcher):
    for p, h in PATTERNS:
        if p(matcher):
            return h(incoming, matcher)
    return DEFAULT

def factorial(n):
    return match(
        n,
        (Range(0, 1), 1),
        (_, lambda _: n * factorial(n - 1))
    )

print(factorial(5))

def fibanocci(n):
    return match(
        n,
        (Range(1, 2), 1),
        (_, lambda x: fibanocci(x-1) + fibanocci(x-2))
    )

print(fibanocci(6))

def all_pats(val):
    return match(
        val,
        ([1, 2, _],         lambda x: x),
        ([1, [2, 3], 4],    lambda x: x),
        (1,                 lambda x: x),
        (float,             lambda x: x),
        (callable,          lambda x: x)
    )

print(all_pats([1, 2, 4, 5]))
print(all_pats([1, 2, [1, 2, 3]]))
print(all_pats([1, [2, 3], 4]))
print(all_pats(1))
print(all_pats(20.0))
print(all_pats(lambda x: x+4)(0))

print(type(_[1:2]))
