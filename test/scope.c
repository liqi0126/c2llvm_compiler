int printf(const char *format, ...);

int test () {
    int a=2;
    printf("%d\n", a);
    return 0;
}

int main () {
    int a=1;
    printf("%d\n", a);
    test();
    printf("%d\n", a);
    return 0;
}