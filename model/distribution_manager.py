from model.distribution_model import Distribution
from utils.validators.expression_validators import validate_positive_integer
from ui.pages.distribution_page.method_config import METHOD_CONFIG

class DistributionManager:
    def __init__(self):
        self.distributions = []
        self.valid_algorithms = list(METHOD_CONFIG.keys()) # Usar las claves de METHOD_CONFIG como algoritmos válidos

    def create_distribution(self, algorithm, seed=None, **kwargs):
        self.validate_algorithm_choice(algorithm, self.valid_algorithms)
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
        """Calcula la integral definida utilizando el método Monte Carlo."""
        validate_positive_integer(n_points)
        if a >= b:
            raise ValueError("El límite inferior debe ser menor que el límite superior.")
            
        distribution = self.create_distribution(algorithm, seed, **kwargs)
        return distribution.monte_carlo_integration(expr, a, b, n_points)

    def simulate_markov_epidemic(self, params, algorithm="mersenne", seed=None, **kwargs):
        """Simula la propagación de una epidemia usando el modelo de Markov."""
        if not isinstance(params, dict):
            raise ValueError("Los parámetros deben proporcionarse como un diccionario")
            
        # Validar parámetros obligatorios y establecer valores por defecto
        default_params = {
            'initial_recovered': 0,
            'beta': 0.3,
            'gamma': 0.1,
            'days': 30,
            'dt': 0.1
        }
        
        # Verificar parámetros requeridos
        required_params = ['population', 'initial_infected']
        for param in required_params:
            if param not in params:
                raise ValueError(f"Falta el parámetro requerido: {param}")
        
        # Aplicar valores por defecto para parámetros opcionales
        for param, default_value in default_params.items():
            if param not in params:
                params[param] = default_value
        
        # Validar valores numéricos y convertir tipos
        try:
            # Parámetros enteros
            for param in ['population', 'initial_infected', 'initial_recovered', 'days']:
                if param in params:
                    params[param] = int(params[param])
                    
            # Parámetros flotantes
            for param in ['beta', 'gamma', 'dt']:
                if param in params:
                    params[param] = float(params[param])
                    
            # Validaciones adicionales de rango
            if params['population'] <= 0:
                raise ValueError("La población debe ser mayor que cero")
                
            if params['initial_infected'] + params['initial_recovered'] > params['population']:
                raise ValueError("La suma de infectados y recuperados no puede superar la población total")
                
            if not (0 <= params['beta'] <= 1 and 0 <= params['gamma'] <= 1):
                raise ValueError("Las tasas beta y gamma deben estar entre 0 y 1")
                
        except ValueError as e:
            raise ValueError(f"Error en los parámetros: {str(e)}")
            
        try:
            # Validar el algoritmo y crear la distribución
            self.validate_algorithm_choice(algorithm, self.valid_algorithms)
            distribution = self.create_distribution(algorithm, seed, **kwargs)
            
            # Ejecutar la simulación y obtener resultados con el canvas
            result = distribution.markov_epidemic_simulation(params)
            
            # Verificar que el resultado contiene todos los componentes necesarios
            required_results = ['times', 'susceptible', 'infected', 'recovered', 'parameters', 'canvas']
            for component in required_results:
                if component not in result:
                    raise ValueError(f"Falta el componente {component} en los resultados")
                    
            return result
            
        except Exception as e:
            raise ValueError(f"Error en la simulación: {str(e)}")
    
    def transform_numbers(self, numbers, distribution_type, **params):
        """Transforma una lista de números a la distribución especificada."""
        try:
            # Convertir string de números a lista
            if isinstance(numbers, str):
                numbers = [float(x.strip()) for x in numbers.split(',')]
                
            # Validar que los números estén en [0,1]
            if not all(0 <= x <= 1 for x in numbers):
                raise ValueError("Todos los números deben estar en el intervalo [0,1]")

            distribution = self.create_distribution("mersenne")
            distribution.numbers = numbers
            transformed = distribution.transform_distribution(distribution_type, params)
            
            return {
                "original": numbers,
                "transformed": transformed,
                "distribution": distribution_type,
                "parameters": params
            }
            
        except Exception as e:
            raise ValueError(f"Error en la transformación: {str(e)}")

    def validate_algorithm_choice(self, choice, valid_choices):
        """Valida que la elección del algoritmo sea válida."""
        if choice not in valid_choices:
            raise ValueError(f"Elección de algoritmo no válida. Debe ser uno de: {', '.join(valid_choices)}.")