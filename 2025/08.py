from unionfind import UnionFind
import itertools
import math
import sys

N = 1000
points = []

for line in sys.stdin:
    points.append(tuple(int(t) for t in line.split(",")))

pairs = sorted(
    itertools.combinations(points, 2),
    key=lambda p: math.sqrt(
        (p[0][0] - p[1][0]) ** 2 + (p[0][1] - p[1][1]) ** 2 + (p[0][2] - p[1][2]) ** 2
    ),
)

uf = UnionFind(points)

for i, p in enumerate(pairs):
    uf.union(p[0], p[1])

    if i + 1 == N:
        print(math.prod(sorted([len(c) for c in uf.components()], reverse=True)[:3]))

    if len(uf.components()) == 1:
        print(p[0][0] * p[1][0])
        break
