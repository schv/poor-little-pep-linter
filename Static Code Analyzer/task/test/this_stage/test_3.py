class Test:
    def __init__(self, alpha, beta=1):
        self.alpha = alpha
        self.beta = beta

    def function(self):
        print(self.alpha)

    def mutable_var(self, s=[]):
        print(s)

    def okey(self, s=None):
        print("okey")
