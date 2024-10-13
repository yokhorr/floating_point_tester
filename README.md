# TLDR
Generate 100 tests of all operations to `tests/my_file.txt`:

`python gen_test_file.py -f tests/my_file.txt -n 100 -o "+-*/"`

Test `main.cpp` on `tests/my_file.txt`

`python checker.py main.cpp -t tests/my_file.txt`

Test `main.cpp` on stress tests:

`python checker.py main.cpp --stress`

# Documentation
You need `clang++` installed to compile `gen.cpp`, otherwise change it to other C++ compiler in [gen_test_file.py](gen_test_file.py) line 38.

Check your programm on specified test file:

`python checker.py <solution-t <tests.txt>`

Run endless stress testing:

`python checker.py <solution--stress`

Specify rounding types and operations:

`python checker.py <solution--stress --rounding <rounding--operation <operation>`

`python checker.py <solution--stress -r <rounding-o <operation>`

Default rounding type is `1` and default operations are `+-*/`.
**Rounding with other types for some reason don't correctly work with C++ built-in floats.**
I'll handle it later.

If errors occur during testing on file, they are printed immediately and testing process ends.

if errors occur during stress testing, they are saved in `stress_log.txt` file.

Solutions are automatically compiled (if needed) and executed. Supported extensions: `.cpp`, `.py`, `.java`, `.out`

