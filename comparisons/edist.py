import random
import sys

N = int(sys.argv[1])
K = 3
X = [[10*random.random() for _ in range(K)] for _ in range(N)]
D = [[0.0] * N for _ in range(N)]

def pairwise_dist(X, D, size, dim):
    for i in range(size):
        for j in range(size):
            d = 0.0
            for k in range(dim):
                d += (X[i][k] - X[j][k]) ** 2
            D[i][j] = d ** 0.5

pairwise_dist(X, D, N, K)
print("Done.")