import parsec as p
import sys
from functools import lru_cache


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


def paths(graph, goal, start):
    @lru_cache
    def aux(node):
        if node == goal:
            return 1

        return sum(aux(n) for n in graph.get(node, []))

    return aux(start)


graph = dict(p_input.parse(sys.stdin.read()))

print(paths(graph, "out", "you"))

print(
    paths(graph, "fft", "svr") * paths(graph, "dac", "fft") * paths(graph, "out", "dac")
    + paths(graph, "dac", "svr")
    * paths(graph, "fft", "dac")
    * paths(graph, "out", "fft")
)
