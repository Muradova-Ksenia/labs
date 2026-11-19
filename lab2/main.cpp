#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <string>
#include <iomanip>
#include <omp.h>

using namespace std;
using namespace std::chrono;

vector<vector<double>> readMatrix(const string& filename, int& n) {
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Ошибка: не удалось открыть файл " << filename << endl;
        exit(1);
    }
    file >> n;
    vector<vector<double>> matrix(n, vector<double>(n));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            file >> matrix[i][j];
        }
    }
    return matrix;
}

void writeMatrix(const string& filename, const vector<vector<double>>& matrix) {
    ofstream file(filename);
    int n = matrix.size();
    file << n << "\n";
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            file << matrix[i][j] << " ";
        }
        file << "\n";
    }
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        cerr << "Использование: " << argv[0] << " <matrixA.txt> <matrixB.txt> <threads>" << endl;
        return 1;
    }

    string fileA = argv[1];
    string fileB = argv[2];
    int num_threads = atoi(argv[3]);

    omp_set_num_threads(num_threads);

    int n = 0;
    vector<vector<double>> A = readMatrix(fileA, n);
    int nB = 0;
    vector<vector<double>> B = readMatrix(fileB, nB);

    if (n != nB) {
        cerr << "Ошибка: размеры матриц не совпадают!" << endl;
        return 1;
    }

    vector<vector<double>> C(n, vector<double>(n, 0.0));

    auto start = high_resolution_clock::now();

    #pragma omp parallel for collapse(2) schedule(static)
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            double sum = 0.0;
            for (int k = 0; k < n; ++k) {
                sum += A[i][k] * B[k][j];
            }
            C[i][j] = sum;
        }
    }

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);

    cout << "TIME_CPP: " << duration.count() / 1000000.0 << endl;
    cout << "SIZE: " << n << endl;
    cout << "THREADS: " << num_threads << endl;

    string outFilename = "result_cpp_" + to_string(n) + "_" + to_string(num_threads) + ".txt";
    writeMatrix(outFilename, C);

    return 0;
}