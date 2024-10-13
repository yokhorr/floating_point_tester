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
import tqdm
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="Floating point lab checker")

    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('solution', nargs='?', help='Program to check')
    group.add_argument('-t', '--test', help='Test file to check')
    group.add_argument('--stress', action='store_true', help='Stress testing mode')
    parser.add_argument('-r', '--rounding', default='1', help='Roundings to test')
    parser.add_argument('-o', '--operation', default='+-*/', help='Operations to test')

    return parser.parse_args()


def compile_solution(solution):
    runnable = ""
    if solution.endswith(".cpp"):
        runnable = f'./{solution[:-4]}.out'
        compile_cmd = f'clang++ {solution} -o {runnable}'
    elif solution.endswith(".py"):
        runnable = f'python3 {solution}'
        compile_cmd = None
    elif solution.endswith(".java"):
        runnable = f'java {solution[:-5]}'
        compile_cmd = f'javac {solution}'
    elif solution.endswith(".out"):
        runnable = f'./{solution}'
        compile_cmd = None
    else:
        raise ValueError(f"Unknown file extension for {solution}")
    if compile_cmd:
        subprocess.run(compile_cmd, shell=True)

    return runnable


def test(test_file, runnable):
    # Run tests
    with open(test_file, "r") as f:
        tests = [line.strip() for line in f.readlines()]

    i = 1
    for test in tqdm.tqdm(tests, desc=f'Running {test_file}'):
        parts = test.split("#")
        cmd = f'{runnable} {parts[0].strip()}'
        correct_output = parts[1].strip()

        # Run the test
        output = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        actual_output = output.stdout.decode("utf-8").strip()

        # Check if the test passed
        if actual_output != correct_output:
            if actual_output == "skip": continue
            print(f"Test number {i} failed: {test}\n   Your output: {actual_output}\nCorrect output: {correct_output}")
            break
        i += 1
    else:
        print("OK")


def log_error(test, solution_output, answer):
    print()
    print("Failed test")
    print(f'\t {test}')
    print("Your output: ")
    print(f'\t {solution_output}')
    print("Correct output: ")
    print(f'\t {answer}')
    print()


def stress(runnable, rounding, operation):
    with open("stress_log.txt", "w") as f:
        f.write("")
    i = 1
    while True:
        test_cmd = f'./gen.out {rounding} "{operation}" 1'
        test = subprocess.run(test_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8").strip()
        parts = test.split("#")

        answer = parts[1].strip()

        solution_cmd = f'./{runnable} {parts[0].strip()}'
        solution_output = subprocess.run(solution_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8").strip()
        if solution_output != answer:
            if solution_output == "skip":
                continue
            with open("stress_log.txt", "a") as f:
                f.write(test)
                f.write("\n")
            log_error(test, solution_output, answer)
        else:
            print(f'\rTests successfuly passed: {i}', end='')
        i += 1


def main():
    print('\033[91m' + '***** By Egor Solyanik M3139: https://t.me/yokhor *****' + '\033[0m\n')
    
    args = parse_arguments()

    runnable = compile_solution(args.solution)

    if args.stress:
        stress(runnable, args.rounding, args.operation)
    elif args.test:
        test(args.test, runnable)


if __name__ == "__main__":
    1 // 0
    main()
