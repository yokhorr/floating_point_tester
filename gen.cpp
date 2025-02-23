// Copyright (c) 2024 Egor Solyanik
// 
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.


#include <cfenv>
#include <iostream>
#include <random>
#include <iomanip>
#include <bitset>
#include <chrono>

using namespace std;

mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());

char setRounding(const string &roundings, mt19937& rng) {
    uniform_int_distribution<int> dist(0, roundings.length() - 1);
    char c = roundings[dist(rng)];
    switch (c) {
        case '0':
            fesetround(FE_TOWARDZERO);
            break;
        case '1':
            fesetround(FE_TONEAREST);
            break;
        case '2':
            fesetround(FE_UPWARD);
            break;
        case '3':
            fesetround(FE_DOWNWARD);
            break;
    }
    return c;
}

char chooseOperation(const string &operations, mt19937& rng) {
    uniform_int_distribution<int> dist(0, operations.length() - 1);
    return operations[dist(rng)];
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        cerr << "Usage: " << argv[0] << " <roundings> <operations> <iterations>" << endl;
        return 1;
    }

    string roundings = argv[1];
    string operations = argv[2];
    const unsigned long long iterations = stoll(argv[3]);

    for (unsigned long long i = 0; i < iterations; ++i) {
        for (char c : roundings) {
            if (c != '0' && c != '1' && c != '2' && c != '3') {
                cerr << "Error: invalid rounding type " << c << endl;
                return 1;
            }
        }

        for (char c : operations) {
            if (c != '+' && c != '-' && c != '*' && c != '/') {
                cerr << "Error: invalid operation " << c << endl;
                return 1;
            }
        }

        float A;
        float B;

        // Set the bits of A and B manually
        union {
            float f;
            uint32_t i;
        } u_A, u_B;
        uniform_int_distribution<uint32_t> dist(0, 0xFFFFFFFF);
        u_A.i = dist(rng);
        u_B.i = dist(rng);
        A = u_A.f;
        B = u_B.f;

        char rounding = setRounding(roundings, rng);
        char operation = chooseOperation(operations, rng);

        float result = 0;
        switch (operation) {
            case '+':
                result = A + B;
                break;
            case '-':
                result = A - B;
                break;
            case '*':
                result = A * B;
                break;
            case '/':
                result = A / B;
                break;
        }

        // Print the result as a hexadecimal value
        union {
            float f;
            uint32_t i;
        } u_result;
        u_result.f = result;

        cout << "f " << rounding << " 0x" << hex << setfill('0') << setw(8) << u_A.i;
        cout << " ";
        if (operation == '*') {
            cout << "\"*\"";
        } else {
            cout << operation;
        }
        cout << " 0x" << hex << setfill('0') << setw(8) << u_B.i << " # ";
        cout << "0x" << hex << uppercase << setfill('0') << setw(8) << u_result.i << endl;
    }

    

    return 0;
}
