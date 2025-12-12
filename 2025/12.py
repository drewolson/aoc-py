import sys
import parsec as p


@p.generate
def p_num():
    digits = yield p.regex(r"[0-9]+")

    return int("".join(digits))


p_shape_line = p.many1(p.string("#") | p.string("."))


@p.generate
def p_shape():
    i = yield p_num << p.string(":\n")
    shape = yield p.sepEndBy1(p_shape_line, p.string("\n"))

    return i, shape


@p.generate
def p_region():
    x = yield p_num << p.string("x")
    y = yield p_num << p.string(": ")
    counts = yield p.sepBy1(p_num, p.string(" "))

    return (x, y), counts


@p.generate
def p_input():
    shapes = yield p.sepEndBy1(p_shape, p.string("\n"))
    regions = yield p.sepBy1(p_region, p.string("\n"))

    return dict(shapes), regions


def size(shape):
    sum = 0

    for r in shape:
        for c in r:
            if c == "#":
                sum += 1

    return sum


shapes, regions = p_input.parse(sys.stdin.read())

count = 0

for (x, y), counts in regions:
    s = sum(size(shapes[i]) * c for i, c in enumerate(counts))

    if s <= x * y:
        count += 1

print(count)
