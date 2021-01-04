int scanf(const char *format, ...);
int printf(const char *format,...);
int strlen(const char * s);
int memset(char *str, int c, int n);
int atoi(const char * str);


int OpID(char op) {
    if (op == '+')
        return 0;
    else if (op == '-')
        return 1;
    else if (op == '*')
        return 2;
    else if (op == '/')
        return 3;
    else if (op == '(')
        return 4;
    else if (op == ')')
        return 5;
    else if (op == '=')
        return 6;
    return 0;
}

char compareOp(char op1, char op2) {
    char * order[7] = {
        ">><<<>>",
        ">><<<>>",
        ">>>><>>",
        ">>>><>>",
        "<<<<<= ",
        ">>>> >>",
        "<<<<< ="
    };

    int x = OpID(op1);
    int y = OpID(op2);

    return order[x][y];
}

int calc(int a, int b, char op) {
     if (op == '+')
         return a + b;
     if (op == '-')
         return a - b;
     if (op == '*')
         return a * b;
     if (op == '/')
         return a / b;
     return 0;
}


struct NumStack {
    int *data;
    int top;
};

int popNum(struct NumStack * stack) {
    if (stack->top >= 0) {
        stack->top -= 1;
        return stack->data[stack->top + 1];
    }
    return 0;
}

void pushNum(struct NumStack * stack, int num) {
    stack->data[++stack->top] = num;
}


struct OpStack {
    char *data;
    int top;
};

char popOp(struct OpStack * stack) {
    if (stack->top >= 1)
        return stack->data[stack->top--];
    return '\0';
}

void pushOp(struct OpStack * stack, char op) {
    stack->top++;
    stack->data[stack->top] = op;
}

char topOp(struct OpStack * stack) {
    if (stack->top < 0)
        return '0';
    return stack->data[stack->top];
}


int main () {
    char expr[512];
    printf("expression:");
    scanf("%s", expr);
    int expr_len = strlen(expr);

    struct NumStack num_stack;
    int data_vec[512];
    num_stack.top = -1;
    num_stack.data = data_vec;
    struct OpStack op_stack;
    char op_vec[512];
    op_stack.top = -1;
    op_stack.data = op_vec;

    char num[128];
    memset(num, 0, 128);

    pushOp(&op_stack, '=');
    expr[expr_len] = '=';
    expr[expr_len+1] = '\0';


    for (int i = 0, k = 0; i <= expr_len;) {
        if (expr[i] >= '0' && expr[i] <= '9') {
            num[k++] = expr[i++];
            continue;
        }

        if (k != 0) {
            pushNum(&num_stack, atoi(num));
            memset(num, 0, 128);
            k = 0;
        }

        char result = compareOp(topOp(&op_stack), expr[i]);

        if (result == '<') {
            pushOp(&op_stack, expr[i++]);
        } else if (result == '=') {
            popOp(&op_stack);
            i++;
        } else if (result == '>') {
            int a = popNum(&num_stack);
            int b = popNum(&num_stack);
            char op = popOp(&op_stack);
            pushNum(&num_stack, calc(b, a, op));
        }
    }
    printf("result=%d\n", popNum(&num_stack));
    return 0;
}
