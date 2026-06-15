#include <iostream>
#include <cmath>
#include <cstdlib>
using namespace std;

void pairwise_dist(double** X, double** D, int n, int dim) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            double d = 0.0;
            for (int k = 0; k < dim; ++k) {
                double diff = X[i][k] - X[j][k];
                d += diff * diff;
            }
            D[i][j] = sqrt(d);
        }
    }
}

int main(int argc, char *argv[]) {

    int N = atoi(argv[1]);
    int K = 3;

    double** X = new double*[N];
    double** D = new double*[N];
    for (int i = 0; i < N; ++i) {
        X[i] = new double[K];
        D[i] = new double[N];
    }

    srand (static_cast <unsigned> (time(0)));
    float LO = static_cast <float> (0);
    float HI = static_cast <float> (10);

    for (int i = 0; i < N; ++i) {
        for (int k = 0; k < K; ++k) {
            X[i][k] = LO + static_cast <float> (rand()) /( static_cast <float> (RAND_MAX/(HI-LO)));; 
        }
    }

    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            D[i][j] = 0.0;
        }
    }

    pairwise_dist(X, D, N, K);    
    cout << "Done." << endl;


    for (int i = 0; i < N; ++i) {
        delete[] X[i];
        delete[] D[i];
    }
    delete[] X;
    delete[] D;

    return 0;
}