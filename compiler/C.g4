grammar C;

//---------------------------------------语法规则----------------------------------------------

//-----------------------程序框架-----------------------
program
    :   (includeStatement|declareStatement|definitionStatement|functionStatement)*
    ;


//-----------------------头文件-----------------------
includeStatement
    :   '#include' '<' library '>'
    ;

library
    :   Identifier '.h'
    ;

//-----------------------变量声明-----------------------
declareStatement
    :   preservedTypeSpecifier (Identifier ('=' Constant)?)  (',' Identifier ('=' Constant)?)* ';'
    |   typeSpecifier (Identifier|arrayIdentifier) (',' Identifier|arrayIdentifier)* ';'
    ;

//-----------------------结构体定义-----------------------
definitionStatement
    :   structDefinitionStatement
    ;

structDefinitionStatement
    :   structIdentifier '{' structParam+ '}' ';'
    ;

structIdentifier
    :   Struct Identifier
    ;

structParam
    :   typeSpecifier (arrayIdentifier|Identifier) ';'
    ;

//-----------------------函数-----------------------
functionStatement
    :   (Void|typeSpecifier) Identifier '(' funcParameters ')' compoundStatement
    ;

funcParameters
    :   (funcParameter (',' funcParameter)*)?
    ;

funcParameter
    :   typeSpecifier Identifier
    ;

compoundStatement
    :   '{' blockItemList? '}'
    ;

blockItemList
    :   statement
    |   blockItemList statement
    ;

statement
    :   declareStatement
    |   expressionStatement
    |   compoundStatement
    |   selectionStatement
    |   iterationStatement
    |   jumpStatement
    ;

//-----------------------表达式-----------------------
primaryExpression
    :   Identifier
    |   Constant
    |   StringLiteral+
    |   '(' expression ')'
    ;

postfixExpression
    :   primaryExpression
    |   postfixExpression '[' expression ']'
    |   postfixExpression '(' argumentExpressionList? ')'
    |   postfixExpression '.' Identifier
    |   postfixExpression '->' Identifier
    |   postfixExpression '++'
    |   postfixExpression '--'
    ;

argumentExpressionList
    :   assignmentExpression
    |   argumentExpressionList ',' assignmentExpression
    ;

unaryExpression
    :   postfixExpression
    |   '++' unaryExpression
    |   '--' unaryExpression
    |   unaryOperator castExpression
    ;

unaryOperator
    :   '&' | '*' | '+' | '-' | '~' | '!'
    ;

castExpression
    :   '(' typeSpecifier ')' castExpression
    |   unaryExpression
    |   DigitSequence // for
    ;

multiplicativeExpression
    :   castExpression
    |   multiplicativeExpression '*' castExpression
    |   multiplicativeExpression '/' castExpression
    |   multiplicativeExpression '%' castExpression
    ;

additiveExpression
    :   multiplicativeExpression
    |   additiveExpression '+' multiplicativeExpression
    |   additiveExpression '-' multiplicativeExpression
    ;

shiftExpression
    :   additiveExpression
    |   shiftExpression '<<' additiveExpression
    |   shiftExpression '>>' additiveExpression
    ;

relationalExpression
    :   shiftExpression
    |   relationalExpression '<' shiftExpression
    |   relationalExpression '>' shiftExpression
    |   relationalExpression '<=' shiftExpression
    |   relationalExpression '>=' shiftExpression
    ;

equalityExpression
    :   relationalExpression
    |   equalityExpression '==' relationalExpression
    |   equalityExpression '!=' relationalExpression
    ;

andExpression
    :   equalityExpression
    |   andExpression '&' equalityExpression
    ;

exclusiveOrExpression
    :   andExpression
    |   exclusiveOrExpression '^' andExpression
    ;

inclusiveOrExpression
    :   exclusiveOrExpression
    |   inclusiveOrExpression '|' exclusiveOrExpression
    ;

logicalAndExpression
    :   inclusiveOrExpression
    |   logicalAndExpression '&&' inclusiveOrExpression
    ;

logicalOrExpression
    :   logicalAndExpression
    |   logicalOrExpression '||' logicalAndExpression
    ;

conditionalExpression
    :   logicalOrExpression ('?' expression ':' conditionalExpression)?
    ;

assignmentExpression
    :   conditionalExpression
    |   unaryExpression assignmentOperator assignmentExpression
    |   DigitSequence // for
    ;

assignmentOperator
    :   '=' | '*=' | '/=' | '%=' | '+=' | '-=' | '<<=' | '>>=' | '&=' | '^=' | '|='
    ;

expression
    :   assignmentExpression
    |   expression ',' assignmentExpression
    ;

expressionStatement
    :   expression? ';'
    ;

//-----------------------条件选择-----------------------
selectionStatement
    :   ifStatement
    ;

ifStatement
    :   'if' '(' expression ')' statement ('else' statement)?
    ;

// TODO: switchStatement
//    :   'switch' '(' expression ')' statement
//    ;

//-----------------------循环-----------------------
iterationStatement
    :   whileStatement
    |   doWhileStatement
    |   forStatement
    ;

