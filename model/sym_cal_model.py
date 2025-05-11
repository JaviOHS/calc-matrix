from controller.graph_controller import GraphController 
from model.graph_manager import GraphManager
from sympy import symbols, diff, integrate, sympify, Function, lambdify
import sympy as sp
import numpy as np

class SymCalModel:
    def __init__(self):
        self.x = symbols('x')
        self.y = symbols('y')
        self.history = []
        self.graph_controller = GraphController(GraphManager())

    def derive(self, expression, var=None):
        try:
            # Si la expresión es una lista, se asume que es un polinomio
            if isinstance(expression, list):
                from model.polynomial_model import Polynomial
                
                coeffs = expression
                variable = var or 'x'
                
                # Implementación para coeffs = [an, ..., a1, a0]
                if len(coeffs) <= 1:
                    result = Polynomial([0], var=variable)
                else:
                    n = len(coeffs) - 1
                    new_coeffs = [(n - i) * coeffs[i] for i in range(len(coeffs) - 1)]
                    result = Polynomial(new_coeffs, var=variable)
                    
                self.history.append(("Derivada polinomio", str(expression), result))
                return result
            
            # Si es una instancia de Polynomial, convertirlo a expresión simbólica
            from model.polynomial_model import Polynomial
            if isinstance(expression, Polynomial):
                sym_expr = expression.to_sympy_expr()
                variable = symbols(expression.var)
                result = diff(sym_expr, variable)
                
                # Intentar convertir el resultado a un polinomio
                try:
                    poly_result = Polynomial(sp.Poly(result, variable).all_coeffs(), var=expression.var)
                    self.history.append(("Derivada polinomio", str(expression), poly_result))
                    return poly_result
                except:
                    # Si no se puede convertir a polinomio, devolver la expresión simbólica
                    self.history.append(("Derivada", str(expression), result))
                    return result
                
            f = sympify(expression)
            variable = symbols(var) if var else self.x
            result = diff(f, variable)
            self.history.append(("Derivada", expression, result))
            return result
        except Exception as e:
            raise ValueError(f"Error al derivar: {str(e)}")
    
    def integrate(self, expression, limits=None, var=None, constant=0):
        try:
            # Si la expresión es una lista, se asume que es un polinomio
            if isinstance(expression, list):
                from model.polynomial_model import Polynomial
                coeffs = expression
                variable = var or 'x'
                
                # Implementación CORRECTA para coeffs = [an, ..., a1, a0]
                new_coeffs = []
                n = len(coeffs) - 1  # Grado máximo del polinomio
                
                for i in range(len(coeffs)):
                    # Para cada término a_i*x^(n-i), la integral es (a_i/(n-i+1))*x^(n-i+1)
                    new_coeff = coeffs[i] / (n - i + 1)
                    new_coeffs.append(new_coeff)
                
                # Añadir la constante de integración como nuevo término independiente
                new_coeffs.append(constant)
                
                poly = Polynomial(new_coeffs, var=variable)
                
                if limits:
                    lower, upper = limits
                    result = poly.evaluate(upper) - poly.evaluate(lower)
                    self.history.append(("Integral definida polinomio", str(expression), result, limits))
                    return result
                else:
                    self.history.append(("Integral polinomio", str(expression), poly))
                    return poly
                  
            # Si es una instancia de Polynomial, obtenemos sus coeficientes
            from model.polynomial_model import Polynomial
            if isinstance(expression, Polynomial):
                return self.integrate(expression.coefficients, limits=limits, var=expression.var, constant=constant)
            
            f = sympify(expression)
            variable = symbols(var) if var else self.x
            
            if limits:
                result = integrate(f, (variable, *limits))
            else:
                result = integrate(f, variable)
                
            self.history.append(("Integral", expression, result, limits))
            return result
        except Exception as e:
            raise ValueError(f"Error al integrar:\n{str(e)}")
    
    def solve_differential_equation(self, equation, initial_condition=None, x_range=None):
        x = self.x
        y = Function('y')(x)
        
        try:
            # Asegurarse de que la ecuación esté en términos de y(x)
            if not isinstance(equation, sp.Eq):
                equation = sp.Eq(equation, 0)
                
            # Resolver la ecuación diferencial
            solution = sp.dsolve(equation, y)
            self.history.append(("Ecuación diferencial", str(equation), solution))
            
            if initial_condition and x_range:
                x0, y0 = initial_condition
                solution_func = self._prepare_solution_function(solution, x0, y0)
                
                if solution_func:
                    # Generar puntos para graficar
                    x_vals = np.linspace(x_range[0], x_range[1], 20)
                    y_vals = [solution_func(xi) for xi in x_vals]
                    solution_points = list(zip(x_vals, y_vals))
                    
                    # Generar canvas
                    canvas = self.graph_controller.generate_ode_solution_canvas(
                        equation=str(equation),
                        solution_points=solution_points,
                        initial_condition=initial_condition,
                        x_range=x_range,
                        title=f"Solución Analítica"
                    )
                    
                    return {
                        "solution": solution,
                        "canvas": canvas
                    }
            
            return solution
        except Exception as e:
            raise ValueError(f"No se pudo resolver la ecuación diferencial:\n{str(e)}")
        
    def _prepare_solution_function(self, solution, x0, y0):
        """Convierte una solución simbólica en una función numérica, aplicando la condición inicial"""
        try:
            solution_rhs = solution.rhs
            
            # Si hay constantes de integración, hay que resolverlas
            if 'C1' in str(solution_rhs) or 'C2' in str(solution_rhs):
                # Resuelve para las constantes usando la condición inicial
                const_eq = solution_rhs.subs(self.x, x0) - y0
                const_sol = sp.solve(const_eq, 'C1')
                if const_sol:
                    # Sustituye la constante resuelta en la solución
                    solution_rhs = solution_rhs.subs('C1', const_sol[0])
                
            # Convierte la solución simbólica a una función numérica
            solution_func = sp.lambdify(self.x, solution_rhs)
            return solution_func
        except Exception as e:
            print(f"Error preparando función de solución:\n{e}")
            return None
    
    def _parse_ode_equation(self, equation):
        """Parsea una ecuación diferencial y devuelve la función f(x,y) para y'=f(x,y)"""
        try:
            # Parsear la ecuación (ejemplo: "y' = x + y" -> "x + y")
            if '=' in equation:
                rhs = equation.split('=')[1].strip()
            else:
                rhs = equation
                
            f = lambdify([symbols('x'), symbols('y')], sympify(rhs))
            return f, rhs
        except Exception as e:
            raise ValueError(f"No se pudo parsear la ecuación:\n{str(e)}")

    def solve_ode_numerical(self, equation, initial_condition, x_range, h=0.1, method="euler"):
        """Método general para resolver EDOs con diferentes métodos numéricos"""
        x0, y0 = initial_condition
        x_start, x_end = x_range
        x_vals = [x0]
        y_vals = [y0]
        
        # Obtener la función f(x,y) de la ecuación y'=f(x,y)
        f, rhs = self._parse_ode_equation(equation)
        
        # Inicializar valores
        x = x0
        y = y0
        
        # Resolver la ecuación paso a paso según el método elegido
        while x < x_end:
            if method == "euler":
                # Método de Euler: y_{n+1} = y_n + h * f(x_n, y_n)
                y = y + h * f(x, y)
            
            elif method == "heun":
                # Método de Heun (predictor-corrector)
                k1 = f(x, y)
                y_pred = y + h * k1
                k2 = f(x + h, y_pred)
                y = y + h * (k1 + k2) / 2
                
            elif method == "rk4":
                # Método de Runge-Kutta de 4to orden
                k1 = f(x, y)
                k2 = f(x + h/2, y + h*k1/2)
                k3 = f(x + h/2, y + h*k2/2)
                k4 = f(x + h, y + h*k3)
                y = y + h * (k1 + 2*k2 + 2*k3 + k4) / 6
            
            # Actualizar x y guardar los valores
            x = x + h
            x_vals.append(x)
            y_vals.append(y)
        
        # Crear la lista de puntos de solución
        solution_points = list(zip(x_vals, y_vals))
        
        # Obtener título según el método
        method_titles = {
            "euler": "Método de Euler",
            "heun": "Método de Heun",
            "rk4": "Método de Runge-Kutta (4º orden)"
        }
        method_title = method_titles.get(method, "Método Numérico")
        
        # Generar el gráfico
        equation_display = f"y' = {rhs}"
        canvas = self.graph_controller.generate_ode_solution_canvas(
            equation=equation_display,
            solution_points=solution_points,
            initial_condition=initial_condition,
            x_range=x_range,
            title=f"{method_title} - {len(solution_points)} puntos"
        )
        
        self.history.append((method.capitalize(), equation, solution_points))
        
        # Devolver tanto la solución como el canvas
        return {
            "solution": solution_points,
            "canvas": canvas
        }

    def solve_ode_euler(self, equation, initial_condition, x_range, h=0.1):
        """Resuelve una ecuación diferencial usando el método de Euler"""
        return self.solve_ode_numerical(equation, initial_condition, x_range, h, method="euler")
        
    def solve_ode_heun(self, equation, initial_condition, x_range, h=0.1):
        """Resuelve una ecuación diferencial usando el método de Heun"""
        return self.solve_ode_numerical(equation, initial_condition, x_range, h, method="heun")
        
    def solve_ode_rk4(self, equation, initial_condition, x_range, h=0.1):
        """Resuelve una ecuación diferencial usando Runge-Kutta de 4º orden"""
        return self.solve_ode_numerical(equation, initial_condition, x_range, h, method="rk4")
            
    def get_history(self):
        return self.history

    def clear(self):
        self.history.clear()
