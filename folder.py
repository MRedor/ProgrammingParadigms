from model import *


class ConstantFolder:

    def visit(self, tree):
        return tree.accept(self)

    def visitNumber(self, num):
        return num

    def visitPrint(self, text):
        return Print(text.expr.accept(self))

    def visitRead(self, read):
        return read

    def visitReference(self, ref):
        return ref

    def visitConditional(self, cond):
        cond.condtion = cond.condtion.accept(self)
        for i in range(len(cond.if_true)):
            cond.if_true[i] = self.visit(cond.if_true[i])
        if (cond.if_false):
            for i in range(len(cond.if_false)):
                cond.if_false[i] = self.visit(cond.if_false[i])

    def visitFunctionDefinition(self, deff):
        for i in range(len(deff.function.body)):
            deff.function.body[i] = self.visit(deff.function.body[i])

    def visitFunctionCall(self, function):
        for i in range(len(function.args)):
            function.args[i] = function.args[i].accept(self)
        return function

    def visitUnaryOperation(self, op):
        op.expr = op.expr.accept(self)
        if (type(op.expr) is Number):
            return op.evaluate(Scope())
        return op

    def visitBinaryOperation(self, op):
        lhs = op.lhs.accept(self)
        rhs = op.rhs.accept(self)
        isL = isinstance(lhs, Number)
        isR = isinstance(rhs, Number)
        isL2 = isinstance(lhs, Reference)
        isR2 = isinstance(rhs, Reference)
        if (isL2):
            nameL = op.lhs.name
        if (isR2):
            nameR = op.rhs.name
        if (isL and isR):
            return BinaryOperation(lhs, op.op, rhs).evaluate(Scope())
        if ((isL2 and isR2) and (nameL == nameR) and (op.op == '-')):
            return Number(0)
        if (op.op == '*'):
            if (isL):
                valL = lhs.value
            if (isR):
                valR = rhs.value
            if ((isL and valL == 0 and isR2) or (isR and valR == 0 and isL2)):
                return Number(0)
        return op


def testUnaryOperation():
    folder = ConstantFolder()
    assert Number(-1) == folder.visit(UnaryOperation('-', Number(1)))
    assert Number(1) == folder.visit(UnaryOperation('!', Number(0)))


def testBinaryOperation():
    folder = ConstantFolder()
    assert Number(0) == folder.visit(
        BinaryOperation(Number(1), '*', Number(0)))
    assert Number(0) == folder.visit(
        BinaryOperation(Number(0), '*', Reference('x')))
    assert Number(0) == folder.visit(
        BinaryOperation(Reference('x'), '-', Reference('x')))

if __name__ == "__main__":
    testUnaryOperation()
    testBinaryOperation()
