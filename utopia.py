"""
A sketch of usage of pyalchemist, before it's written.
"""

from pyalchemist import Alchemist

class A:
    foo, bar, answer = 1, 2, 42


class B:
    def __init__(self, life, fish):
        self.life, self.fish = life, fish


alchemist = Alchemist(B)

@alchemist.transmutation(['foo', 'bar'])
def transmute_foo_bar(a, b):
    b.fish = a.foo + a.bar

@alchemist.transmutation(['answer'], ['life'])
def transmute_answer_life(a, b):
    b.life = a.answer if a.answer == 42 else None


a = A()
b = alchemist.transmute(a)

assert b.life == 42
assert b.fish == 3




