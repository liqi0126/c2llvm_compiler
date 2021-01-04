#!/bin/bash

echo "表达式求值"
echo "输入:"
cat test/eval_case
echo "输出:"
python main.py test/eval.c test.ll; /usr/local/opt/llvm/bin/lli test.ll < test/eval_case;
echo "回文"
echo "输入:"
cat test/palindrome_case
echo "输出"
python main.py test/palindrome.c test.ll; /usr/local/opt/llvm/bin/lli test.ll < test/palindrome_case;
echo "快速排序"
echo "输入"
cat test/quicksort_case
echo ""
echo "输出"
python main.py test/quicksort.c test.ll; /usr/local/opt/llvm/bin/lli test.ll < test/quicksort_case;
echo "KMP字符串匹配"
echo "输入"
cat test/kmp_case
echo "输出"
python main.py test/kmp.c test.ll; /usr/local/opt/llvm/bin/lli test.ll < test/kmp_case;
rm test.ll;