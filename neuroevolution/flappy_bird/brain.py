import numpy as np


class Brain:
    """A network like ml5 in neuroEvolution mode: never trained,
    only randomly initialized, copied and mutated."""

    def __init__(self, inputs=5, hidden=16, outputs=2, weights=None):
        self.shape = (inputs, hidden, outputs)
        if weights is None:
            self.w1 = np.random.randn(inputs, hidden) * np.sqrt(2 / inputs)
            self.b1 = np.zeros(hidden)
            self.w2 = np.random.randn(hidden, outputs) * np.sqrt(2 / hidden)
            self.b2 = np.zeros(outputs)
        else:
            self.w1, self.b1, self.w2, self.b2 = (w.copy() for w in weights)

    @property
    def weights(self):
        return self.w1, self.b1, self.w2, self.b2

    def predict(self, inputs):
        x = np.asarray(inputs, dtype=np.float64)
        hidden = np.maximum(0.0, x @ self.w1 + self.b1)  # ReLU
        return hidden @ self.w2 + self.b2

    def decide(self, inputs):
        """True = flap. No softmax needed - argmax is the same before and after."""
        output = self.predict(inputs)
        return output[0] > output[1]

    def copy(self):
        return Brain(*self.shape, weights=self.weights)

    def mutate(self, rate=0.1, strength=0.1):
        """Like ml5.mutate(rate): each weight is shifted by a bit of
        noise with probability 'rate'."""
        for w in self.weights:
            mask = np.random.random(w.shape) < rate
            w += mask * np.random.randn(*w.shape) * strength

    @staticmethod
    def crossover(a, b):
        """Each weight is taken randomly from parent a or b."""
        mixed = []
        for wa, wb in zip(a.weights, b.weights):
            mask = np.random.random(wa.shape) < 0.5
            mixed.append(np.where(mask, wa, wb))
        return Brain(*a.shape, weights=mixed)
