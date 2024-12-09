import numpy as np
from math import floor

def NRZ(bit_stream):
  size = len(bit_stream)
  signal = np.zeros(size*100).astype(int)
  n = np.arange(0 , size, 0.01) # Esse é o tempo suficiente para representar o clock que é de 2Bauds
  for i in range(size*100):
    if bit_stream[floor(i/100)] == 1:
      signal[i] = 1
    else:
      signal[i] = -1
  return n, signal

def Clock(size, v0 = -1, v1 = 1):
  signal = np.zeros(size*100).astype(int)
  content = v1

  for i in range(size*100):
    if i%50 == 0:
      content = v1 if content == v0 else v0
    signal[i] = content
  return signal

def Manchester(bit_stream):

  size = len(bit_stream)

  x , y = NRZ(bit_stream)
  clock = Clock(size)
  signal = np.zeros(size*100).astype(int)

  for i in range(len(y)):
    signal[i] =  y[i] ^ clock[i]

  return x, signal
    
def Bipolar(bit_stream, v0 = -1, v1 = 1):
  size = len(bit_stream)
  signal = np.zeros(size*100).astype(int)
  content = v1
  n = np.arange(0 , size, 0.01) # Esse é o tempo suficiente para representar o clock que é de 2Bauds
  for i in range(size*100):
    if i%50 == 0:
      content = v1 if content == v0 else v0
    if bit_stream[floor(i/100)] == 1:
      signal[i] = content
    else:
      signal[i] = 0
  return n, signal


