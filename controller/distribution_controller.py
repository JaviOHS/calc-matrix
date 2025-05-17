class DistributionController:
    def __init__(self, manager):
        self.manager = manager

    def execute_operation(self, operation, **kwargs):
        try:
            if operation == "generar_numeros":
                return self.generate_numbers(**kwargs)
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
