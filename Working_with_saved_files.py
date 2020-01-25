from Robot import Robot
from Turtle import Turtle
from Calculator import Calculator
from Blueprinter import Blueprinter
import tkinter
import copy

# -------------------------------------------------------------------------------------------------------
op_dict = {'Робот': Robot(), 'Черепаха': Turtle(), 'Вычислитель': Calculator(), 'Чертежник': Blueprinter()}
main = tkinter.Tk()
canvas = tkinter.Canvas(height=800, width=800, bg='#006400')


# ---------------------------------------------------------------------------------------------------
class MySyntaxError(SyntaxError):
    pass


def no_space_string(s):
    s1 = ''
    for i in range(len(s)):
        if s[i] != ' ':
            s1 += s[i]
    return s1


def formatted_command(s):
    i = 0
    res = ''
    if '(' in s:
        while s[i] != '(':
            res += s[i]
            i += 1
        return no_space_string(res)
    else:
        return no_space_string(s)


def function_argument(s):
    i = 0
    while s[i] != '(':
        i += 1
    i += 1
    i1 = i
    while s[i] != ')':
        i += 1
    i -= 1
    i2 = i
    res = s[i1:i2 + 1]
    return no_space_string(res)


def complicated_argument(s):
    s1 = function_argument(s)
    res = []
    i = 0
    while s1[i] != ',':
        i += 1
    res.append(eval(s1[:i]))
    i += 1
    res.append(eval(s1[i:]))
    return res


def cycle_body(l):
    f = False
    p1, p2 = 0, 0
    for i in range(len(l)):
        if 'пока' in l[i] or 'нц' in l[i]:
            p1 = i + 1
            f = True
            break
    for i in range(len(l) - 1, -1, -1):
        if 'кц' in l[i]:
            p2 = i
            break

    if f:
        res = l[p1:p2]
        res.insert(0, p2 + 1)
    else:
        return [False]
    return res


# -------------------------------------------------------------------------------------------------------
def xs(x):
    return x + 400


def ys(y):
    return -y + 400


def coords():
    global canvas
    for i in range(1, 40):
        canvas.create_line(i * 20, 0, i * 20, 800, fill='black')
    for j in range(0, 820, 20):
        canvas.create_line(0, j, 800, j)
    canvas.create_line(400, 0, 400, 800, fill='purple')
    canvas.create_line(0, 400, 800, 400, fill='purple')


# -------------------------------------------------------------------------------------------------------
def compiling_txt(file_name):
    file = open(file_name, 'rt', encoding='utf-8')
    l = file.readlines()
    for i in range(len(l)):
        if l[i][-1] == '\n':
            l[i] = l[i][:len(l[i]) - 1]
    operator = l[0]
    f = False
    for i in range(1, len(l)):
        t = formatted_command(l[i])
        if (t in op_dict[operator].command_list) or ('нц' in t) or ('пока' in t) or ('кц' in t):
            f = True
        else:
            f = False
            raise MySyntaxError('Синтаксическая ошибка в строке {}'.format(i + 1))
    if f:
        op = l[0]
        if op == 'Чертежник':
            op = Blueprinter()
        elif op == 'Черепаха':
            op = Turtle()
        elif op == 'Робот':
            op = Robot()
        elif op == 'Вычислитель':
            op = Calculator()
        core_alg(l[1:], op)
        if isinstance(op, Turtle) or isinstance(op, Blueprinter) or op == (op, Robot):
            canvas.pack()
            main.mainloop()


def core_alg(l, op):
    global canvas, main

    if isinstance(op, Blueprinter):
        coords()
        crd = op.pos
        pos = canvas.create_oval(xs(crd[0] - 2), ys(crd[1] - 2), xs(crd[0] + 2), ys(crd[1] + 2), fill='red')
        i = 0
        while i < len(l):
            print(l[i])
            t = formatted_command(l[i])
            if t == 'сместись_в_точку':
                args = complicated_argument(l[i])
                point1 = copy.deepcopy(op.pos)
                op.moveto(args[0], args[1])
                point2 = copy.deepcopy(op.pos)
                if op.f:
                    canvas.create_line(xs(point1[0]), ys(point1[1]), xs(point2[0]), ys(point2[1]), fill='blue')
                canvas.delete(pos)
                crd = op.pos
                pos = canvas.create_oval(xs(crd[0] - 2), ys(crd[1] - 2), xs(crd[0] + 2), ys(crd[1] + 2), fill='red')

            elif t == 'сместись_на_вектор':
                args = complicated_argument(l[i])
                point1 = copy.deepcopy(op.pos)
                op.vector_move(args[0], args[1])
                point2 = copy.deepcopy(op.pos)
                if op.f:
                    canvas.create_line(xs(point1[0]), ys(point1[1]), xs(point2[0]), ys(point2[1]), fill='blue')
                canvas.delete(pos)
                crd = op.pos
                pos = canvas.create_oval(xs(crd[0] - 2), ys(crd[1] - 2), xs(crd[0] + 2), ys(crd[1] + 2), fill='red')
            elif t == 'подними_перо':
                op.up()
            elif t == 'опусти_перо':
                op.down()
            elif 'нц' in t:
                cycle = cycle_body(l)
                for j in range(int(t[2])):
                    core_alg(cycle[1:], op)
                i = int(cycle[0]) - 1
            i += 1

    elif isinstance(op, Turtle):
        i = 0
        crd = op.pos
        pos = canvas.create_oval(xs(crd[0] - 2), ys(crd[1] - 2), xs(crd[0] + 2), ys(crd[1] + 2), fill='black')
        while i < len(l):
            t = formatted_command(l[i])
            print(l[i])
            if t == 'вперед':
                point1 = copy.deepcopy(op.pos)
                op.forward(function_argument(l[i]))
                point2 = copy.deepcopy(op.pos)
                if op.f:
                    canvas.create_line(xs(point1[0]), ys(point1[1]), xs(point2[0]), ys(point2[1]))
                canvas.delete(pos)
                pos = canvas.create_oval(xs(crd[0] - 2), ys(crd[1] - 2), xs(crd[0] + 2), ys(crd[1] + 2), fill='black')
            elif t == 'назад':
                point1 = copy.deepcopy(op.pos())
                op.backwards(function_argument(l[i]))
                point2 = copy.deepcopy(op.pos())
                if op.f:
                    canvas.create_line(xs(point1[0]), ys(point1[1]), xs(point2[0]), ys(point2[1]))
                canvas.delete(pos)
                pos = canvas.create_oval(xs(crd[0] - 2), ys(crd[1] - 2), xs(crd[0] + 2), ys(crd[1] + 2), fill='black')
            elif t == 'вправо':
                op.right(function_argument(l[i]))
            elif t == 'влево':
                op.left(function_argument(l[i]))
            elif t == 'подними_хвост':
                op.up()
            elif t == 'опусти_хвост':
                op.down()
            elif 'нц' in t:
                cycle = cycle_body(l)
                for j in range(int(t[2])):
                    core_alg(cycle[1:], op)
                i = int(cycle[0]) - 2
            i += 1
    elif isinstance(op, Calculator):
        pass
    elif isinstance(op, Robot):
        pass


compiling_txt('sample_file.txt')