// while 循环
whileStatement
    :   While '(' expression ')' statement
    ;

// do while 循环
doWhileStatement
    :   Do statement While '(' expression ')' ';'
    ;

// for 循环
forStatement
    :   For '(' forCondition ')' statement
    ;

forCondition
	:   forDeclaration ';' forExpression? ';' forExpression?
	|   expression? ';' forExpression? ';' forExpression?
	;

forDeclaration
    :   declareStatement (',' declareStatement)*
    ;

forExpression
    :   assignmentExpression
    |   forExpression ',' assignmentExpression
    ;

//-----------------------跳转-----------------------
jumpStatement
    :   'continue' ';'
    |   'break' ';'
    |   'return' expression? ';'
    ;


//-----------------------数据类型声明-----------------------
typeSpecifier
    :   preservedTypeSpecifier
    |   structSpecifier
    ;

preservedTypeSpecifier
    :   'int'
    |   'float'
    |   'double'
    |   'char'
    ;

structSpecifier
    :   Struct Identifier
    ;

//-----------------------数组-----------------------
arrayIdentifier
    :   Identifier '[' DecimalConstant ']'
    ;

arrayItem
    :   Identifier '[' expression ']'
    ;

//---------------------------------------词法规则----------------------------------------------

//-----------------------系统预定义字段-----------------------
Auto : 'auto';
Break : 'break';
Case : 'case';
Char : 'char';
Const : 'const';
Continue : 'continue';
Default : 'default';
Do : 'do';
Double : 'double';
Else : 'else';
Enum : 'enum';
Extern : 'extern';
Float : 'float';
For : 'for';
Goto : 'goto';
If : 'if';
Inline : 'inline';
Int : 'int';
Long : 'long';
Register : 'register';
Restrict : 'restrict';
Return : 'return';
Short : 'short';
Signed : 'signed';
Sizeof : 'sizeof';
Static : 'static';
Struct : 'struct';
Switch : 'switch';
Typedef : 'typedef';
Union : 'union';
Unsigned : 'unsigned';
Void : 'void';
Volatile : 'volatile';
While : 'while';

Alignas : '_Alignas';
Alignof : '_Alignof';
Atomic : '_Atomic';
Bool : '_Bool';
Complex : '_Complex';
Generic : '_Generic';
Imaginary : '_Imaginary';
Noreturn : '_Noreturn';
StaticAssert : '_Static_assert';
ThreadLocal : '_Thread_local';

LeftParen : '(';
RightParen : ')';
LeftBracket : '[';
RightBracket : ']';
LeftBrace : '{';
RightBrace : '}';

Less : '<';
LessEqual : '<=';
Greater : '>';
GreaterEqual : '>=';
LeftShift : '<<';
RightShift : '>>';

Plus : '+';
PlusPlus : '++';
Minus : '-';
MinusMinus : '--';
Star : '*';
Div : '/';
Mod : '%';

And : '&';
Or : '|';
AndAnd : '&&';
OrOr : '||';
Caret : '^';
Not : '!';
Tilde : '~';

Question : '?';
Colon : ':';
Semi : ';';
Comma : ',';

Assign : '=';
// '*=' | '/=' | '%=' | '+=' | '-=' | '<<=' | '>>=' | '&=' | '^=' | '|='
StarAssign : '*=';
DivAssign : '/=';
ModAssign : '%=';
PlusAssign : '+=';
MinusAssign : '-=';
LeftShiftAssign : '<<=';
RightShiftAssign : '>>=';
AndAssign : '&=';
XorAssign : '^=';
OrAssign : '|=';

Equal : '==';
NotEqual : '!=';

Arrow : '->';
Dot : '.';
Ellipsis : '...';

//-----------------------符号与常量-----------------------
Identifier
    :   IdentifierNondigit
        (   IdentifierNondigit
        |   Digit
        )*
    ;

IdentifierNondigit
    :   Nondigit
    ;

Constant
    :   IntegerConstant
    |   FloatingConstant
    |   CharacterConstant
    ;

IntegerConstant
    :   DecimalConstant
    ;

FloatingConstant
    :   DecimalFloatingConstant
    ;

DecimalConstant
    :   NonzeroDigit Digit*
    ;

DecimalFloatingConstant
    :   DigitSequence? '.' DigitSequence
    |   DigitSequence '.'
    ;

CharacterConstant
    :   '\'' CCharSequence '\''
    ;

CCharSequence
    :   CChar+
    ;

CChar
    :   ~['\\\r\n]
    ;

DigitSequence
    :   Digit+
    ;

Nondigit
    :   [a-zA-Z_]
    ;

NonzeroDigit
    :   [1-9]
    ;

Digit
    :   [0-9]
    ;

StringLiteral
    :   '"' .*? '"'
    ;


//-----------------------忽略空格与换行-----------------------
Whitespace
    :   [ \t]+
        -> skip
    ;

Newline
    :   (   '\r' '\n'?
        |   '\n'
        )
        -> skip
    ;


//-----------------------忽略注释-----------------------
BlockComment
    :   '/*' .*? '*/'
        -> skip
    ;

LineComment
    :   '//' ~[\r\n]*
        -> skip
    ;