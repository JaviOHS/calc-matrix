from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QTextEdit, QWidget
from PySide6.QtCore import Qt
from ui.widgets.expression_op_widget import ExpressionOpWidget
from utils.formatting import format_math_expression

class SymCalOpWidget(ExpressionOpWidget):
    def __init__(self, manager, controller, operation_type=None):
        self.manager = manager
        self.controller = controller
        self.operation_type = operation_type

        input_label = f"Ingresa una expresión para realizar cálculo de {operation_type.replace('_', ' ')}:"
        placeholder = "Ejemplo: 2x^2 + 2x"

        super().__init__(
            manager,
            controller,
            operation_type=operation_type,
            placeholder=placeholder,
            input_label=input_label,
            use_dialog_for_result=False
        )

        self.add_additional_inputs()

    def add_additional_inputs(self):
        if self.operation_type == "integrales":
            self.limits_widget = QWidget()
            limits_layout = QHBoxLayout(self.limits_widget)
            limits_layout.setContentsMargins(20, 0, 0, 0)

            limits_layout.addWidget(QLabel("Desde x ="))
            self.lower_limit = QSpinBox()
            self.lower_limit.setRange(-1000, 1000)
            self.lower_limit.setValue(0)
            self.lower_limit.setAlignment(Qt.AlignCenter)
            limits_layout.addWidget(self.lower_limit)

            limits_layout.addWidget(QLabel("Hasta x ="))
            self.upper_limit = QSpinBox()
            self.upper_limit.setRange(-1000, 1000)
            self.upper_limit.setValue(1)
            self.upper_limit.setAlignment(Qt.AlignCenter)
            limits_layout.addWidget(self.upper_limit)
            limits_layout.addStretch() # Problema

            self.layout.insertWidget(1, self.limits_widget)

    def validate_operation(self):
        expression = self.get_input_expression().strip()
        if not expression:
            return False, "Por favor ingresa una expresión para continuar."
        try:
            # Validación tentativa
            self.controller.parser.parse_expression(expression)
            return True, ""
        except Exception as e:
            return False, f"Expresión inválida: {str(e)}"

    def execute_operation(self):
        expression = self.get_input_expression().strip()
        if self.operation_type == "derivadas":
            result = self.controller.compute_derivative(expression)
        elif self.operation_type == "integrales":
            limits = (self.lower_limit.value(), self.upper_limit.value())
            result = self.controller.compute_integral(expression, limits)
        else:
            raise ValueError("Tipo de operación desconocido.")
        return result

    def prepare_result_display(self, result):
        expr = self.get_input_expression().strip()
        return format_math_expression(expr, result, operation_type="polynomial")
    
