from ui.widgets.expression_op_widget import ExpressionOpWidget
from model.polynomial_manager import PolynomialManager
from controller.polynomial_controller import PolynomialController
from utils.formating.formatting import format_math_expression
from utils.components.spinbox_utils import create_float_spinbox
from utils.components.two_column import TwoColumnWidget
from utils.formating.messages import format_warning, format_error

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
        two_column_widget.add_to_column2(result_container)
        self.layout.insertWidget(1, two_column_widget)

        # Configurar el spinbox si es necesario
        if self.operation_type == "evaluation":
            x_input_container = create_float_spinbox(min_val=-1000, max_val=1000, step=0.1, label_text="📍 Valor de x:")
            self.x_input = x_input_container.spinbox
            two_column_widget.add_to_column1(x_input_container)

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
        try:
            expr = self.expression_input.toPlainText().strip()
            valid, error_message = self.validate_operation()

            if not valid:
                self.display_result(format_warning(error_message))
                return

            # Lógica específica según el tipo de operación
            if self.operation_type == "evaluation":
                x_value = self.x_input.value()
                poly = self.controller.parser.to_polynomial(self._parsed_expr)
                self.controller.manager.add_polynomial(poly)
                result = self.controller.execute_operation("evaluation", float(x_value))
                formatted_result = self.prepare_result_display([("P1", result[0])])
            else:
                if self.operation_type in {"derivative", "integral", "roots"}:
                    poly = self.controller.parser.to_polynomial(self._parsed_expr)
                    self.controller.manager.add_polynomial(poly)
                    result = self.controller.execute_operation(self.operation_type)
                else:
                    result = self.controller.execute_operation(self.operation_type, expr)
                
                formatted_result = self.prepare_result_display(result)
            
            self.display_result(formatted_result)
            return result  # Opcional: devolver el resultado por si es necesario

        except ValueError as e:
            self.display_result(format_error(str(e)))
        except Exception as e:
            self.display_result(format_error(str(e)))
            import traceback
            print(traceback.format_exc())

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
