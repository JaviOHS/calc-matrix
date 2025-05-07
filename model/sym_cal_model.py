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

    def derive(self, expression: str):
        f = sympify(expression)
        result = diff(f, self.x)
        self.history.append(("Derivada", expression, result))
        return result

    def integrate(self, expression: str, limits=None):
        f = sympify(expression)
        if limits:
            result = integrate(f, (self.x, *limits))
        else:
            result = integrate(f, self.x)
        self.history.append(("Integral", expression, result, limits))
        return result
    
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
            raise ValueError(f"No se pudo resolver la ecuación diferencial: {str(e)}")
        
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
            print(f"Error preparando función de solución: {e}")
            return None
    
    def solve_ode_euler(self, equation, initial_condition, x_range, h=0.1):
        x0, y0 = initial_condition
        x_start, x_end = x_range
        x_vals = []
        y_vals = []
        
        # Convertir la ecuación a una función f(x, y)
        try:
            # Parsear la ecuación (ejemplo: "y' = x + y" -> "x + y")
            if '=' in equation:
                rhs = equation.split('=')[1].strip()
            else:
                rhs = equation
                
            f = lambdify([symbols('x'), symbols('y')], sympify(rhs))
        except Exception as e:
            raise ValueError(f"No se pudo parsear la ecuación: {str(e)}")
        
        # Implementación del método de Euler
        x = x0
        y = y0
        x_vals.append(x)
        y_vals.append(y)
        
        while x < x_end:
            y = y + h * f(x, y)
            x = x + h
            x_vals.append(x)
            y_vals.append(y)
        
        # Crear la lista de puntos de solución
        solution_points = list(zip(x_vals, y_vals))
        
        # Generar el gráfico usando el GraphController existente
        equation_display = f"y' = {rhs}"
        canvas = self.graph_controller.generate_ode_solution_canvas(
            equation=equation_display,
            solution_points=solution_points,
            initial_condition=initial_condition,
            x_range=x_range,
            title=f"Método de Euler - {len(solution_points)} puntos"
        )
        
        self.history.append(("Euler", equation, solution_points))
        
        # Devolver tanto la solución como el canvas
        return {
            "solution": solution_points,
            "canvas": canvas
        }
            
    def get_history(self):
        return self.history

    def clear(self):
        self.history.clear()
