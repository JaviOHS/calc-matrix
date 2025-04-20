from sympy import sympify, symbols

class SymCalController:
    def __init__(self, manager):
        self.manager = manager

    def compute_derivative(self, expression):
        try:
            # Validación de la expresión
            if not expression:
                raise ValueError("La expresión para derivar no puede estar vacía.")
            
            try:
                sympified_expr = sympify(expression)
            except Exception as e:
                raise ValueError(f"Expresión inválida: {e}")

            return self.manager.get_derivative(expression)
        
        except ValueError as ve:
            print(f"Error: {ve}")
            return None

    def compute_integral(self, expression, limits=None):
        """Calcula la integral de la expresión con validación."""
        try:
            if not expression:
                raise ValueError("La expresión para integrar no puede estar vacía.")
            
            try:
                sympified_expr = sympify(expression)
            except Exception as e:
                raise ValueError(f"Expresión inválida: {e}")

            if limits:
                if len(limits) != 2:
                    raise ValueError("Los límites deben ser una tupla de dos elementos.")
                if not all(isinstance(i, (int, float)) for i in limits):
                    raise ValueError("Los límites deben ser numéricos.")
                if limits[0] >= limits[1]:
                    raise ValueError("El límite inferior debe ser menor que el límite superior.")
            
            # Calculamos la integral
            return self.manager.get_integral(expression, limits)

        except ValueError as ve:
            print(f"Error: {ve}")
            return None

    def get_history(self):
        """Obtiene el historial de operaciones realizadas."""
        return self.manager.get_history()

    def clear_history(self):
        """Limpia el historial de operaciones."""
        self.manager.clear()
