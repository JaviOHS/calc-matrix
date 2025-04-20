from widgets.math_operation_widget import MathOperationWidget
from model.polynomial_manager import PolynomialManager
from controller.polynomial_controller import PolynomialController
from PySide6.QtWidgets import QVBoxLayout, QTextEdit, QLabel, QWidget, QMessageBox, QDoubleSpinBox, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCharFormat, QFont
from utils.formatting import format_polynomial_html


class PolynomialOpWidget(MathOperationWidget):
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
        
        self.expression_input.textChanged.connect(self.format_expression_in_input)
        input_layout.addWidget(self.expression_input)

        # Vista previa eliminada
        self.preview_label = QLabel()
        self.preview_label.setWordWrap(True)
        self.preview_label.setProperty("class", "result-math")
        input_layout.addWidget(self.preview_label)

        self.layout.addWidget(input_widget)

        if self.operation_type == "evaluacion":
            # Crear un widget contenedor para la entrada de x
            x_input_widget = QWidget()
            x_input_layout = QHBoxLayout(x_input_widget)
            x_input_layout.setContentsMargins(0, 0, 0, 0)
            
            self.x_input_label = QLabel("Ingrese valor de x:")
            self.x_input_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            # Usar QDoubleSpinBox en lugar de QTextEdit
            self.x_input = QDoubleSpinBox()
            self.x_input.setObjectName("dim_spinbox")
            self.x_input.setRange(-999999, 999999)
            self.x_input.setSingleStep(0.1)
            self.x_input.setDecimals(2)
            self.x_input.setMaximumWidth(150)
            self.x_input.setAlignment(Qt.AlignCenter)
            self.x_input.setValue(4.0)
            
            x_input_layout.addWidget(self.x_input_label)
            x_input_layout.addWidget(self.x_input)
            x_input_layout.addStretch()
            
            self.layout.addWidget(x_input_widget)

        # Creación de botones
        buttons = self.create_buttons()
        self.layout.addWidget(buttons)
        self.calculate_button.clicked.connect(self.execute_operation)

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

    def collect_polynomials(self):
        expr = self.expression_input.toPlainText().strip()

        if self.operation_type in {"raices", "derivacion", "integracion", "evaluacion"}:
            try:
                sym_expr = self.controller.parser.parse_expression(expr)
                poly = self.controller.parser.to_polynomial(sym_expr)
                return [poly]  # Para operaciones de polinomios, se convierte a polinomio
            except Exception as e:
                raise ValueError(f"Error al convertir la expresión a polinomio: {str(e)}")
        else:
            return [expr]  # Para operaciones combinadas, se pasa la expresión en string

    def execute_operation(self):
        expr = self.expression_input.toPlainText().strip()
        valid, error_message = self.validate_operation()  # Validación inicial

        if not valid:
            QMessageBox.warning(self, "Error", error_message)
            return
        try:
            if self.operation_type == "evaluacion":
                x_value = self.x_input.value()  # Obtenemos el valor del spinbox
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
        expression = self.expression_input.toPlainText().strip()
        formatted_expr = format_polynomial_html(expression)
        formatted_result = format_polynomial_html(str(result))

        self.preview_label.setText(
            f"<span style='font-family: Dosis; color: #aaa;'>Resultado:</span><br>"
            f"<span style='font-family: Cambria Math;'>{formatted_expr}</span> = "
            f"<span style='font-family: Cambria Math; color: rgba(114, 228, 140, 0.7);'>{formatted_result}</span>"
        )


    def get_evaluation_value(self):
        return str(self.x_input.value())

    def format_expression_in_input(self):
        cursor = self.expression_input.textCursor()
        position = cursor.position()

        text = self.expression_input.toPlainText()

        # Guardar el texto y evitar bucle de señal
        self.expression_input.blockSignals(True)

        # Vamos a construir un nuevo documento formateado
        self.expression_input.clear()
        new_cursor = self.expression_input.textCursor()

        base_format = QTextCharFormat()
        base_format.setFont(QFont("Cambria Math", 14))

        super_format = QTextCharFormat(base_format)
        super_format.setVerticalAlignment(QTextCharFormat.AlignSuperScript)

        i = 0
        while i < len(text):
            if text[i] == '^':
                new_cursor.insertText('^', base_format)  # Insertamos el carácter visible
                i += 1
                # Si hay un dígito (o varios) después de ^
                start = i
                while i < len(text) and text[i].isdigit():
                    new_cursor.insertText(text[i], super_format)
                    i += 1

            else:
                new_cursor.insertText(text[i], base_format)
                i += 1

        # Restaurar posición del cursor
        new_cursor.setPosition(min(position, len(self.expression_input.toPlainText())))
        self.expression_input.setTextCursor(new_cursor)

        self.expression_input.blockSignals(False)

    