from nearestNeighbor import naiveNearestNeighbor, nNearestNeighbor

def numDist(x, y):
    return abs(x - y)

def naiveNNTests():
    naiveNN = naiveNearestNeighbor(numDist, alpha=0.8, initialData={1 : 1, 2 : 2, 3 : 3})
    assert naiveNN.predict(4) == 3
    naiveNN.addDatum(4, 4)
    assert naiveNN.predict(4) == 4
    naiveNN.addDatum(4, 5)
    assert naiveNN.predict(4) == 4.8

def nNNTests():
    nNN = nNearestNeighbor(numDist, alpha=0.8, n=3, initialData={1 : 1, 2 : 2, 3 : 3})
    assert nNN.predict(4) == 2.0
    nNN.addDatum(4,4)
    assert nNN.predict(4) == 3.0
    nNN.addDatum(4,5)
    assert nNN.predict(4) == 3.27


if __name__ == '__main__':
    naiveNNTests()
    nNNTests()
