import os
import random

class MersenneTwister:
    def __init__(self, seed):
        self.index = 624
        self.mt = [0] * 624
        self.initialize_generator(seed)

    def initialize_generator(self, seed):
        self.mt[0] = seed & 0xffffffff
        for i in range(1, 624):
            self.mt[i] = (1812433253 * (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) + i) & 0xffffffff

    def extract_number(self):
        if self.index >= 624:
            self.twist()
        y = self.mt[self.index]
        self.index += 1
        y ^= (y >> 11)
        y ^= (y << 7) & 0x9d2c5680
        y ^= (y << 15) & 0xefc60000
        y ^= (y >> 18)
        return y & 0xffffffff

    def twist(self):
        for i in range(624):
            y = (self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff)
            self.mt[i] = self.mt[(i + 397) % 624] ^ (y >> 1)
            if y % 2 != 0:
                self.mt[i] ^= 0x9908b0df
        self.index = 0

    def random(self):
        return self.extract_number() / 0xffffffff
    
class LinearCongruential:
    def __init__(self, seed, a=1664525, c=1013904223, m=2**32):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m
        self.current = seed

    def next(self):
        self.current = (self.a * self.current + self.c) % self.m
        return self.current / self.m

    def generate(self, n):
        return [self.next() for _ in range(n)]
    
class LinearCongruentialMultiplicative:
    def __init__(self, seed, a=1664525, m=2**32):
        self.seed = seed
        self.a = a
        self.m = m
        self.current = seed

    def next(self):
        self.current = (self.a * self.current) % self.m
        return self.current / self.m

    def generate(self, n):
        return [self.next() for _ in range(n)]

class LFSR:
    def __init__(self, seed, taps):
        self.state = seed
        self.taps = taps if isinstance(taps, list) else [taps, 2]

    def next(self):
        xor = 0
        for t in self.taps:
            xor ^= (self.state >> t) & 1
        self.state = ((self.state << 1) | xor) & ((1 << self.state.bit_length()) - 1)
        return self.state / (1 << self.state.bit_length())

    def generate(self, n):
        return [self.next() for _ in range(n)]
    
class MiddleProduct:
    def __init__(self, seed):
        self.current = seed
        self.previous = seed + 1 if seed < 9999 else seed - 1

    def next(self):
        # Multiplicamos los dos números actuales
        product = self.current * self.previous
        product_str = str(product).zfill(8)  # Asegura al menos 8 dígitos
        middle = len(product_str) // 2
        
        # Extraer los dígitos medios (4 dígitos)
        middle_digits = int(product_str[middle - 2:middle + 2]) 
        
        # Actualizar valores
        self.previous = self.current
        self.current = middle_digits
        
        return self.current / 10000

    def generate(self, n):
        return [self.next() for _ in range(n)]
    
class QuadraticProduct:
    def __init__(self, seed):
        self.current = seed

    def next(self):
        # Calculamos el cuadrado del número actual
        square = self.current ** 2
        square_str = str(square).zfill(8)  # Asegura al menos 8 dígitos
        middle = len(square_str) // 2

        # Extraer los dígitos medios (4 dígitos)
        self.current = int(square_str[middle - 2:middle + 2])
        
        return self.current / 10000

    def generate(self, n):
        return [self.next() for _ in range(n)]
    
class Xorshift:
    def __init__(self, seed=None):
        self.state = seed if seed is not None else random.randint(1, 2**32 - 1)

    def _xorshift32(self, state):
        state ^= (state << 13) & 0xFFFFFFFF
        state ^= (state >> 17) & 0xFFFFFFFF
        state ^= (state << 5) & 0xFFFFFFFF
        return state & 0xFFFFFFFF

    def next(self):
        self.state = self._xorshift32(self.state)
        return self.state / float(2**32)

    def set_seed(self, seed):
        self.state = seed
        
class PhysicalNoise:
    def next(self):
        # Genera un número aleatorio usando bytes del sistema operativo
        return int.from_bytes(os.urandom(4), 'big') / (2**32)

    def generate(self, n):
        return [self.next() for _ in range(n)]
