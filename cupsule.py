class A:
    def __init__(self, a, b) -> None:
        self.a = a
        self.b = b

    def calc(self):
        print(self.a + self.b)

class B(A):
    def __init__(self, a, b) -> None:
        super().__init__(a, b)

    def calc2(self):
        print(self.a * self.b)

example_object = B(100, 200)
example_object.calc()
example_object.calc2()