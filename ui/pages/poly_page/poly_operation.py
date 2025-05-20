from ui.widgets.expression_op_widget import ExpressionOpWidget
from model.polynomial_manager import PolynomialManager
from controller.polynomial_controller import PolynomialController
from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout
from utils.formating.formatting import format_math_expression
from utils.components.spinbox_utils import create_float_spinbox
from utils.components.two_column import TwoColumnWidget

class PolynomialOpWidget(ExpressionOpWidget):
    def __init__(self, manager=PolynomialManager, controller=PolynomialController, operation_type=None):
        input_label = "Ingrese expresión"
        if operation_type == "combined_operations":
            placeholder = "Ejemplo: (x^2 + 2x + 1) + (4x^2 + 3x + 4)"
        else:
            placeholder = "Ejemplo: x^2 + 2x + 1"

        super().__init__(manager, controller, operation_type, placeholder=placeholder, input_label=input_label)
        self.custom_setup()
        self.input_mode = "text"
        self.last_valid_text = ""
        self._parsed_expr = None 

    def custom_setup(self):
        # Ocultar el título si existe
        self.title_label.hide()
        result_container = self.detach_result_container()

        # Crear widget de dos columnas
        two_column_widget = TwoColumnWidget(
            column1_label=self.input_label_text,
            column2_label="Resultado",
        )
        two_column_widget.add_to_column1(self.expression_input)

        # Añadir el contenedor de resultado a la segunda columna
        two_column_widget.add_to_column2(result_container)

        # Insertar el widget de dos columnas en el layout principal
        self.layout.insertWidget(1, two_column_widget)

        # Configurar el spinbox si es necesario
        if self.operation_type == "evaluation":
            self.x_input = create_float_spinbox(min_val=-1000, max_val=1000, step=0.1)

            x_label = QLabel("📍 Valor de x:")

            layout = QHBoxLayout()
            layout.addWidget(x_label)
            layout.addWidget(self.x_input)
            layout.addStretch()

            # Añadir el spinbox al diseño de la primera columna
            container_widget = QWidget()
            container_widget.setLayout(layout)
            two_column_widget.add_to_column1(container_widget)

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

        if self.operation_type in {"roots", "derivative", "integral", "evaluation"}:
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
        if self.operation_type == "evaluation":
            x_value = self.x_input.value()
            poly = self.controller.parser.to_polynomial(self._parsed_expr)
            self.controller.manager.add_polynomial(poly)
            result = self.controller.execute_operation("evaluation", float(x_value))
            return [("P1", result[0])]
        else:
            if self.operation_type in {"derivative", "integral", "roots"}:
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

        if self.operation_type == "roots":
            _, roots = result[0]  # resultado tipo ('P1', [...])
            return format_math_expression(expression, roots, operation_type="roots")
        elif self.operation_type == "evaluation":
            return format_math_expression(expression, result, operation_type="evaluation")
        else:
            formatted_expr = format_math_expression(expression, result, operation_type="polynomial")  # Aquí se llama a la función
            return formatted_expr  # Mostrar el resultado completo
