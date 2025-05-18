import numpy as np
from sympy import symbols, lambdify, sympify
from model._custom_generators import *
from model.graph_manager import GraphManager
from controller.graph_controller import GraphController
from ui.pages.distribution_page.method_config import METHOD_CONFIG

class Distribution:
    def __init__(self, algorithm="mersenne", seed=None, **kwargs):
        self.seed = seed if seed is not None else 12345
        self.algorithm = algorithm
        self.kwargs = kwargs
        self.generator = self._create_generator()
        self.numbers = []
        self.graph_controller = GraphController(GraphManager())

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
            x_random = np.array(self.numbers[:n_points]) * (b - a) + a

            try:
                f_values = f(x_random)
            except Exception as e:
                raise ValueError(f"Error al evaluar la función: {str(e)}")
            
            integral_result = (b - a) * np.mean(f_values) # Calcular la integral aproximada
            
            std_error = (b - a) * np.std(f_values) / np.sqrt(n_points) # Calcular el error estándar
            
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

            # Simulación basada en ecuaciones diferenciales
            steps = int(days / dt)
            for step in range(steps):
                current_S = S[-1]
                current_I = I[-1]
                current_R = R[-1]

                # Calcular cambios usando las ecuaciones diferenciales
                dS = -beta * current_S * current_I / N * dt
                dI = (beta * current_S * current_I / N - gamma * current_I) * dt
                dR = gamma * current_I * dt

                # Actualizar estados
                next_S = current_S + dS
                next_I = current_I + dI
                next_R = current_R + dR

                # Asegurar que los valores sean consistentes
                next_S = max(0, next_S)
                next_I = max(0, next_I)
                next_R = max(0, next_R)

                S.append(next_S)
                I.append(next_I)
                R.append(next_R)
                times.append(times[-1] + dt)

            # Generar el gráfico
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
                    "R0": beta / gamma
                },
                "canvas": canvas
            }

        except Exception as e:
            raise ValueError(f"Error en la simulación de Markov: {str(e)}")

