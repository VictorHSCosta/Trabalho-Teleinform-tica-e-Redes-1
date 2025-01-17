import numpy as np
from math import floor

import numpy as np
from math import floor

class SignalGeneratorDigital:
    def __init__(self):
        self.bit_stream = []
        self.Vmin = -1
        self.Vmax = 1
        self.size = 0
        self.pointsNumber = 100
        self.time = 0

    #setup methods

    def setBitStream(self, bit_stream):
        self.bit_stream = bit_stream
        self.size = len(bit_stream)
        self.time = np.arange(0, self.size, 1/self.pointsNumber)

    def setV(self, V):
        self.Vmin = -V
        self.Vmax = V

    def setPointsNumber(self, pointsNumber):
        self.pointsNumber = pointsNumber
        self.time = np.arange(0, self.size, 1/self.pointsNumber)


    def NRZ(self):
        
        content = 0
        aux = 0
        signal = np.zeros(self.size * self.pointsNumber).astype(int)

        for i in range(self.size):
            if self.bit_stream[i] == 1:
                content = self.Vmax
            else:
              content = self.Vmin
            for j in range(self.pointsNumber):
                signal[aux] = content
                aux += 1

        return self.time, signal

    def Clock(self):

        signal = np.zeros(self.size * 100).astype(int)

        content = self.Vmax
        for i in range(self.size * 100):
            if i % 50 == 0:
                content = self.Vmax if content == self.Vmin else self.Vmin
            signal[i] = content
        return signal

    def Manchester(self):

        n, y = self.NRZ()
        clock = self.Clock()

        signal = np.zeros(self.size * 100).astype(int)
        for i in range(len(y)):
            signal[i] = self.Vmin if (y[i] ^ clock[i]) == 0 else self.Vmax
        return n, signal

    def Bipolar(self):

        signal = np.zeros(self.size * 100).astype(int)
        content = self.Vmin
        multiplicador = 1
        aux = 0

        for i in range(self.size):
            
            if ((self.bit_stream[i] == 1) and (content == self.Vmin)):
                multiplicador = self.Vmax
                content = self.Vmax
            elif ((self.bit_stream[i] == 1) and (content == self.Vmax)):
                multiplicador = self.Vmin
                content = self.Vmin
            else:
                multiplicador = 0

            for j in range(100):
                signal[aux] = multiplicador
                aux += 1

        return self.time, signal


