import numpy as np

def ask(A, f , bit_stream):
  size = len(bit_stream)
  signal = np.zeros(size*100)
  t = np.arange(0, size*100 ,1/100)
  
  for i in range(size):
    for j in range(100):
      signal[j*i] = 1
        
     
    

  return t , signal
    

