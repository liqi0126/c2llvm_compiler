#include <stdio.h>
#include <string.h>

int printf(const char *format, ...);
int scanf(const char *format, ...);
int strlen(const char *s);

void computeLPSArray(char* pat, int M, int* lps)
{
    int len = 0;

    lps[0] = 0; // lps[0] is always 0

    int i = 1;
    while (i < M) {
        if (pat[i] == pat[len]) {
            len++;
            lps[i] = len;
            i++;
        }
        else // (pat[i] != pat[len])
        {
            if (len != 0) {
                len = lps[len - 1];
            }
            else // if (len == 0)
            {
                lps[i] = 0;
                i++;
            }
        }
    }
}

void KMPSearch(char* pat, char* txt, int * lps)
{
    int M = strlen(pat);
    int N = strlen(txt);

    computeLPSArray(pat, M, lps);

    int i = 0;
    int j = 0;
    while (i < N) {
        if (pat[j] == txt[i]) {
            j++;
            i++;
        }

        if (j == M) {
            printf("Found pattern at index %d\n", i - j);
            j = lps[j - 1];
        }

        else if (i < N && pat[j] != txt[i]) {
            if (j != 0)
                j = lps[j - 1];
            else
                i = i + 1;
        }
    }
}

int main()
{
    char txt[512];
    char pat[512];
    int  lps[512];
    printf("text: ");
    scanf("%s", txt);
    printf("pattern: ");
    scanf("%s", pat);

    KMPSearch(pat, txt, lps);
    return 0; 
}