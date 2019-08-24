"""
@author:husan
@date 2019-08-24 00:06
"""
import json
from pandas import DataFrame, Series
import pandas as pd; import numpy as np
import matplotlib.pyplot as plt

unames = ['user_id','gender','age','occupation','zip']
users = pd.read_table('dataset/users.dat',sep='::', header=None, names=unames, engine='python')

rnames = ['user_id','movie_id','rating','timestamp']
ratings = pd.read_table('dataset/ratings.dat', sep='::', header=None, names = rnames, engine='python')

mnames = ['movie_id','title','genres']
movies = pd.read_table('dataset/movies.dat', sep='::', header=None, names = mnames, engine='python')

data = pd.merge(pd.merge(ratings,users), movies)
mean_ratings = data.pivot_table('rating', index='title', columns='gender', aggfunc='mean')
print(mean_ratings[:5])