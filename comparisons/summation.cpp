#include <iostream>
#include <vector>
#include <chrono>

int main() {
    int size = 10000;
    
    std::vector<std::vector<double>> matrix(size, std::vector<double>(size, 1.0));

    auto start = std::chrono::high_resolution_clock::now();
    
    double total = 0;
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            total += matrix[i][j];
        }
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;

    std::cout << elapsed.count() << "s" << std::endl;
    return 0;
}