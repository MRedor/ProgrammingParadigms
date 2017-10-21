from model import *
import sys


class PrettyPrinter:

    def __init__(self):
        self.tab = 0

    def visit(self, tree):
        tree.accept(self)
        print(';')

    def visitConditional(self, cond):
        print('if (', end='')
        cond.condtion.accept(self)
        print(') {')
        self.tab += 4
        for exp in cond.if_true:
            self.visit(exp)
        print(' ' * (self.tab - 4), '}', end='', sep='')
        print(' else {')
        for exp in cond.if_false:
            self.visit(exp)
        self.tab -= 4
        print(' ' * self.tab, '}', end='', sep='')

    def visitNumber(self, num):
        print(num.value, end='')

    def visitFunctionDefinition(self, deff):
        print('def ', deff.name, '(', end='', sep='')
        for i in range(len(deff.function.args)):
            print(deff.function.args[i], end='')
            if (i + 1 < len(deff.function.args)):
                print(', ', end='')
        print(') {')
        self.tab += 4
        for exp in deff.function.body:
            self.visit(exp)
        self.tab -= 4
        print(' ' * self.tab, '}', end='', sep='')

    def visitPrint(self, text):
        print('print ', end='')
        text.expr.accept(self)

    def visitRead(self, read):
        print('read ', read.name, end='', sep='')

    def visitReference(self, ref):
        print(ref.name, end='')

    def visitFunctionCall(self, function):
        print(function.fun_expr.name, '(', end='', sep='')
        for i in range(len(function.args)):
            function.args[i].accept(self)
            if (i + 1 < len(function.args)):
                print(', ', end='')
        print(')', end='')

    def visitUnaryOperation(self, op):
        print(op.op, '(', end='', sep='')
        op.expr.accept(self)
        print(')', end='')

    def visitBinaryOperation(self, op):
        print('(', end='')
        op.lhs.accept(self)
        print(' ', op.op, ' ', end='', sep='')
        op.rhs.accept(self)
        print(')', end='')


def testConditional():
    global tmp
    tmp = sys.stdout
    sys.stdout = open('Conditional', 'w')

    number = Number(0)
    conditional = Conditional(number, [], [])
    printer = PrettyPrinter()
    printer.visit(conditional)

    sys.stdout.close()
    fin = open('Conditional', 'r')
    check = fin.read()
    sys.stdout = tmp
    fin.close()

    assert check == 'if (0) {\n} else {\n};\n'


def testNumber():
    global tmp
    tmp = sys.stdout
    sys.stdout = open('Number', 'w')

    number = Number(12)
    printer = PrettyPrinter()
    printer.visit(number)

    sys.stdout.close()
    fin = open('Number', 'r')
    check = fin.read()
    sys.stdout = tmp
    fin.close()

    assert check == '12;\n'


def testFunctionDefinition():
    global tmp
    tmp = sys.stdout
    sys.stdout = open('FDef', 'w')

    function = Function(('i'), [])
    deff = FunctionDefinition('kek', function)
    printer = PrettyPrinter()
    printer.visit(deff)

    sys.stdout.close()
    fin = open('FDef', 'r')
    check = fin.read()
    sys.stdout = tmp
    fin.close()

    assert check == 'def kek(i) {\n};\n'


def testPrintRead():
    global tmp
    tmp = sys.stdout
    sys.stdout = open('Read', 'w')

    printer = PrettyPrinter()
    read = Read('x')
    printer.visit(read)
    num = Number(10)
    print = Print(num)
    printer.visit(print)

    sys.stdout.close()
    fin = open('Read', 'r')
    check = fin.read()
    sys.stdout = tmp
    fin.close()

    assert check == 'read x;\nprint 10;\n'


def testFunctionCall():
    global tmp
    tmp = sys.stdout
    sys.stdout = open('FCall', 'w')

    printer = PrettyPrinter()
    name = Reference("kek")
    function = FunctionCall(name, [Number(0)])
    printer.visit(function)

    sys.stdout.close()
    fin = open('FCall', 'r')
    check = fin.read()
    sys.stdout = tmp
    fin.close()

    assert check == 'kek(0);\n'


def testUnaryOperation():
    global tmp
    tmp = sys.stdout
    sys.stdout = open('UnOp', 'w')

    number = Number(42)
    unary = UnaryOperation('-', number)
    printer = PrettyPrinter()
    printer.visit(unary)

    sys.stdout.close()
    fin = open('UnOp', 'r')
    check = fin.read()
    sys.stdout = tmp
    fin.close()

    assert check == '-(42);\n'


def testBinaryOperation():
    global tmp
    tmp = sys.stdout
    sys.stdout = open('BinOp', 'w')

    n0, n1, n2 = Number(1), Number(2), Number(3)
    add = BinaryOperation(n1, '*', n2)
    mul = BinaryOperation(add, '+', add)
    printer = PrettyPrinter()
    printer.visit(mul)

    sys.stdout.close()
    fin = open('BinOp', 'r')
    check = fin.read()
    sys.stdout = tmp
    fin.close()

    assert check == '((2 * 3) + (2 * 3));\n'


if __name__ == "__main__":
    testConditional()
    testNumber()
    testFunctionDefinition()
    testPrintRead()
    testFunctionCall()
    testUnaryOperation()
    testBinaryOperation()
