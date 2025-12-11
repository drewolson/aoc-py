import parsec as p
import sys
from functools import cache


@p.generate
def p_name():
    cs = yield p.many1(p.letter())

    return "".join(cs)


@p.generate
def p_line():
    node = yield p_name << p.string(": ")
    conns = yield p.sepBy1(p_name, p.string(" "))

    return node, conns


p_input = p.sepEndBy1(p_line, p.string("\n"))


def paths(graph, goal, start, d=False, f=False):
    @cache
    def aux(d, f, node):
        if node == "dac":
            d = True

        if node == "fft":
            f = True

        if node == goal:
            if d and f:
                return 1
            else:
                return 0

        return sum(aux(d, f, n) for n in graph.get(node, []))

    return aux(d, f, start)


graph = dict(p_input.parse(sys.stdin.read()))

print(paths(graph, "out", "you", True, True))

print(paths(graph, "out", "svr"))
