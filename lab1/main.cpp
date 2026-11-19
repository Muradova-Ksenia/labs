#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <string>
#include <iomanip>

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

    if (argc < 3) {
        cerr << "Использование: " << argv[0] << " <matrixA.txt> <matrixB.txt>" << endl;
        return 1;
    }

    string fileA = argv[1];
    string fileB = argv[2];

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

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            for (int k = 0; k < n; ++k) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);


    cout << "TIME_CPP: " << duration.count() / 1000000.0 << endl;
    cout << "SIZE: " << n << endl;


    string outFilename = "result_cpp_" + to_string(n) + ".txt";
    writeMatrix(outFilename, C);

    return 0;
}