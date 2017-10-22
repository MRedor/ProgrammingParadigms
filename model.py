#!/usr/bin/env python3

# Шаблонъ для домашнѣго задания
# Рѣализуйте мѣтоды с raise NotImplementedError

from folder import *


class Scope:

    """Scope - представляет доступ к значениям по именам
    (к функциям и именованным константам).
    Scope может иметь родителя, и если поиск по имени
    в текущем Scope не успешен, то если у Scope есть родитель,
    то поиск делегируется родителю.
    Scope должен поддерживать dict-like интерфейс доступа
    (см. на специальные функции __getitem__ и __setitem__)
    """

    def __init__(self, parent=None):
        self.parent = parent
        self.dict = dict()

    def __getitem__(self, key):
        if (key in self.dict):
            return self.dict[key]
        if (self.parent):
            return self.parent[key]
        else:
            raise KeyError

    def __setitem__(self, key, value):
        self.dict[key] = value


class Number:

    """Number - представляет число в программе.
    Все числа в нашем языке целые."""

    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self

    def __eq__(self, other):
        return (self.value == other.value)

    def __hash__(self):
        return (self.value * 7) % (10**6 + 3)

    def accept(self, visitor):
        return visitor.visitNumber(self)


class Function:

    """Function - представляет функцию в программе.
    Функция - второй тип поддерживаемый языком.
    Функции можно передавать в другие функции,
    и возвращать из функций.
    Функция состоит из тела и списка имен аргументов.
    Тело функции это список выражений,
    т. е.  у каждого из них есть метод evaluate.
    Список имен аргументов - список имен
    формальных параметров функции.
    Аналогично Number, метод evaluate должен возвращать self.
    """

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        return self


class FunctionDefinition:

    """FunctionDefinition - представляет определение функции,
    т. е. связывает некоторое имя с объектом Function.
    Результатом вычисления FunctionDefinition является
    обновление текущего Scope - в него
    добавляется новое значение типа Function."""

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function

    def accept(self, visitor):
        return visitor.visitFunctionDefinition(self)


class Conditional:

    """
    Conditional - представляет ветвление в программе, т. е. if.
    """

    def __init__(self, condtion, if_true, if_false=None):
        self.condtion = condtion
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        if (self.condtion.evaluate(scope).value == 0):
            ans = None
            if (self.if_false):
                for cur in self.if_false:
                    ans = cur.evaluate(scope)
            return ans
        else:
            ans = None
            if (self.if_true):
                for cur in self.if_true:
                    ans = cur.evaluate(scope)
            return ans

    def accept(self, visitor):
        return visitor.visitConditional(self)


class Print:

    """Print - печатает значение выражения на отдельной строке."""

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        print(self.expr.evaluate(scope).value)
        return self.expr.evaluate(scope)

    def accept(self, visitor):
        return visitor.visitPrint(self)


class Read:

    """Read - читает число из стандартного потока ввода
     и обновляет текущий Scope.
     Каждое входное число располагается на отдельной строке
     (никаких пустых строк и лишних символов не будет).
     """

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        a = Number(int(input()))
        scope[self.name] = a
        return a

    def accept(self, visitor):
        return visitor.visitRead(self)


class FunctionCall:

    """
    FunctionCall - представляет вызов функции в программе.
    В результате вызова функции должен создаваться новый объект Scope,
    являющий дочерним для текущего Scope
    (т. е. текущий Scope должен стать для него родителем).
    Новый Scope станет текущим Scope-ом при вычислении тела функции.
    """

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        call_scope = Scope(scope)
        function = self.fun_expr.evaluate(scope)
        for i in range(len(self.args)):
            x = function.args[i]
            call_scope[function.args[i]] = self.args[i].evaluate(scope)
        ans = None
        for expr in function.body:
            ans = expr.evaluate(call_scope)
        return ans

    def accept(self, visitor):
        return visitor.visitFunctionCall(self)


class Reference:

    """Reference - получение объекта
    (функции или переменной) по его имени."""

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]

    def accept(self, visitor):
        return visitor.visitReference(self)


class BinaryOperation:

    """BinaryOperation - представляет бинарную операцию над двумя выражениями.
    Результатом вычисления бинарной операции является объект Number.
    Поддерживаемые операции:
    “+”, “-”, “*”, “/”, “%”, “==”, “!=”,
    “<”, “>”, “<=”, “>=”, “&&”, “||”."""

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

    def evaluate(self, scope):
        left = self.lhs.evaluate(scope).value
        right = self.rhs.evaluate(scope).value
        if (self.op == '+'):
            return Number(left + right)
        if (self.op == '-'):
            return Number(left - right)
        if (self.op == '*'):
            return Number(left * right)
        if (self.op == '/'):
            return Number(left / right)
        if (self.op == '%'):
            return Number(left % right)
        if (self.op == '=='):
            return Number(left == right)
        if (self.op == '!='):
            return Number(left != right)
        if (self.op == '<'):
            return Number(left < right)
        if (self.op == '>'):
            return Number(left > right)
        if (self.op == '<='):
            return Number(left <= right)
        if (self.op == '>='):
            return Number(left >= right)
        if (self.op == '&&'):
            return Number(left and right)
        if (self.op == '||'):
            return Number(left or right)

    def accept(self, visitor):
        return visitor.visitBinaryOperation(self)


class UnaryOperation:

    """UnaryOperation - представляет унарную операцию над выражением.
    Результатом вычисления унарной операции является объект Number.
    Поддерживаемые операции: “-”, “!”."""

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        x = self.expr.evaluate(scope).value
        if (self.op == '!'):
            return Number(not x)
        else:
            return Number(-x)

    def accept(self, visitor):
        return visitor.visitUnaryOperation(self)
