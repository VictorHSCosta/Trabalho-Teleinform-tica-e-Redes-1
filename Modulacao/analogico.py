import numpy as np

class SignalGeneratorAnalogic:
    def __init__(self):
      self.Amplitude = 1
      self.Frequency = 1
      self.Frequency2 = 2
      self.bit_stream = []
      self.size = 0
      self.time = 0
      self.pointsNumber = 100
      self.signalAsk = []

    #os 3 metodos abaixo sao a configuracao inicial para usar o sistema de modulacao 
    def SetBitStream(self, bit_stream):
        self.bit_stream = bit_stream
        self.size = len(bit_stream)
        self.time = np.arange(0, self.size, 1/self.pointsNumber)

    def SetAmplitude(self, Amplitude):
        self.Amplitude = Amplitude

    def SetPointsNumber(self, pointsNumber):
        self.pointsNumber = pointsNumber
        self.time = np.arange(0, self.size, 1/self.pointsNumber) 

    def SetFrequency(self, Frequency):
        self.Frequency = Frequency

    def SetFrequency2(self, Frequency):
        self.Frequency2 = Frequency

    def Ask(self):
        aux = 0 
        signal = np.zeros(self.size * self.pointsNumber).astype(float)

        for i in range(self.size):
            if self.bit_stream[i] == 1:
                for i in range(100):
                    signal[aux] = self.Amplitude * np.sin(2 * np.pi * self.Frequency * self.time[aux])
                    aux += 1
            else:
                for i in range(100):
                    signal[aux] = 0
                    aux += 1
                    
        self.signalAsk = signal

        return self.time, signal              

    def getAsk(self):
        return self.time, self.signalAsk
    
    def FSK(self):

        aux = 0 
        signal = np.zeros(self.size * self.pointsNumber).astype(float)

        for i in range(self.size):
            if self.bit_stream[i] == 1:
                for i in range(100):
                    signal[aux] = self.Amplitude * np.sin(2 * np.pi * self.Frequency2 * self.time[aux])
                    aux += 1
            else:
                for i in range(100):
                    signal[aux] = self.Amplitude * np.sin(2 * np.pi * self.Frequency * self.time[aux])
                    aux += 1
                    
        return self.time, signal
    
    def getFSK(self):
        return self.time, self.signalFSK
    
    def PSK(self):
        aux = 0
        signal = np.zeros(self.size * self.pointsNumber).astype(float)

        for i in range(self.size):

            if self.bit_stream[i] == 1:
                for i in range(100):
                    signal[aux] = self.Amplitude * np.sin(2 * np.pi * self.Frequency * self.time[aux])
                    aux += 1
            else:
                for i in range(100):
                    signal[aux] = self.Amplitude * np.sin(2 * np.pi * self.Frequency * self.time[aux]  + np.pi)
                    aux += 1
        
        return self.time, signal