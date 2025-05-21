from utils.parsers.expression_parser import ExpressionParser

class SymCalController:
    def __init__(self, manager):
        self.manager = manager
        self.parser = ExpressionParser()

    def compute_derivative(self, expression, var=None):
        if not expression:
            raise ValueError("La expresión para derivar no puede estar vacía.")
        
        if isinstance(expression, str) and ("'" in expression or "=" in expression):
            raise ValueError("Esta expresión parece ser una ecuación diferencial. Por favor, use el módulo correspondiente.")
        
        try:
            parsed_expr = self.parser.parse_expression(expression)
            return self.manager.get_derivative(parsed_expr, var)
        except Exception as e:
            raise ValueError(str(e))

    def compute_integral(self, expression, limits=None, var=None, constant=0):
        if not expression:
            raise ValueError("La expresión para integrar no puede estar vacía.")
        
        if isinstance(expression, str) and ("'" in expression or "=" in expression):
            raise ValueError("Esta expresión parece ser una ecuación diferencial. Por favor, use el módulo correspondiente.")
        
        try:
            parsed_expr = self.parser.parse_expression(expression)

            if limits:
                if len(limits) != 2:
                    raise ValueError("Los límites deben ser una tupla de dos elementos.")
                if not all(isinstance(i, (int, float)) for i in limits):
                    raise ValueError("Los límites deben ser numéricos.")
                if limits[0] >= limits[1]:
                    raise ValueError("El límite inferior debe ser menor que el límite superior.")
            
            return self.manager.get_integral(parsed_expr, limits, var, constant)
        
        except Exception as e:
            raise ValueError(f"Error al calcular la integral:\n{str(e)}")
        
    def solve_differential_equation(self, expression, initial_condition=None, x_range=None):
        if not expression:
            raise ValueError("La ecuación diferencial no puede estar vacía.")
        
        try:
            # Procesar la entrada para que tenga formato similar al numérico
            if isinstance(expression, str):
                # Obtener función y texto para formato numérico
                f, expr_text = self.parser.parse_ode_for_numerical(expression)
                # También mantener la ecuación simbólica para resolución analítica
                symbolic_eq = self.parser.parse_equation(expression)
                
                # Pasar todo al manager en formato (func, texto, eq_simbólica)
                result = self.manager.solve_differential_equation(
                    (f, expr_text, symbolic_eq),
                    initial_condition, 
                    x_range
                )
                return result
            else:
                # Si ya es un objeto procesado
                parsed_expr = expression
                result = self.manager.solve_differential_equation(parsed_expr, initial_condition, x_range)
                return result
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            error_msg = str(e)
            if "invalid syntax" in error_msg:
                raise ValueError("Sintaxis inválida. Verifique el formato de la ecuación.")
            elif "division by zero" in error_msg:
                raise ValueError("Error matemático: división por cero.")
            else:
                raise ValueError(f"Error al resolver la ecuación diferencial: {error_msg}")
                    
    def _validate_ode_params(self, equation, initial_condition, x_range, h):
        """Método auxiliar para validar los parámetros comunes a todos los métodos numéricos"""
        if not equation:
            raise ValueError("La ecuación diferencial no puede estar vacía.")
        
        if len(initial_condition) != 2:
            raise ValueError("La condición inicial debe ser una tupla (x0, y0).")
        
        if len(x_range) != 2 or x_range[0] >= x_range[1]:
            raise ValueError("El rango de x debe ser una tupla (inicio, fin) con inicio < fin.")
        
        if h <= 0:
            raise ValueError("El tamaño de paso h debe ser positivo.")
        
        return True

    def solve_ode_numerical(self, equation, initial_condition, x_range, h=0.1, method="euler"):
        """Método genérico para resolver EDOs con cualquier método numérico"""
        try:
            self._validate_ode_params(equation, initial_condition, x_range, h)
            
            # Parsear la ecuación usando ExpressionParser
            if isinstance(equation, str):
                # Usar el método especial para EDOs numéricas
                f, expr_text = self.parser.parse_ode_for_numerical(equation)
                parsed_expr = (f, expr_text)  # Tupla con función y texto
            else:
                parsed_expr = equation
                
            # Llamar al método apropiado en el manager
            method_func = getattr(self.manager, f"solve_ode_{method}")
            return method_func(parsed_expr, initial_condition, x_range, h)
        except Exception as e:
            raise ValueError(f"Error en método {method}:\n{str(e)}")

    def solve_ode_euler(self, equation, initial_condition, x_range, h=0.1):
        """Resuelve una EDO con el método de Euler"""
        return self.solve_ode_numerical(equation, initial_condition, x_range, h, method="euler")
    
    def solve_ode_heun(self, equation, initial_condition, x_range, h=0.1):
        """Resuelve una EDO con el método de Heun"""
        return self.solve_ode_numerical(equation, initial_condition, x_range, h, method="heun")

    def solve_ode_rk4(self, equation, initial_condition, x_range, h=0.1):
        """Resuelve una EDO con el método de Runge-Kutta de 4º orden"""
        return self.solve_ode_numerical(equation, initial_condition, x_range, h, method="rk4")
    
    def solve_ode_taylor(self, equation, initial_condition, x_range, h=0.1):
        """Resuelve una EDO con el método de Taylor"""
        return self.solve_ode_numerical(equation, initial_condition, x_range, h, method="taylor")
    
    def compare_ode_methods(self, equation, initial_condition, x_range, h=0.1, methods=None, include_analytical=False):
        """Compara diferentes métodos numéricos y opcionalmente la solución analítica para resolver una EDO"""
        try:
            self._validate_ode_params(equation, initial_condition, x_range, h)
            
            # Parsear la ecuación usando ExpressionParser si es una cadena
            if isinstance(equation, str):
                # Usar el método especial para EDOs numéricas
                f, expr_text = self.parser.parse_ode_for_numerical(equation)
                parsed_expr = (f, expr_text)  # Tupla con función y texto
            else:
                parsed_expr = equation
                
            # Llamar al método de comparación en el manager
            return self.manager.compare_ode_methods(parsed_expr, initial_condition, x_range, h, methods, include_analytical)
        except Exception as e:
            raise ValueError(f"No se pudo realizar la comparación:\n{str(e)}")