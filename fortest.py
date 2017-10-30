import numpy as np

axis = np.float32([[0,0,0], [0,1,0], [1,1,0], [1,0,0],
                   [0,0,-1],[0,1,-1],[1,1,-1],[1,0,-1] ])

arr = np.arange(0.0, 8.0, 0.5)
for i in arr:
  print i
