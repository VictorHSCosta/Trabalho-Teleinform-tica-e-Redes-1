import numpy as np
from math import floor

import numpy as np
from math import floor

class SignalGenerator:
    def __init__(self, bit_stream, V):
        self.bit_stream = bit_stream
        self.v0 = -V
        self.v1 = V
        self.size = len(bit_stream)
        self.pointsNumber = 100
        self.time = np.arange(0, self.size, 1/self.pointsNumber)

    def setBitStream(self, bit_stream):
        self.bit_stream = bit_stream
        self.size = len(bit_stream)
        self.time = np.arange(0, self.size, 1/self.pointsNumber)

    def setV(self, V):
        self.Vmin = V
        self.Vmax = -V

    def setPointsNumber(self, pointsNumber):
        self.pointsNumber = pointsNumber
        self.time = np.arange(0, self.size, 1/self.pointsNumber)

    def NRZ(self):
        
        content = 0
        aux = 0
        signal = np.zeros(self.size * self.pointsNumber).astype(int)

        for i in range(self.size):
            if self.bit_stream[i] == 1:
                content = self.v1
            else:
              content = self.v0
            for j in range(self.pointsNumber):
                signal[aux] = content
                aux += 1

        return self.time, signal

    def Clock(self):
        signal = np.zeros(self.size * 100).astype(int)
        content = self.v1
        for i in range(self.size * 100):
            if i % 50 == 0:
                content = self.v1 if content == self.v0 else self.v0
            signal[i] = content
        return signal

    def Manchester(self):
        n, y = self.NRZ()
        clock = self.Clock()
        signal = np.zeros(self.size * 100).astype(int)
        for i in range(len(y)):
            signal[i] = y[i] ^ clock[i]
        return n, signal

    def Bipolar(self):
        signal = np.zeros(self.size * 100).astype(int)
        content = self.v0
        aux = 0

        for i in range(self.size):
            content = self.v1 if self.bit_stream[i] == 1 and content == self.v0 else self.v0
            for j in range(100):
                signal[aux] = content
                aux += 1

        return self.time, signal


