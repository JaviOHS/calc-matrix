from numpy import cos, sin, pi
from math import log, sqrt, exp

class DistributionTransformer:
    @staticmethod
    def _safe_uniform(u):
        """Asegura que u esté en el rango (0, 1) excluyendo extremos."""
        return max(1e-10, min(0.9999999, u))
    
    @staticmethod
    def box_muller(uniform_numbers):
        """Transforma números uniformes a distribución normal usando Box-Muller."""
        if len(uniform_numbers) < 2:
            raise ValueError("Se necesitan al menos 2 números para Box-Muller.")
            
        transformed = []
        for i in range(0, len(uniform_numbers) - 1, 2):
            u1, u2 = uniform_numbers[i:i+2]
            # Proteger contra valores extremos
            u1 = DistributionTransformer._safe_uniform(u1)
            u2 = DistributionTransformer._safe_uniform(u2)
            
            z1 = sqrt(-2 * log(u1)) * cos(2 * pi * u2)
            z2 = sqrt(-2 * log(u1)) * sin(2 * pi * u2)
            transformed.extend([z1, z2])
        return transformed

    @staticmethod
    def exponential(uniform_numbers, lambda_param=1.0):
        """Transforma números uniformes a distribución exponencial."""
        if lambda_param <= 0:
            raise ValueError("lambda debe ser positivo")
        return [-log(1 - DistributionTransformer._safe_uniform(u)) / lambda_param for u in uniform_numbers]

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
        if alpha <= 0 or beta <= 0:
            raise ValueError("alpha y beta deben ser positivos")
            
        # Para alpha < 1, usamos el método de Weibull
        if alpha < 1:
            c = 1/alpha
            transformed = []
            for u in uniform_numbers:
                u_safe = DistributionTransformer._safe_uniform(u)
                x = (-log(1-u_safe))**(1/c)
                transformed.append(x * beta)
            return transformed
            
        # Para alpha >= 1, mantener el método actual con protecciones
        def gamma_transform(u1, u2):
            u1_safe = DistributionTransformer._safe_uniform(u1)
            u2_safe = DistributionTransformer._safe_uniform(u2)
            
            y = -log(u1_safe)
            z = -log(u2_safe) / alpha
            if z <= 0:
                return None
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
