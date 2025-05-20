class MatrixController:
    def __init__(self, manager):
        self.manager = manager
        # Mapeo de operaciones a métodos
        self.operations = {
            "plus": self.sum_matrices,
            "substract": self.subtract_all,
            "multiplication": self.multiply_all,
            "division": self.divide_all,
            "determinant": self.get_determinants,
            "reverse": self.get_inverses,
            "transposed": self.get_transpose,
            "system_solver": self.solve_system,
            "eigenvalues": self.get_vector_and_eigenvalues,
        }

    def execute_operation(self, operation_name: str):
        """Ejecuta la operación solicitada por nombre"""
        if operation_name not in self.operations:
            raise ValueError(f"Operación no soportada: {operation_name}.")
        return self.operations[operation_name]()
        
    def validate_operation(self, operation, matrices):
        """Valida que la operación se pueda realizar con las matrices dadas"""
        if not matrices:
            raise ValueError("No hay matrices para operar")
            
        if operation in ['plus', 'substract', 'multiplication']:
            if len(matrices) < 2:
                raise ValueError(f"Se necesitan al menos 2 matrices para realizar esta operación.")
        elif operation in ['division', 'system_solver']:
            if len(matrices) != 2:
                raise ValueError(f"Se necesitan exactamente 2 matrices para realizar esta operación.")
        elif operation in ['determinante', 'inversa', 'valores_propios', 'vectores_propios']:
            if len(matrices) != 1:
                raise ValueError(f"Se necesita exactamente 1 matriz para realizar esta operación.")

    def sum_matrices(self):
        try:
            result = self.manager.sum_all()
            return result
        except ValueError as e:
            raise ValueError(f"Error al sumar las matrices:\n{e}")
        
    def subtract_all(self):
        try:
            result = self.manager.subtract_all()
            return result
        except ValueError as e:
            raise ValueError(f"Error al restar las matrices:\n{e}")
        
    def multiply_all(self):
        try:
            result = self.manager.multiply_all()
            return result
        except ValueError as e:
            raise ValueError(f"Error al multiplicar las matrices:\n{e}")

    def divide_all(self):
        try:
            result = self.manager.divide_all()
            return result
        except ValueError as e:
            raise ValueError(f"Error al dividir las matrices:\n{e}")
        
    def get_determinants(self):
        try:
            results = self.manager.get_determinants()
            return results
        except ValueError as e:
            raise ValueError(f"Error al calcular determinantes:\n{e}")
        
    def get_inverses(self):
        try:
            results = self.manager.get_inverses()
            return results
        except ValueError as e:
            raise ValueError(f"Error al calcular inversas:\n{e}")
        
    def get_transpose(self):
        try:
            results = self.manager.get_transpose()
            return results
        except ValueError as e:
            raise ValueError(f"Error al calcular transpuestas:\n{e}")

    def solve_system(self):
        try:
            result = self.manager.solve_system()
            return result
        except ValueError as e:
            raise ValueError(f"Error al resolver el sistema:\n{e}")

    def get_vector_and_eigenvalues(self):
        try:
            results = self.manager.get_vector_and_eigenvalues()
            return results
        except ValueError as e:
            raise ValueError(f"Error al calcular vectores y valores propios:\n{e}")