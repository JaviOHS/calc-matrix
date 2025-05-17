from ui.widgets.expression_op_widget import ExpressionOpWidget
from model.vector_manager import VectorManager
from controller.vector_controller import VectorController
import re
from utils.formatting import format_math_expression

ALLOWED_VECTOR_CHARS = re.compile(r'^[\[\]\d,\s+\-*/.\·]*$')
class VectorOpWidget(ExpressionOpWidget):
    def __init__(self, manager=VectorManager, controller=VectorController, operation_type=None):
        if operation_type == "operaciones_basicas":
            input_label = "Ingrese varios vectores para realizar cálculo de operaciones combinadas:"
            placeholder = "Ejemplo: [2, 3, 4] + [1, 0, 2]"
        elif operation_type == "magnitud":
            input_label = "Ingrese un vector para calcular su magnitud:"
            placeholder = "Ejemplo: [2, 3, 4]"
        else:
            input_label = f"Ingrese dos vectores para realizar cálculo de {operation_type.replace('_', ' ')}:"
            placeholder = "Ejemplo: [2, 3, 4][1, 0, 2]"
        super().__init__(manager, controller, operation_type, placeholder=placeholder, input_label=input_label)
        self.input_mode = "text"
        self.last_valid_text = ""
        self.custom_setup()

    def custom_setup(self):
        self.expression_input.textChanged.connect(self.filter_vector_input)

    def validate_operation(self):
        expr = self.expression_input.toPlainText().strip()
        
        try:
            self.controller.parser.parse_expression(expr)
            return True, ""
        except ValueError as e:
            return False, str(e)

    def collect_vectors(self):
        expr = self.expression_input.toPlainText().strip()
        try:
            sym_expr = self.controller.parser.parse_expression(expr)
            vector = self.controller.parser.to_vector(sym_expr)
            return [vector]
        except Exception as e:
            raise ValueError(f"Error al convertir la expresión a vector: {str(e)}")

    def execute_operation(self):
        try:
            expr = self.get_input_expression()
            valid, error = self.validate_operation()
            if not valid:
                self.display_result(f"<span style='color:red'>Error: {error}</span>")
                return

            result = self.controller.execute_operation(self.operation_type, expr)
            if result is None:
                self.display_result("<span style='color:red'>Error en el cálculo</span>")
                return

            # Usar el formateador unificado para vectores
            formatted_output = format_math_expression(expr, result, "vector")
            self.display_result(formatted_output)

        except Exception as e:
            self.display_result(f"<span style='color:red'>Error: {str(e)[:100]}</span>")
            
    def filter_vector_input(self):
        current_text = self.expression_input.toPlainText()
        if ALLOWED_VECTOR_CHARS.match(current_text):
            self.last_valid_text = current_text
        else:
            cursor = self.expression_input.textCursor()
            self.expression_input.blockSignals(True)
            self.expression_input.setPlainText(self.last_valid_text)
            self.expression_input.blockSignals(False)
            self.expression_input.setTextCursor(cursor)