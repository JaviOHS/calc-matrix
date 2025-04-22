class MatrixController:
    def __init__(self, manager):
        self.manager = manager

    def execute_operation(self, operation_name: str):
        if operation_name == "suma":
            return self.sum_matrices()
        elif operation_name == "resta":
            return self.subtract_all()
        elif operation_name == "multiplicacion":
            return self.multiply_all()
        elif operation_name == "division":
            return self.divide_all()
        elif operation_name == "determinante":
            return self.get_determinants()
        elif operation_name == "inversa":
            return self.get_inverses()
        elif operation_name == "sistema":
            return self.solve_system()
        else:
            raise ValueError(f"Operación no soportada: {operation_name}")

    def sum_matrices(self):
        try:
            result = self.manager.sum_all()
            return result
        except ValueError as e:
            raise ValueError(f"Error al sumar las matrices: {e}")
        
    def subtract_all(self):
        try:
            result = self.manager.subtract_all()
            return result
        except ValueError as e:
            raise ValueError(f"Error al restar las matrices: {e}")
        
    def multiply_all(self):
        try:
            result = self.manager.multiply_all()
            return result
        except ValueError as e:
            raise ValueError(f"Error al multiplicar las matrices: {e}")

    def divide_all(self):
        try:
            result = self.manager.divide_all()
            return result
        except ValueError as e:
            raise ValueError(f"Error al dividir las matrices: {e}")
        
    def get_determinants(self):
        try:
            results = self.manager.get_determinants()
            return results
        except ValueError as e:
            raise ValueError(f"Error al calcular determinantes: {e}")
        
    def get_inverses(self):
        try:
            results = self.manager.get_inverses()
            return results
        except ValueError as e:
            raise ValueError(f"Error al calcular inversas: {e}")

    def solve_system(self):
        try:
            result = self.manager.solve_system()
            return result
        except ValueError as e:
            raise ValueError(f"Error al resolver el sistema: {e}")
