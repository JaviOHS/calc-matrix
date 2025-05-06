from utils.parsers.expression_parser import ExpressionParser

class SymCalController:
    def __init__(self, manager):
        self.manager = manager
        self.parser = ExpressionParser()

    def compute_derivative(self, expression):
        if not expression:
            raise ValueError("La expresión para derivar no puede estar vacía.")
        
        try:
            parsed_expr = self.parser.parse_expression(expression)
            return self.manager.get_derivative(parsed_expr)
        except Exception as e:
            raise ValueError(str(e))

    def compute_integral(self, expression, limits=None):
        if not expression:
            raise ValueError("La expresión para integrar no puede estar vacía.")
        
        try:
            parsed_expr = self.parser.parse_expression(expression)

            if limits:
                if len(limits) != 2:
                    raise ValueError("Los límites deben ser una tupla de dos elementos.")
                if not all(isinstance(i, (int, float)) for i in limits):
                    raise ValueError("Los límites deben ser numéricos.")
                if limits[0] >= limits[1]:
                    raise ValueError("El límite inferior debe ser menor que el límite superior.")
            
            return self.manager.get_integral(parsed_expr, limits)
        
        except Exception as e:
            raise ValueError(f"Error al calcular la integral: {str(e)}")

    def get_history(self):
        """Obtiene el historial de operaciones realizadas."""
        return self.manager.get_history()

    def clear_history(self):
        """Limpia el historial de operaciones."""
        self.manager.clear()
