from numpy import array, mean, std, sqrt
from sympy import symbols, lambdify, sympify
from model._custom_generators import *
from model.graph_manager import GraphManager
from controller.graph_controller import GraphController
from ui.pages.distribution_page.method_config import METHOD_CONFIG
from model._dis_transform import DistributionTransformer

class Distribution:
    def __init__(self, algorithm="mersenne", seed=None, **kwargs):
        self.seed = seed if seed is not None else 12345
        self.algorithm = algorithm
        self.kwargs = kwargs
        self.generator = self._create_generator()
        self.numbers = []
        self.graph_controller = GraphController(GraphManager())
        self.transformer = DistributionTransformer()

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

    def monte_carlo_integration(self, expr, a, b, n_points=10000):
        """Calcula la integral definida de una expresión matemática en el intervalo [a, b] utilizando el método de Monte Carlo."""
        try:
            x = symbols('x')
            if isinstance(expr, str):
                sym_expr = sympify(expr)
            else:
                sym_expr = expr
                
            f = lambdify(x, sym_expr, 'numpy')
            
            # Generar puntos aleatorios en el intervalo [a, b]
            if not self.numbers or len(self.numbers) < n_points:
                self.generate_numbers(n_points)
                
            # Convertir los números aleatorios al intervalo [a, b]
            x_random = array(self.numbers[:n_points]) * (b - a) + a

            try:
                f_values = f(x_random)
            except Exception as e:
                raise ValueError(f"Error al evaluar la función: {str(e)}")
            
            integral_result = (b - a) * mean(f_values)
            std_error = (b - a) * std(f_values) / sqrt(n_points)
            
            return {
                "result": float(integral_result),
                "error": float(std_error),
                "n_points": n_points,
                "a": a,
                "b": b,
                "expression": str(sym_expr)
            }
            
        except Exception as e:
            raise ValueError(f"Error en la integración Monte Carlo: {str(e)}")
    
    def markov_epidemic_simulation(self, params):
        try:
            # Configurar el generador
            self.algorithm = params.get('algorithm', 'mersenne')
            self.seed = params.get('seed', 12345)
            self.generator = self._create_generator()
    
            # Extraer parámetros
            N = int(params.get('population', 1000))
            I0 = int(params.get('initial_infected', 1))
            R0 = int(params.get('initial_recovered', 0))
            beta = float(params.get('beta', 0.3))
            gamma = float(params.get('gamma', 0.1))
            days = int(params.get('days', 30))
            dt = float(params.get('dt', 0.1))
    
            # Inicializar estados
            S0 = N - I0 - R0
            S, I, R = [S0], [I0], [R0]
            times = [0]
    
            # Generar números aleatorios base
            steps = int(days / dt)
            base_numbers = self.generate_numbers(steps * 2)  # Necesitamos 2 números por paso
            
            # Dividir los números base en dos grupos
            infection_base = base_numbers[:steps]
            recovery_base = base_numbers[steps:]
            
            # Transformar a distribución gamma para modelar tiempos entre eventos
            infection_numbers = self.transformer.gamma(infection_base, alpha=beta * dt, beta=1.0)
            recovery_numbers = self.transformer.gamma(recovery_base, alpha=gamma * dt, beta=1.0)

            # Simulación
            for step in range(min(steps, len(infection_numbers), len(recovery_numbers))):
                current_S = S[-1]
                current_I = I[-1]
                current_R = R[-1]

                # Calcular transiciones usando los números transformados directamente
                actual_infections = int(max(0, min(current_S, 
                    infection_numbers[step] * beta * current_S * current_I / N)))
                actual_recoveries = int(max(0, min(current_I,
                    recovery_numbers[step] * gamma * current_I)))

                # Actualizar estados
                next_S = max(0, current_S - actual_infections)
                next_I = max(0, current_I + actual_infections - actual_recoveries)
                next_R = max(0, current_R + actual_recoveries)
    
                # Normalizar población
                total = next_S + next_I + next_R
                if total > 0:
                    factor = N / total
                    next_S = int(next_S * factor)
                    next_I = int(next_I * factor)
                    next_R = int(next_R * factor)
    
                S.append(next_S)
                I.append(next_I)
                R.append(next_R)
                times.append(times[-1] + dt)
    
            # Generar el gráfico y retornar resultados
            canvas = self.graph_controller.create_epidemic_plot(times, S, I, R, params)
            
            return {
                "times": times,
                "susceptible": S,
                "infected": I,
                "recovered": R,
                "parameters": {
                    "population": N,
                    "initial_infected": I0,
                    "initial_recovered": R0,
                    "initial_susceptible": S0,
                    "beta": beta,
                    "gamma": gamma,
                    "days": days,
                    "dt": dt,
                    "R0": beta / gamma,
                    "algorithm": self.algorithm,
                    "seed": self.seed
                },
                "canvas": canvas
            }
    
        except Exception as e:
            raise ValueError(f"Error en la simulación de Markov: {str(e)}")
    
    def transform_distribution(self, distribution_type, params=None, uniform_numbers=None):
        """Transforma los números uniformes a la distribución especificada."""
        
        # Si se proporcionan números uniformes como parámetro, usarlos
        if uniform_numbers is not None:
            if isinstance(uniform_numbers, str):
                # Convertir string separado por comas a lista de floats
                try:
                    numbers_to_transform = [float(x.strip()) for x in uniform_numbers.split(',')]
                except ValueError:
                    raise ValueError("Los números deben ser valores numéricos separados por comas")
            elif isinstance(uniform_numbers, list):
                numbers_to_transform = uniform_numbers
            else:
                raise ValueError("uniform_numbers debe ser una lista o string separado por comas")
        else:
            # Usar los números generados internamente
            if not self.numbers:
                raise ValueError("No hay números generados para transformar")
            numbers_to_transform = self.numbers
    
        if params is None:
            params = {}
    
        try:
            if distribution_type == "normal":
                return self.transformer.box_muller(numbers_to_transform)
            elif distribution_type == "exponential":
                lambda_param = params.get('lambda', 1.0)
                return self.transformer.exponential(numbers_to_transform, lambda_param)
            elif distribution_type == "poisson":
                lambda_param = params.get('lambda', 1.0)
                return self.transformer.poisson(numbers_to_transform, lambda_param)
            elif distribution_type == "binomial":
                n = params.get('n', 10)
                p = params.get('p', 0.5)
                return self.transformer.binomial(numbers_to_transform, n, p)
            elif distribution_type == "gamma":
                alpha = params.get('alpha', 1.0)
                beta = params.get('beta', 1.0)
                return self.transformer.gamma(numbers_to_transform, alpha, beta)
            elif distribution_type == "beta":
                alpha = params.get('alpha', 1.0)
                beta = params.get('beta', 1.0)
                return self.transformer.beta(numbers_to_transform, alpha, beta)
            else:
                raise ValueError(f"Tipo de distribución no soportada: {distribution_type}")
        except Exception as e:
            raise ValueError(f"Error en la transformación: {str(e)}")