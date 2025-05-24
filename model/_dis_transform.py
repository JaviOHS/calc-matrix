from numpy import cos, sin, pi
from math import log, sqrt, exp, factorial

class DistributionTransformer:
    @staticmethod
    def box_muller(uniform_numbers):
        """Transforma números uniformes a distribución normal usando Box-Muller."""
        if len(uniform_numbers) < 2:
            raise ValueError("Se necesitan al menos 2 números para Box-Muller.")
            
        transformed = []
        for i in range(0, len(uniform_numbers) - 1, 2):
            u1, u2 = uniform_numbers[i:i+2]
            z1 = sqrt(-2 * log(u1)) * cos(2 * pi * u2)
            z2 = sqrt(-2 * log(u1)) * sin(2 * pi * u2)
            transformed.extend([z1, z2])
        return transformed

    @staticmethod
    def exponential(uniform_numbers, lambda_param=1.0):
        """Transforma números uniformes a distribución exponencial."""
        return [-log(1 - u) / lambda_param for u in uniform_numbers]

    @staticmethod
    def poisson(uniform_numbers, lambda_param=1.0):
        """Transforma números uniformes a distribución de Poisson."""
        def inverse_poisson(u, lambda_param):
            p = exp(-lambda_param)
            F = p
            k = 0
            while u > F:
                k += 1
                p = p * lambda_param / k
                F += p
            return k

        return [inverse_poisson(u, lambda_param) for u in uniform_numbers]

    @staticmethod
    def binomial(uniform_numbers, n, p):
        """Transforma números uniformes a distribución binomial."""
        def inverse_binomial(u, n, p):
            k = 0
            prob = (1 - p) ** n
            F = prob
            while u > F and k < n:
                k += 1
                prob *= (n - k + 1) * p / (k * (1 - p))
                F += prob
            return k

        return [inverse_binomial(u, n, p) for u in uniform_numbers]

    @staticmethod
    def gamma(uniform_numbers, alpha, beta=1.0):
        """Transforma números uniformes a distribución gamma."""
        if alpha < 1:
            raise ValueError("Alpha debe ser >= 1.")
            
        def gamma_transform(u1, u2):
            y = -log(u1)
            z = -log(u2) / alpha
            if y >= (alpha - 1) * (z - log(z) - 1):
                return z * beta
            return None

        transformed = []
        i = 0
        while i < len(uniform_numbers) - 1:
            result = gamma_transform(uniform_numbers[i], uniform_numbers[i+1])
            if result is not None:
                transformed.append(result)
            i += 2
        return transformed

    @staticmethod
    def beta(uniform_numbers, alpha, beta):
        """Transforma números uniformes a distribución beta."""
        if len(uniform_numbers) < 2:
            raise ValueError("Se necesitan al menos 2 números para distribución beta.")
            
        transformed = []
        for i in range(0, len(uniform_numbers) - 1, 2):
            # Usar método de aceptación-rechazo
            u1, u2 = uniform_numbers[i:i+2]
            x = u1 ** (1/alpha)
            y = u2 ** (1/beta)
            if x + y <= 1:
                transformed.append(x / (x + y))
        return transformed
