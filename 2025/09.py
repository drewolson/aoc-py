import itertools
import sys


def intersect(x, y):
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

    (a, b) = x
    (c, d) = y

    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)


def area(a, b):
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)


def lines(pair):
    maxx = max(pair[0][0], pair[1][0]) - 0.5
    minx = min(pair[0][0], pair[1][0]) + 0.5
    maxy = max(pair[0][1], pair[1][1]) - 0.5
    miny = min(pair[0][1], pair[1][1]) + 0.5

    return [
        ((minx, miny), (maxx, miny)),
        ((maxx, miny), (maxx, maxy)),
        ((maxx, maxy), (minx, maxy)),
        ((minx, maxy), (minx, miny)),
    ]


def intersection(polygon, box):
    for p in polygon:
        for b in box:
            if intersect(p, b):
                return True

    return False


points = [tuple(int(x) for x in line.split(",")) for line in sys.stdin]

pairs = sorted(
    itertools.combinations(points, 2), key=lambda pair: -area(pair[0], pair[1])
)

print(area(*pairs[0]))

polygon = list(itertools.pairwise(points)) + [(points[-1], points[0])]

result = next(pair for pair in pairs if not intersection(polygon, lines(pair)))

print(area(*result))
