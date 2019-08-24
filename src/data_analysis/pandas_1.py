
"""
@author:husan
@date 2019-08-23 22:36
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.Series(np.random.randn(1000), index = np.arange(1000))
data = data.cumsum()
data.plot()
plt.show()