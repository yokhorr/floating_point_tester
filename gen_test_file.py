# Copyright (c) 2024 Egor Solyanik
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import subprocess
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, required=True, metavar='FILE', help='Output file')
    parser.add_argument('-n', type=int, required=True, metavar='NUM_TESTS', help='Number of tests to generate')
    parser.add_argument('-r', type=str, default='1', metavar='ROUNDING', help='Rounding types. Possible values: 0, 1, 2, 3 or any combination')
    parser.add_argument('-o', type=str, default='+-*/', metavar='OPERATIONS', help='Operations. Possible values: +, -, *, / or any combination')
    return parser.parse_args()


def main():
    args = parse_args()
    print('Generating tests...')
    subprocess.run('clang++ gen.cpp -o gen.out', shell=True)

    with open(args.f, 'w') as f:
        f.write(subprocess.check_output(['./gen.out'] + [args.r, args.o, str(args.n)]).decode())
    
    print('Done')


if __name__ == '__main__':
    main()
