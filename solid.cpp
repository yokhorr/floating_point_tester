// SPDX-License-Identifier: MIT
// 
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
#include <iomanip>
#include <bitset>
#include <cstdint>
#include <cmath>

using namespace std;

void setRounding(char c) {
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
}

int main(int argc, char *argv[]) {
    setRounding(argv[2][0]);
    char operation = argv[4][0];

    union {
        float f;
        uint32_t i;
    } u_A, u_B;

    u_A.i = stoul(argv[3], nullptr, 16);
    u_B.i = stoul(argv[5], nullptr, 16);

    float A = u_A.f;
    float B = u_B.f;

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

    cout << hex << showbase << hexfloat << result << " ";
    cout << "0x" << noshowbase << uppercase << setw(8) << setfill('0');
    cout << u_result.i << endl;

    return 0;
}
