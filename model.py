#!/usr/bin/env python3

# Шаблонъ для домашнѣго задания
# Рѣализуйте мѣтоды с raise NotImplementedError


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


class Print:

    """Print - печатает значение выражения на отдельной строке."""

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        print(self.expr.evaluate(scope).value)
        return self.expr.evaluate(scope)


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


class Reference:

    """Reference - получение объекта
    (функции или переменной) по его имени."""

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


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
            if (left == right):
                return Number(1)
            else:
                return Number(0)
        if (self.op == '!='):
            if (left == right):
                return Number(0)
            else:
                return Number(1)
        if (self.op == '<'):
            if (left < right):
                return Number(1)
            else:
                return Number(0)
        if (self.op == '>'):
            if (left > right):
                return Number(1)
            else:
                return Number(0)
        if (self.op == '<='):
            if (left <= right):
                return Number(1)
            else:
                return Number(0)
        if (self.op == '>='):
            if (left >= right):
                return Number(1)
            else:
                return Number(0)
        if (self.op == '&&'):
            if (left and right):
                return Number(1)
            else:
                return Number(0)
        if (self.op == '||'):
            if (left or right):
                return Number(1)
            else:
                return Number(0)


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
            if (x == 0):
                return Number(1)
            else:
                return Number(0)
        else:
            return Number(-x)


def example():
    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end=' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)


def test_scope_print_num():
    parent = Scope()
    parent['bar'] = Number(10)
    scope = Scope(parent)
    ans = scope['bar']

    Print(ans).evaluate(scope)
    scope['bar'] = Number(20)
    ans = scope['bar']
    Print(ans).evaluate(scope)


def test_reference():
    scope = Scope()
    scope['x'] = Number(0)
    assert Reference('x').evaluate(scope) == Number(0)


def test_condition():
    scope = Scope()
    scope["x"] = Number(0)
    scope["y"] = Number(1)
    res = Conditional(BinaryOperation(Number(0), '||', Number(1)),
                      [BinaryOperation(Number(1), '+', Number(2))],
                      [Number(0)]).evaluate(scope)
    assert res == Number(3)


def test_bin_ops():
    scope = Scope()
    # “%”, “==”, “!=”, “<”, “>”, “<=”, “>=”, “&&”, “||”.
    assert BinaryOperation(Number(1), '+', Number(2)
                           ).evaluate(scope) == Number(3)
    assert BinaryOperation(Number(1), '-', Number(2)
                           ).evaluate(scope) == Number(-1)
    assert BinaryOperation(Number(1), '*', Number(2)
                           ).evaluate(scope) == Number(2)
    assert BinaryOperation(Number(8), '/', Number(4)
                           ).evaluate(scope) == Number(2)
    assert BinaryOperation(Number(4), '%', Number(3)
                           ).evaluate(scope) == Number(1)
    assert BinaryOperation(Number(1), '==', Number(1)
                           ).evaluate(scope) == Number(1)
    assert BinaryOperation(Number(1), '==', Number(2)
                           ).evaluate(scope) == Number(0)
    assert BinaryOperation(Number(4), '!=', Number(3)
                           ).evaluate(scope) == Number(1)
    assert BinaryOperation(Number(4), '<', Number(3)
                           ).evaluate(scope) == Number(0)
    assert BinaryOperation(Number(4), '>', Number(3)
                           ).evaluate(scope) == Number(1)
    assert BinaryOperation(Number(4), '<=', Number(3)
                           ).evaluate(scope) == Number(0)
    assert BinaryOperation(Number(4), '<=', Number(4)
                           ).evaluate(scope) == Number(1)
    assert BinaryOperation(Number(4), '>=', Number(5)
                           ).evaluate(scope) == Number(0)
    assert BinaryOperation(Number(4), '>=', Number(4)
                           ).evaluate(scope) == Number(1)
    assert BinaryOperation(Number(1), '&&', Number(0)
                           ).evaluate(scope) == Number(0)
    assert BinaryOperation(Number(1), '||', Number(0)
                           ).evaluate(scope) == Number(1)


def test_un_ops():
    scope = Scope()
    assert UnaryOperation('-', Number(3)).evaluate(scope) == Number(-3)
    assert UnaryOperation('!', Number(1)).evaluate(scope) == Number(0)


def test_function():
    scope = Scope()
    function = Function(("x"), [Conditional(BinaryOperation(Number(0), '||', Number(1)), [
        BinaryOperation(Number(1), '+', Number(2))], [Number(0)]).evaluate(scope)])
    f = FunctionDefinition("my_f", function)
    assert FunctionCall(f, [Number(1)]).evaluate(scope) == Number(3)


if __name__ == '__main__':
    example()
    test_scope_print_num()
    test_bin_ops()
    test_un_ops()
    test_reference()
    test_condition()
    test_function()
