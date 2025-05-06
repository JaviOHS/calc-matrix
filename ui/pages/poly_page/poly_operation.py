from ui.widgets.expression_op_widget import ExpressionOpWidget
from model.polynomial_manager import PolynomialManager
from controller.polynomial_controller import PolynomialController
from PySide6.QtWidgets import QLabel, QWidget, QDoubleSpinBox, QHBoxLayout
from PySide6.QtCore import Qt
from utils.formatting import format_math_expression

class PolynomialOpWidget(ExpressionOpWidget):
    def __init__(self, manager=PolynomialManager, controller=PolynomialController, operation_type=None):
        input_label = f"Ingrese el polinomio para realizar cálculo de {operation_type.replace("_", " ")}:"
        placeholder = "Ejemplo: x^2 + 2x + 1"
        super().__init__(manager, controller, operation_type, placeholder=placeholder, input_label=input_label)
        self.input_mode = "text"
        self.last_valid_text = ""
        self._parsed_expr = None 
        self.custom_setup()

    def custom_setup(self):
        if self.operation_type == "evaluacion":
            # Crear un contenedor horizontal para toda la línea
            top_row = QWidget()
            top_layout = QHBoxLayout(top_row)
            top_layout.setContentsMargins(20, 0, 0, 0)
            top_layout.setSpacing(10)
            
            # Texto descriptivo
            instruction_label = QLabel("Ingrese el polinomio y el valor de `x` a evaluar:") # Mismo label para valores de x
            top_layout.addWidget(instruction_label)
            
            # Contenedor para el input de x
            x_container = QWidget()
            x_layout = QHBoxLayout(x_container)
            x_layout.setContentsMargins(0, 0, 0, 0)
            
            x_layout.addWidget(QLabel("x ="))
            self.x_input = QDoubleSpinBox()
            self.x_input.setRange(-999999, 999999)
            self.x_input.setValue(1.0)
            self.x_input.setFixedWidth(100)
            self.x_input.setAlignment(Qt.AlignCenter)
            self.x_input.setObjectName("dim_spinbox")
            x_layout.addWidget(self.x_input)
            
            top_layout.addWidget(x_container)
            top_layout.addStretch()  # Empuja todo a la izquierda
            
            # Reemplazar el título original
            if self.layout.count() > 0:
                old_item = self.layout.takeAt(0)
                if old_item.widget():
                    old_item.widget().deleteLater()
            
            self.layout.insertWidget(0, top_row)
            
    def validate_operation(self):
        expr = self.expression_input.toPlainText().strip()

        if not expr:
            return False, "La expresión no puede estar vacía. ¿Por qué no empezar con unos polinomios básicos?"
            
        try:
            self._parsed_expr = self.controller.parser.parse_expression(expr)
            return True, ""
        except ValueError as e:
            return False, str(e)

    def collect_polynomials(self):
        expr = self.expression_input.toPlainText().strip()

        if self.operation_type in {"raices", "derivacion", "integracion", "evaluacion"}:
            try:
                poly = self.controller.parser.to_polynomial(self._parsed_expr)
                return [poly] # Para operaciones de polinomios, se convierte a polinomio
            except Exception as e:
                raise ValueError(f"Error al convertir la expresión a polinomio: {str(e)}")
        else:
            return [expr]  # Para operaciones combinadas, se pasa la expresión en string

    def execute_operation(self):
        expr = self.expression_input.toPlainText().strip()
        valid, error_message = self.validate_operation()

        if not valid:
            raise ValueError(error_message)

        # Reusar self._parsed_expr en lugar de parsear de nuevo
        if self.operation_type == "evaluacion":
            x_value = self.x_input.value()
            poly = self.controller.parser.to_polynomial(self._parsed_expr)
            self.controller.manager.add_polynomial(poly)
            result = self.controller.execute_operation("evaluacion", float(x_value))
            return [("P1", result[0])]
        else:
            if self.operation_type in {"derivacion", "integracion", "raices"}:
                poly = self.controller.parser.to_polynomial(self._parsed_expr)
                self.controller.manager.add_polynomial(poly)
                result = self.controller.execute_operation(self.operation_type)
                return result
            else:
                result = self.controller.execute_operation(self.operation_type, expr)
                return result
            
    def get_evaluation_value(self):
        return str(self.x_input.value())

    def prepare_result_display(self, result):
        expression = self.expression_input.toPlainText().strip()

        if self.operation_type == "raices":
            _, roots = result[0]  # resultado tipo ('P1', [...])
            return format_math_expression(expression, roots, operation_type="roots")
        else:
            formatted_expr = format_math_expression(expression, result, operation_type="polynomial")  # Aquí se llama a la función
            return formatted_expr  # Mostrar el resultado completo
