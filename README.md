Поддерживается только тестирование single precision floating point. Тестирование операций `mad` и `fma` не поддерживается.

___

Сначала надо скомпилировать `gen.cpp` и `solid.cpp`.

Для Linux:

`g++ gen.cpp -o gen.out`

Для Windows:

`g++ gen.cpp -o gen.exe`

Файл `solid.cpp` можно использовать как эталонное решение, правда, только для hex представления ответа.

___

Запуск стресс-тестов:

`python checker.py --stress [-r <rounding>] [-o <operation>] <solution>`

Например:

`python checker.py --stress -r "012" -o "+-" main.out`

Если не указывать rounding и operation, по умолчанию тестируется всё.

Ещё есть флаг `--special`, при использовании которого с высокой вероятностью будут генерироваться денормализованные числа, NaN'ы и бесконечности:

`python checker.py --stress --special main.out`

Ошибки записываются в `stress_log.txt`, который очищается при очередном запуске стресс-тестов.

___

Есть также кастомные тесты на всякие частные случаи, но, к сожалению, ответы к ним есть только в hex представлении. Тем не менее, очень рекомендуется их запустить:

`python checker.py --test tests/custom.txt main.out`
