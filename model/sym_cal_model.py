from sympy import symbols, diff, integrate, sympify, Function, lambdify
import sympy as sp

class SymCalModel:
    def __init__(self):
        self.x = symbols('x')
        self.y = symbols('y')
        self.history = []

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
    
    def solve_differential_equation(self, equation):
        x = self.x
        y = Function('y')(x)
        
        try:
            # Asegurarse de que la ecuación esté en términos de y(x)
            if not isinstance(equation, sp.Eq):
                equation = sp.Eq(equation, 0)
                
            # Resolver la ecuación diferencial
            solution = sp.dsolve(equation, y)
            self.history.append(("Ecuación diferencial", str(equation), solution))
            return solution
        except Exception as e:
            raise ValueError(f"No se pudo resolver la ecuación diferencial: {str(e)}")
        
    def solve_ode_euler(self, equation, initial_condition, x_range, h=0.1):
        """
        Resuelve una EDO usando el método de Euler.
        
        Args:
            equation: Ecuación diferencial (e.g., "y' = x + y")
            initial_condition: Tupla (x0, y0)
            x_range: Tupla (x_inicio, x_fin)
            h: Tamaño del paso
            
        Returns:
            Lista de tuplas (x, y) con la solución numérica
        """
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
            
        self.history.append(("Euler", equation, (x_vals, y_vals)))
        return list(zip(x_vals, y_vals))
            
    def get_history(self):
        return self.history

    def clear(self):
        self.history.clear()
