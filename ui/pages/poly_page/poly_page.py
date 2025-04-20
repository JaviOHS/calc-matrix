from model.polynomial_manager import PolynomialManager
from model.polynomial_model import Polynomial
from controller.polynomial_controller import PolynomialController
from ui.pages.base_page import BaseOperationPage
from ui.pages.poly_page.poly_operation import PolynomialOpWidget
from PySide6.QtWidgets import QMessageBox
from utils.formatting import format_polynomial_html

class PolynomialPage(BaseOperationPage):
    def __init__(self, manager: PolynomialManager):
        controller = PolynomialController(manager)

        operations = {
            "Operaciones Combinadas": ("operaciones_combinadas", PolynomialOpWidget),
            "Raíces": ("raices", PolynomialOpWidget),
            "Derivación": ("derivacion", PolynomialOpWidget),
            "Integración": ("integracion", PolynomialOpWidget),
            "Evaluación": ("evaluacion", PolynomialOpWidget),
        }

        intro_text = (
            "Bienvenido a la sección de operaciones con polinomios.\n\n"
            "Puedes realizar operaciones combinadas (suma, resta, multiplicación, división),\n"
            "obtener raíces, derivadas, integrales y evaluación de polinomios.\n"
        )

        intro_image_path = "assets/images/polynomial_intro.png"
        page_title = "Operaciones con Polinomios"

        super().__init__(manager, controller, operations, intro_text, intro_image_path, page_title)

    def prepare_operation(self, operation_key):
        op_key, widget_class = self.operations[operation_key]
        self.current_operation = op_key
        super().prepare_operation(operation_key)
        self.title_label.setText(f"{self.page_title} - {operation_key}")

    def execute_current_operation(self):
        # Encontrar la clave visible desde la clave interna
        visible_key = next((k for k, v in self.operations.items() if v[0] == self.current_operation), None)
        if not visible_key:
            QMessageBox.critical(self, "Error", f"No se encontró una operación visible para la clave interna '{self.current_operation}'")
            return

        widget = self.operation_widgets.get(visible_key)
        if not widget:
            QMessageBox.critical(self, "Error", "No se encontró el widget de la operación.")
            return

        is_valid, error_msg = widget.validate_operation()
        if not is_valid:
            QMessageBox.warning(self, "Validación", error_msg)
            return

        try:
            op_key = self.current_operation

            if op_key == "operaciones_combinadas":
                expression = widget.collect_polynomials()[0]
                if not expression:
                    QMessageBox.warning(self, "Validación", "Se necesita una expresión para evaluar")
                    return
                result = self.controller.execute_operation(op_key, expression)

            elif op_key == "evaluacion":
                x_value = widget.get_evaluation_value()
                if x_value is None or x_value.strip() == "":
                    QMessageBox.warning(self, "Validación", "Se necesita un valor x para evaluar los polinomios")
                    return
                try:
                    x_value = float(x_value)
                except ValueError:
                    QMessageBox.warning(self, "Validación", "El valor de x no es válido")
                    return
                
                polynomials = widget.collect_polynomials()
                if not polynomials:
                    QMessageBox.warning(self, "Validación", "No hay polinomios para evaluar")
                    return

                self.manager.polynomials.clear()
                for poly in polynomials:
                    self.manager.add_polynomial(poly)
                result = self.controller.execute_operation(op_key, x_value)

            else:
                polynomials = widget.collect_polynomials()
                if not polynomials:
                    QMessageBox.warning(self, "Validación", "No hay polinomios para operar")
                    return

                self.manager.polynomials.clear()
                for poly in polynomials:
                    self.manager.add_polynomial(poly)
                result = self.controller.execute_operation(op_key)

            widget.show_result(result)

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")

    def show_result(self, result, message):
        self.result_label.setText(message)
        self.result_preview_label.clear()

        if isinstance(result, tuple) and all(isinstance(r, Polynomial) for r in result):
            quotient, remainder = result
            formatted_html = (
                f"Cociente: {format_polynomial_html(str(quotient))}<br>"
                f"Residuo: {format_polynomial_html(str(remainder))}"
            )
        elif isinstance(result, list) and all(isinstance(p, Polynomial) for p in result):
            formatted_html = "<br>".join(
                f"P{i+1}: {format_polynomial_html(str(p))}" for i, p in enumerate(result)
            )
        elif isinstance(result, list):  # Evaluación o raíces
            formatted_html = "<br>".join(
                f"{label}: {format_polynomial_html(str(value))}" for label, value in result
            )
        else:
            formatted_html = format_polynomial_html(str(result))

        self.result_preview_label.setText(formatted_html)
        self.stacked_widget.addWidget(self.result_widget)
        self.stacked_widget.setCurrentWidget(self.result_widget)