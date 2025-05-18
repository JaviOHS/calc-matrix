from utils.parsers.expression_parser import ExpressionParser

class DistributionController:
    def __init__(self, manager):
        self.manager = manager
        self.parser = ExpressionParser()

    def execute_operation(self, operation, **kwargs):
        try:
            if operation == "generar_numeros":
                return self.generate_numbers(**kwargs)
            elif operation == "monte_carlo_integration":
                return self.monte_carlo_integration(**kwargs)
            elif operation == "markov_epidemic":
                return self.simulate_markov_epidemic(**kwargs)
            else:
                raise ValueError(f"Operación no soportada: {operation}")
        except Exception as e:
            raise ValueError(f"Error en la operación: {str(e)}")

    def generate_numbers(self, algorithm="mersenne", count=5, seed=None, **kwargs):
        try:
            numbers = self.manager.generate_random_numbers(
                count=count,
                algorithm=algorithm,
                seed=seed,
                **kwargs  # Pasamos todos los parámetros adicionales
            )
            return {"success": True, "numbers": numbers, "count": len(numbers), "algorithm": algorithm}
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    def monte_carlo_integration(self, expression, a, b, n_points=10000, algorithm="mersenne", seed=None, **kwargs):
        """Realiza la integración numérica por Monte Carlo."""
        try:
            if not expression:
                raise ValueError("La expresión no puede estar vacía.")
                
            try:
                a = float(a)
                b = float(b)
            except ValueError:
                raise ValueError("Los límites de integración deben ser números.")
                
            try:
                n_points = int(n_points)
                if n_points <= 0:
                    raise ValueError("El número de puntos debe ser positivo.")
            except ValueError:
                raise ValueError("El número de puntos debe ser un entero positivo.")
                
            parsed_expr = self.parser.parse_expression(expression)
            result = self.manager.calculate_monte_carlo_integration(parsed_expr, a, b, n_points, algorithm, seed, **kwargs)
            
            return {"success": True,**result}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def simulate_markov_epidemic(self, population=1000, initial_infected=1, initial_recovered=0, beta=0.3, gamma=0.1, days=30, dt=0.1,algorithm="mersenne", seed=None, **kwargs):
        """Controla la simulación de una epidemia usando el modelo de Markov."""
        try:
            try:
                population = int(population)
                if population <= 0:
                    raise ValueError("La población debe ser un número positivo.")
                    
                initial_infected = int(initial_infected)
                if initial_infected < 0:
                    raise ValueError("El número inicial de infectados debe ser no negativo.")
                    
                initial_recovered = int(initial_recovered)
                if initial_recovered < 0:
                    raise ValueError("El número inicial de recuperados debe ser no negativo.")
                
                if initial_infected + initial_recovered > population:
                    raise ValueError("La suma de infectados y recuperados no puede superar la población total.")
                
                beta = float(beta)
                if not 0 <= beta <= 1:
                    raise ValueError("Beta debe estar entre 0 y 1.")
                    
                gamma = float(gamma)
                if not 0 <= gamma <= 1:
                    raise ValueError("Gamma debe estar entre 0 y 1.")
                    
                days = int(days)
                if days <= 0:
                    raise ValueError("El número de días debe ser positivo.")
                    
                dt = float(dt)
                if dt <= 0:
                    raise ValueError("El intervalo de tiempo debe ser positivo.")
            except ValueError as e:
                if "could not convert" in str(e):
                    raise ValueError("Todos los parámetros deben ser numéricos.")
                raise e
            
            # Construir diccionario de parámetros
            params = {
                'population': population,
                'initial_infected': initial_infected,
                'initial_recovered': initial_recovered,
                'beta': beta,
                'gamma': gamma,
                'days': days,
                'dt': dt
            }
            
            # Llamar al método del manager y obtener resultado con canvas
            result = self.manager.simulate_markov_epidemic(params, algorithm, seed, **kwargs)
            
            # Procesar el resultado incluyendo el canvas
            processed_result = {
                'times': result['times'],
                'susceptible': result['susceptible'],
                'infected': result['infected'],
                'recovered': result['recovered'],
                'parameters': result['parameters'],
                'canvas': result['canvas']
            }
            
            return {"success": True, "result": processed_result,"message": "Simulación completada exitosamente."}
            
        except Exception as e:
            return {"success": False, "error": str(e),"message": "Error en la simulación de la epidemia."}
