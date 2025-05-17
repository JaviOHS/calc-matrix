from model._custom_generators import *
from ui.pages.distribution_page.method_config import METHOD_CONFIG

class Distribution:
    def __init__(self, algorithm="mersenne", seed=None, **kwargs):
        self.seed = seed if seed is not None else 12345
        self.algorithm = algorithm
        self.kwargs = kwargs
        self.generator = self._create_generator()
        self.numbers = []

    def _create_generator(self):
        if self.algorithm == "mersenne":
            return MersenneTwister(self.seed)
        elif self.algorithm == "xorshift":
            return Xorshift(self.seed)
        elif self.algorithm == "congruencial":
            a = self.kwargs.get('a', 1664525)
            c = self.kwargs.get('c', 1013904223)
            m = self.kwargs.get('m', 2**32)
            return LinearCongruential(self.seed, a, c, m)
        elif self.algorithm == "congruencial_multiplicativo":
            a = self.kwargs.get('a', 1664525) 
            m = self.kwargs.get('m', 2**32)
            return LinearCongruentialMultiplicative(self.seed, a, m)
        elif self.algorithm == "lfsr":
            taps = [self.kwargs.get('taps', 3), 2]  # Por defecto usar taps=[3, 2]
            return LFSR(seed=self.seed, taps=taps)
        elif self.algorithm == "productos_medios":
            return MiddleProduct(seed=self.seed)
        elif self.algorithm == "productos_cuadraticos":
            return QuadraticProduct(seed=self.seed)
        elif self.algorithm == "ruido_fisico":
            return PhysicalNoise()
        else:
            valid_options = list(METHOD_CONFIG.keys())
            raise ValueError(f"Elección de algoritmo no válida. Debe ser uno de: {', '.join(valid_options)}")

    def generate_numbers(self, count):
        if self.algorithm == "mersenne":
            self.numbers = [self.generator.random() for _ in range(count)]
        else:
            self.numbers = [self.generator.next() for _ in range(count)]
        return self.numbers

    def set_seed(self, new_seed):
        self.seed = new_seed
        self.generator = self._create_generator()

    def get_numbers(self):
        return self.numbers
    