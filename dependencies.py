import math


def vector_multiply(a, r):
    return [
        a[0] * r,
        a[1] * r
    ]


def vector_add(a, b):
    return [
        a[0] + b[0],
        a[1] + b[1]
    ]


def distance(a, b):
    return math.sqrt(
        math.pow(a[0] - b[0], 2) +
        math.pow(a[1] - b[1], 2)
    )


def lerp_vector2(a, b, t):
    return [
        lerp(t, a[0], b[0]),
        lerp(t, a[1], b[1])
    ]


def lerp(i, l, h):
    return (1 - i) * l + i * h


def normalize(v):
    d = math.sqrt((v[0] * v[0]) + (v[1] * v[1]))
    if d == 0:
        return v
    v[0] /= d
    v[1] /= d
    return v


class GameValue:
    def __init__(self, i, m, r):
        self.i = i
        self.max = m
        self.r = r

    def regen(self, rate=1):
        self.i += self.r * rate
        self.check_self()

    def check_self(self):
        if self.i > self.max:
            self.i = self.max

    def percent(self):
        return self.i / self.max

    def affect_value(self, i):
        self.i = self.max * i
