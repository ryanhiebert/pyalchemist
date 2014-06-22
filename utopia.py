"""
A sketch of usage of pyalchemist, before it's written.
"""

from pyalchemist import Alchemist, Transmutation, ritual

class A:
    foo, bar, answer = 1, 2, 42


class B:
    def __init__(self, life, fish):
        self.life, self.fish = life, fish


alchemist = Alchemist(B)


@alchemist.transmutation(A, B)
class A2BTransmutation(metaclass=Transmutation):

    @ritual(['foo', 'bar'])
    def foo_bar(a, b):
        b.fish = a.foo + a.bar
        return b

    @ritual(['answer'], ['life'])
    def answer_life(a, b):
        b.life = a.answer if a.answer == 42 else None
        return b


a = A()
b = alchemist.transmute(a, B)

assert b.life == 42
assert b.fish == 3



transmutation = Transmutation()

@transmutation.ritual(['foo', 'bar'])
def foo_bar_ritual(a, b):
    b.fish = a.foo + a.bar
    return b

@transmutation.ritual(['answer'], ['life'])
def answer_life(a, b):
    b.life = a.answer if a.answer == 42 else None


a = A()
b = transmutation.transmute(a, B)

assert b.life == 42
assert b.fish == 3
