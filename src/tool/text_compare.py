#encoding: utf-8
"""
@Auther: husan
@Date: 2019/8/24 09:53

"""
from fuzzywuzzy import fuzz
l  = list()
l1 = list()
l2 = list(range(2))
print(l2)
l = l + l1+ l2
print(l)
#
# p1 = "文三路133号恒升花苑1幢104、105室"
# p2 = "恒升花苑1栋"
# p3 = "恒升花苑"
# print(fuzz.ratio(p1,p2))
# print(fuzz.partial_ratio(p1,p2))
# print(fuzz.token_sort_ratio(p1,p2))
# print(fuzz.token_set_ratio(p1,p2))
# print(fuzz.partial_token_set_ratio(p1,p2))
#
#
# print(fuzz.ratio(p1,p3))
# print(fuzz.partial_ratio(p1,p3))
# print(fuzz.token_sort_ratio(p1,p3))
# print(fuzz.token_set_ratio(p1,p3))
# print(fuzz.partial_token_set_ratio(p1,p3))

