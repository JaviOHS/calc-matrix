from ui.pages.polynomial_page.operation_widgets.base_operation import PolynomialOperationWidget
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QTextEdit, QLabel, QWidget, QMessageBox
from PySide6.QtCore import Qt
import re

class PolynomialOpcWidget(PolynomialOperationWidget):
    def __init__(self, manager, controller, operation_type):
        super().__init__(manager, controller, operation_type)
        self.operation_type = operation_type
        self.input_mode = "text"
        self.last_valid_text = ""
        self.calculate_button.clicked.connect(self.execute_operation)

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)

        title_label = QLabel(f"Ingrese polinomio para realizar cálculo de {self.operation_type.replace('_', ' ')}")
        title_label.setAlignment(Qt.AlignLeft)
        self.layout.addWidget(title_label)

        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(8)

        # Campo de entrada para la expresión
        self.expression_input = QTextEdit()
        self.expression_input.setPlaceholderText("Ejemplo:\n[(2x^4+3x^3-4x^2+1) + (2x+1)] - (2x-1)\nO solo el polinomio: x^2 + 2x + 1")
        self.expression_input.setMaximumHeight(100)
        self.expression_input.textChanged.connect(self.format_expression)
        input_layout.addWidget(self.expression_input)

        # Vista previa
        self.preview_label = QLabel("Vista previa...")
        self.preview_label.setWordWrap(True)
        self.preview_label.setProperty("class", "preview-math")
        input_layout.addWidget(self.preview_label)

        self.layout.addWidget(input_widget)

        # Campo de entrada para evaluación
        if self.operation_type == "evaluacion":
            self.x_input_label = QLabel("Ingrese el valor de x:")
            self.x_input_label.setAlignment(Qt.AlignLeft)
            self.x_input = QTextEdit()
            self.x_input.setMaximumHeight(30)
            self.x_input.setPlaceholderText("Ej: 2.5 o -3")
            self.layout.addWidget(self.x_input_label)
            self.layout.addWidget(self.x_input)

        # Botones
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        self.cancel_button = QPushButton("Cancelar")
        self.calculate_button = QPushButton("Calcular")
        self.cancel_button.setStyleSheet("padding: 6px 12px;")
        self.calculate_button.setStyleSheet("padding: 6px 12px;")

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.calculate_button)
        self.layout.addWidget(buttons_widget)

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
    