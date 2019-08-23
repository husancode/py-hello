"""
@author:husan
@date 2019-08-23
"""
from collections import  defaultdict

def counts(sequence):
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] = counts[x] +1
        else:
            counts[x] = 1
    return counts

def counts2(sequence):
    counts = defaultdict(int)
    for x in sequence:
        counts[x] +=1
    return counts

def top_counts(count_dict, n=10):
    pair = [(count, tz) for tz,count in count_dict.items()]
    pair.sort()
    return pair[-n:]