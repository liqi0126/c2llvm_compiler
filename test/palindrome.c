#include <stdio.h>
#include <string.h>

int printf(const char *format, ...);
int scanf(const char *format, ...);
int strlen(const char *s);

int main()
{
    char str[512];
    printf("string to check:");
    scanf("%s", str);
    int len = strlen(str);
    int l = 0, r = len - 1;
    int is_palindrome = 1;
    while (l < r) {
        if (str[l] == str[r]) {
            l++;
            r--;
        }
        else
        {
            is_palindrome = 0;
            break;
        }
    }
    if (is_palindrome == 1) {
        printf("Yes\n");
    }
    else {
        printf("No\n");
    }
    return 0;
}