int printf(const char *format, ...);
int scanf(const char *format, ...);
int memset(char *str, int c, int n);
int strlen(const char *s);
int atoi(const char * str);

struct IntStack
{
    int *data;
    int top;
};

struct CharStack
{
    char *data;
    int top;
};

int tonum(char c)
{
    if (c == '+')
        return 0;
    else if (c == '-')
        return 1;
    else if (c == '*')
        return 2;
    else if (c == '/')
        return 3;
    else if (c == '(')
        return 4;
    else if (c == ')')
        return 5;
    else if (c == '=')
        return 6;
    return 0;
}

int cal(int a, int b, char c)
{
    if (c == '+')
        return a + b;
    if (c == '-')
        return a - b;
    if (c == '*')
        return a * b;
    if (c == '/')
        return a / b;
    return 0;
}

char compare(char a, char b)
{
    char *oper[7] = {">><<<>>", ">><<<>>", ">>>><>>",
                     ">>>><>>", "<<<<<= ", ">>>> >>", "<<<<< ="};
    int x = tonum(a);
    int y = tonum(b);
    return oper[x][y];
}

int emptyInt(struct IntStack *stack)
{
    if (stack->top > 0)
        return 0;
    return 1;
}

int emptyChar(struct CharStack *stack)
{
    if (stack->top > 0)
        return 0;
    return 1;
}

int topInt(struct IntStack *stack)
{
    if (stack->top > 0)
        return stack->data[stack->top - 1];
    return 0;
}

char topChar(struct CharStack *stack)
{
    if (stack->top > 0)
        return stack->data[stack->top - 1];
    return '\0';
}

int popInt(struct IntStack *stack)
{
    if (stack->top > 0)
    {
        stack->top -= 1;
        return stack->data[stack->top];
    }
    return 0;
}

char popChar(struct CharStack *stack)
{
    if (stack->top > 0)
    {
        stack->top -= 1;
        return stack->data[stack->top];
    }
    return '\0';
}

void pushInt(struct IntStack *stack, int val)
{
    stack->data[stack->top] = val;
    stack->top += 1;
}

void pushChar(struct CharStack *stack, char val)
{
    stack->data[stack->top] = val;
    stack->top += 1;
}

int main()
{
    struct IntStack num;
    num.top = 0;
    int int_data[128];
    num.data = int_data;
    struct CharStack ch;
    ch.top = 0;
    char char_data[128];
    ch.data = char_data;

    printf("Please enter expression:\n");
    char str[128];
    scanf("%s", str);
    while (emptyInt(&num) == 0)
        popInt(&num);
    while (emptyChar(&ch) == 0)
        popChar(&ch);
    pushChar(&ch, '=');
    char temp[128];
    int len = strlen(str), k = 0;
    str[len] = '=';
    str[len + 1] = '\0';
    for (int i = 0; i <= len;)
    {
        if (str[i] >= '0' && str[i] <= '9')
        {
            temp[k] = str[i];
            ++k;
            ++i;
            continue;
        }
        if (str[i] == '.')
        {
            temp[k] = str[i];
            ++k;
            ++i;
            continue;
        }

        if (k != 0)
        {
            pushInt(&num, atoi(temp));
            memset(temp, 0, 128);
            k = 0;
        }
        //	printf("%c",compare(ch.top(),str[i]));
        if (compare(topChar(&ch), str[i]) == '<')
        {
            pushChar(&ch, str[i]);
            ++i;
        }
        else if (compare(topChar(&ch), str[i]) == '=')
        {
            popChar(&ch);
            ++i;
        }
        else if (compare(topChar(&ch), str[i]) == '>')
        {
            int a = popInt(&num);
            int b = popInt(&num);
            pushInt(&num, cal(b, a, popChar(&ch)));
        }
    }
    printf("The result is %d\n", popInt(&num));
    // popInt(&num);
    return 0;
}