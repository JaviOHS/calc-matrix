from model.distribution_model import Distribution
from utils.validators.modules_validators import validate_positive_integer, validate_algorithm_choice
from ui.pages.distribution_page.method_config import METHOD_CONFIG

class DistributionManager:
    def __init__(self):
        self.distributions = []
        # Usar las claves de METHOD_CONFIG como algoritmos válidos
        self.valid_algorithms = list(METHOD_CONFIG.keys())

    def create_distribution(self, algorithm, seed=None, **kwargs):
        validate_algorithm_choice(algorithm, self.valid_algorithms)
        distribution = Distribution(algorithm, seed, **kwargs)
        self.distributions.append(distribution)
        return distribution

    def generate_random_numbers(self, count, algorithm="mersenne", seed=None, **kwargs):
        validate_positive_integer(count)
        distribution = self.create_distribution(algorithm, seed, **kwargs)
        return distribution.generate_numbers(count)

    def get_last_distribution(self):
        if not self.distributions:
            raise ValueError("No hay distribuciones generadas.")
        return self.distributions[-1]

    def clear(self):
        self.distributions.clear()

    def calculate_monte_carlo_integration(self, expr, a, b, n_points=10000, algorithm="mersenne", seed=None, **kwargs):
        """
        Calcula la integral definida utilizando el método Monte Carlo.
        
        Args:
            expr: Expresión a integrar (string o expresión simbólica)
            a: Límite inferior de integración
            b: Límite superior de integración
            n_points: Número de puntos aleatorios
            algorithm: Algoritmo de generación de números aleatorios
            seed: Semilla para el generador
            **kwargs: Argumentos adicionales para el generador
            
        Returns:
            dict: Resultado de la integración con información adicional
        """
        validate_positive_integer(n_points)
        if a >= b:
            raise ValueError("El límite inferior debe ser menor que el límite superior.")
            
        distribution = self.create_distribution(algorithm, seed, **kwargs)
        return distribution.monte_carlo_integration(expr, a, b, n_points)