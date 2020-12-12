int printf(const char *format, ...);
int scanf(const char *format, ...);
int strlen(const char *s);

int main()
{
    char t[128];
    printf("Please enter the string:\n");
    scanf("%s", t);
    int length_t = strlen(t);
    int first = 0, last = length_t - 1;
    int is_palin = 1;
    while (first < last)
    {
        if (t[first] == t[last])
        {
            first = first + 1;
            last = last - 1;
        }
        else
        {
            is_palin = 0;
            break;
        }
    }
    if (is_palin == 1)
    {
        printf("You got palindrome!\n");
    }
    else
    {
        printf("Oops, not palindrome!\n");
    }
    return 0;
}