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


def paths(graph, goal, start, d, f):
    @cache
    def aux(node, d, f):
        if node == goal:
            return 1 if d and f else 0

        return sum(
            aux(n, d or node == "dac", f or node == "fft") for n in graph.get(node, [])
        )

    return aux(start, d, f)


graph = dict(p_input.parse(sys.stdin.read()))

print(paths(graph, "out", "you", True, True))

print(paths(graph, "out", "svr", False, False))
