#!/bin/bash

python main.py test/eval.c test.ll; /usr/local/opt/llvm/bin/lli test.ll < test/eval_case;
python main.py test/palindrome.c test.ll; /usr/local/opt/llvm/bin/lli test.ll < test/palindrome_case;
python main.py test/quicksort.c test.ll; /usr/local/opt/llvm/bin/lli test.ll < test/quicksort_case;
python main.py test/kmp.c test.ll; /usr/local/opt/llvm/bin/lli test.ll < test/kmp_case;
