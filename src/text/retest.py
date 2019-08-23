import re
pattern = '.end'
p = re.compile(pattern)
print(re.search(r'\bThe', 'Th e dd The'))