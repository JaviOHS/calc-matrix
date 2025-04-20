from widgets.math_operation_widget import MathOperationWidget
from model.vector_manager import VectorManager
from controller.vector_controller import VectorController
from PySide6.QtWidgets import QVBoxLayout, QTextEdit, QLabel, QWidget
from PySide6.QtCore import Qt

class VectorOpWidget(MathOperationWidget):
    def __init__(self, manager=VectorManager, controller=VectorController, operation_type=None):
        super().__init__(manager, controller, operation_type)
        self.operation_type = operation_type
        self.input_mode = "text"
        self.last_valid_text = ""
        self.setup_ui()

    def setup_ui(self):
        super().setup_ui()

        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)

        title_label = QLabel(f"Ingrese vectores para realizar cálculo de {self.operation_type.replace('_', ' ')}")
        title_label.setAlignment(Qt.AlignLeft)
        self.layout.addWidget(title_label)

        # Entrada de expresión
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(8)

        self.expression_input = QTextEdit()
        self.expression_input.setPlaceholderText("Ejemplo: [2, 3, 4] + [1, 0, 2] - [0, 1, 1]")
        self.expression_input.setMaximumHeight(100)
        input_layout.addWidget(self.expression_input)

        # Área de resultado bajo el input
        self.result_display = QLabel()
        self.result_display.setWordWrap(True)
        self.result_display.setProperty("class", "result-math")
        input_layout.addWidget(self.result_display)

        self.layout.addWidget(input_widget)

        # Creación de botones
        buttons = self.create_buttons()
        self.layout.addWidget(buttons)
        self.setLayout(self.layout)

    def validate_operation(self):
        expr = self.expression_input.toPlainText().strip()

        if not expr:
            return False, "La expresión no puede estar vacía"
        
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
            expr = self.expression_input.toPlainText().strip()

            valid, error = self.validate_operation()
            if not valid:
                self.controller.show_result("Error", error)
                return

            result = self.controller.execute_operation(self.operation_type, expr)

            self.controller.show_result("Resultado", result)
        except Exception as e:
            self.controller.show_result("Error", f"Operación fallida: {str(e)[:100]}")

    def get_input_expression(self):
        expr = self.expression_input.toPlainText().strip()
        if not expr:
            raise ValueError("La expresión no puede estar vacía")
        return expr