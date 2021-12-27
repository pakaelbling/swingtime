import matplotlib.pyplot as plt
from PIL import Image
from datetime import datetime

class regressionPredictor():
    def __init__(self,initialData, alpha):
        self.data = initialData
        self.alpha = alpha

    def predict(self, key):
        pass

    def addDatum(self, key, val):
        pass

    def setAlpha(self,a):
        self.alpha = a

    def makePredictionChart(self, filename):
        day = datetime.today().weekday()
        x = range(0,540,5)
        y = [self.predict((minute, day)) for minute in x]
        ticks = range(0,540,30)
        tickLabels = [f"{(11 + tick // 60) if (11 + tick // 60) < 13 else (11 + tick // 60) - 12}:{str(tick%60).zfill(2)}" for tick in ticks]
        plt.rcParams['figure.figsize'] = (11,6)
        plt.clf()
        plt.scatter(x,y)
        plt.xlabel("Arrival Time")
        plt.ylabel('Predicted Wait Time (in minutes)')
        plt.xticks(ticks, tickLabels)
        plt.savefig(filename)

class naiveNearestNeighbor(regressionPredictor):
    def __init__(self, distFun, alpha, initialData = None):
        if initialData is None:
            super().__init__({}, alpha)
        else:
            super.__init__(initialData, alpha)
        self.distFun = distFun

    def predict(self, key):
        minDist = float('inf')
        minKey = None
        for k in self.data:
            dist = self.distFun(k, key)
            if dist < minDist:
                minDist = dist
                minKey = k
        return self.data[minKey]

    def addDatum(self, key, val):
        currVal = self.data.get(key)
        if currVal is None:
            self.data[key] = val
        else:
            self.data[key] = currVal + self.alpha * (val - currVal)
        self.makePredictionChart('wteSite/static/chart.png')

class nNearestNeighbor(naiveNearestNeighbor):
    def __init__(self, distFun, alpha, n, initialData = None):
        super().__init__(distFun, alpha, initialData)
        self.n = n

    def predict(self, key):
        if len(self.data) < self.n:
            return super().predict(key)
        else:
            dist = [(self.distFun(k, key), self.data[k]) for k in self.data]
            nMin = sorted(dist, key=lambda x:x[0])[:self.n]
            sum = 0
            for (key, v) in nMin:
                sum += v
            return round(sum / self.n, 2)






