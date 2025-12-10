import heapq
import parsec as p
import sys
import z3


@p.generate
def p_int():
    digits = yield p.many1(p.digit())
    return int("".join(digits))


@p.generate
def p_off_light():
    yield p.string(".")
    return False


@p.generate
def p_on_light():
    yield p.string("#")
    return True


p_light = p_off_light | p_on_light


@p.generate
def p_diagram():
    yield p.string("[")
    lights = yield p.many1(p_light)
    yield p.string("]")

    return lights


@p.generate
def p_schematic():
    yield p.string("(")
    indexes = yield p.sepBy1(p_int, p.string(","))
    yield p.string(")")

    return indexes


@p.generate
def p_joltages():
    yield p.string("{")
    joltages = yield p.sepBy1(p_int, p.string(","))
    yield p.string("}")

    return joltages


@p.generate
def p_machine():
    diagram = yield p_diagram << p.string(" ")
    schematics = yield p.sepEndBy1(p_schematic, p.string(" "))
    joltages = yield p_joltages

    return diagram, schematics, joltages


p_input = p.sepEndBy1(p_machine, p.string("\n"))


def search(machine):
    goal, schematics, _ = machine
    start = list(False for _ in goal)
    q = []
    heapq.heappush(q, (0, start))
    visited = set()

    while q:
        c, d = heapq.heappop(q)
        t = tuple(d)

        if t in visited:
            continue

        visited.add(t)

        if d == goal:
            return c

        for s in schematics:
            new = d.copy()

            for i in s:
                new[i] = not new[i]

            heapq.heappush(q, (c + 1, new))

    return -1


def solve(machine):
    _, schematics, joltage = machine

    opt = z3.Optimize()

    s_vars = [z3.Int("s" + str(i)) for i in range(0, len(schematics))]

    t = z3.Int("t")

    for v in s_vars:
        opt.add(v >= 0)

    for j_i, j_v in enumerate(joltage):
        vs = [v for (i, v) in enumerate(s_vars) if j_i in schematics[i]]
        opt.add(sum(vs) == j_v)

    opt.add(sum(s_vars) == t)

    opt.minimize(t)

    opt.check()

    m = opt.model()

    return m.evaluate(t).as_long()


machines = p_input.parse(sys.stdin.read())  # ty: ignore[invalid-argument-type]

# part 1
print(sum(search(m) for m in machines))

# part 2
print(sum(solve(m) for m in machines))
