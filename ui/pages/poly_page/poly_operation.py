from widgets.math_operation_widget import MathOperationWidget
from model.polynomial_manager import PolynomialManager
from controller.polynomial_controller import PolynomialController
from PySide6.QtWidgets import QVBoxLayout, QTextEdit, QLabel, QWidget, QMessageBox
from PySide6.QtCore import Qt
import re

class PolynomialOpcWidget(MathOperationWidget):
    def __init__(self, manager=PolynomialManager, controller=PolynomialController, operation_type=None):
        super().__init__(manager, controller, operation_type)
        self.operation_type = operation_type
        self.input_mode = "text"
        self.last_valid_text = ""
        self.setup_ui()

    def setup_ui(self):
        super().setup_ui()

        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)

        title_label = QLabel(f"Ingrese polinomio para realizar cálculo de {self.operation_type.replace('_', ' ')}")
        title_label.setAlignment(Qt.AlignLeft)
        self.layout.addWidget(title_label)

        # Entrada de expresión
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(8)

        self.expression_input = QTextEdit()
        self.expression_input.setPlaceholderText("Ejemplo: x^2 + 2x + 1")
        self.expression_input.setMaximumHeight(100)
        self.expression_input.textChanged.connect(self.format_expression)
        input_layout.addWidget(self.expression_input)

        self.preview_label = QLabel("Vista previa...")
        self.preview_label.setWordWrap(True)
        self.preview_label.setProperty("class", "preview-math")
        input_layout.addWidget(self.preview_label)

        self.layout.addWidget(input_widget)

        if self.operation_type == "evaluacion":
            self.x_input_label = QLabel("Ingrese el valor de x:")
            self.x_input_label.setAlignment(Qt.AlignLeft)
            self.x_input = QTextEdit()
            self.x_input.setMaximumHeight(30)
            self.x_input.setPlaceholderText("Ej: 2.5 o -3")
            self.layout.addWidget(self.x_input_label)
            self.layout.addWidget(self.x_input)

        # Creación de botones
        buttons = self.create_buttons()
        self.layout.addWidget(buttons)
        self.calculate_button.clicked.connect(self.execute_operation)

        self.setLayout(self.layout)
        
    def format_expression(self):
        text = self.expression_input.toPlainText()
        try:
            self.controller.parser.parse_expression(text)
            formatted = text.replace(' ', '')
            formatted = formatted.replace('+', ' + ')
            formatted = formatted.replace('-', ' - ')
            formatted = formatted.replace('*', '·')
            formatted = formatted.replace('/', ' ÷ ')
            formatted = formatted.replace('**', '^')
            formatted = re.sub(r'\^(\d+)', r'<sup>\1</sup>', formatted)

            self.preview_label.setText(f"<span style='font-family: Cambria Math; color: #ccc;'>{formatted}</span>")
            self.last_valid_text = text
        except:
            self.preview_label.setText("<span style='color: #ff6666;'>Expresión inválida</span>")

    def validate_operation(self):
        expr = self.expression_input.toPlainText().strip()

        if not expr:
            return False, "La expresión no puede estar vacía"
        
        if self.operation_type == "evaluacion":
            x_value = self.x_input.toPlainText().strip()
            if not x_value:
                return False, "Se necesita un valor x para evaluar los polinomios"
            try:
                float(x_value)
            except ValueError:
                return False, "El valor de x debe ser un número"
        try:
            self.controller.parser.parse_expression(expr)
            return True, ""
        except ValueError as e:
            return False, str(e)
    
    def collect_polynomials(self):
        expr = self.expression_input.toPlainText().strip()
        
        if self.operation_type in {"raices", "derivacion", "integracion", "evaluacion"}:
            try:
                sym_expr = self.controller.parser.parse_expression(expr)
                poly = self.controller.parser.to_polynomial(sym_expr)
                return [poly] # Para operaciones de polinomios, se convierte a polinomio
            except Exception as e:
                raise ValueError(f"Error al convertir la expresión a polinomio: {str(e)}")
        else:
            return [expr] # Para operaciones combinadas, se pasa la expresión en string

    def execute_operation(self):
        expr = self.expression_input.toPlainText().strip()
        valid, error_message = self.validate_operation() # Validación inicial

        if not valid:
            QMessageBox.warning(self, "Error", error_message)
            return
        try:
            if self.operation_type == "evaluacion":
                x_value = self.x_input.toPlainText().strip()
                sym_expr = self.controller.parser.parse_expression(expr)
                poly = self.controller.parser.to_polynomial(sym_expr)
                self.controller.manager.add_polynomial(poly)
                result = self.controller.execute_operation("evaluacion", float(x_value))
                self.show_result([(f"P1", result[0])])
            else:
                if self.operation_type in {"derivacion", "integracion", "raices"}:
                    sym_expr = self.controller.parser.parse_expression(expr)
                    poly = self.controller.parser.to_polynomial(sym_expr)
                    self.controller.manager.add_polynomial(poly)
                else:
                    result = self.controller.execute_operation(self.operation_type, expr)
                    self.show_result(result)
                    return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al calcular la operación: {str(e)}")

    def show_result(self, result):
        formatted_result = self.format_polynomial_html(str(result))
        self.preview_label.setText(formatted_result)

    def format_polynomial_html(self, text: str) -> str:
        formatted = text.replace(' ', '')
        formatted = formatted.replace('+', ' + ')
        formatted = formatted.replace('-', ' - ')
        formatted = formatted.replace('*', '·')
        formatted = formatted.replace('/', ' ÷ ')
        formatted = formatted.replace('**', '^')
        formatted = re.sub(r'\^(\d+)', r'<sup>\1</sup>', formatted)
        return f"<span style='font-family: Cambria Math; color: #ffffff;'>{formatted}</span>"
    
    def get_evaluation_value(self):
        return self.x_input.toPlainText().strip()
    