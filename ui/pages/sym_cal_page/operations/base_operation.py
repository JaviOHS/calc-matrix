from ui.widgets.expression_op_widget import ExpressionOpWidget
from utils.formating.formatting import format_math_expression

class BaseSymCalOperation(ExpressionOpWidget):
    def __init__(self, manager, controller, operation_type=None, placeholder="", input_label="", use_dialog_for_result=False):
        self.manager = manager
        self.controller = controller
        self.operation_type = operation_type
        super().__init__(manager, controller, operation_type=operation_type, 
                        placeholder=placeholder, input_label=input_label,
                        use_dialog_for_result=use_dialog_for_result)

    def validate_operation(self):
        expression = self.get_input_expression().strip()
        if not expression:
            return False, "Por favor ingresa una expresión para continuar."
        try:
            if self.operation_type == "differential_equation":
                self.controller.parser.parse_equation(expression)
            else:
                self.controller.parser.parse_expression(expression)
            return True, ""
        except Exception as e:
            return False, f"Expresión inválida: {str(e)}"

    def on_calculate_clicked(self):
        """Maneja el cálculo y muestra de resultados"""
        is_valid, error_message = self.validate_operation()
            
        if not is_valid:
           return False, error_message
        
        try:
            result = self.execute_operation()
            formatted_result = self.prepare_result_display(result)
            self.process_operation_result(formatted_result)
            return True, "Operación completada exitosamente"
        except Exception as e:
           return False, f"Error al calcular la operación: {str(e)}"

    def prepare_result_display(self, result):
        expr_str = self.get_input_expression().strip()
        try:
            if self.operation_type in ["derivative", "integral", "differential_equation"]:
                parsed_expr = self.controller.parser.parse_equation(expr_str)
                method = self.de_method_selector.currentData() if hasattr(self, 'de_method_selector') else None
                
                # Si hay un canvas en el resultado (para métodos numéricos)
                if isinstance(result, dict) and "solution" in result and "canvas" in result:
                    html_content = format_math_expression(parsed_expr, result["solution"], 
                                                        self.operation_type, method=method)
                    return {
                        "html": html_content,
                        "canvas": result["canvas"]
                    }
                else:
                    return format_math_expression(parsed_expr, result, self.operation_type, method=method)
            else:
                parsed_expr = self.controller.parser.parse_expression(expr_str)
                return format_math_expression(parsed_expr, result, self.operation_type)
        except Exception as e:
            raise ValueError(f"Ocurrió un error: {str(e)}")

    def execute_operation(self):
        """Método que debe ser implementado por las clases hijas"""
        raise NotImplementedError("Las clases hijas deben implementar execute_operation()")