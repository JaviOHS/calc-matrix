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
            raise ValueError("No hay distribuciones generadas")
        return self.distributions[-1]

    def clear(self):
        self.distributions.clear()