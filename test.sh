#!/bin/bash

python main.py test/eval.c; /usr/local/opt/llvm/bin/lli test.ll < test/case1;
python main.py test/IsPalindrome.c; /usr/local/opt/llvm/bin/lli test.ll < test/case2;
python main.py test/KMP.c; /usr/local/opt/llvm/bin/lli test.ll < test/case3;
