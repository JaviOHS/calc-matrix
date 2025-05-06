from model.polynomial_manager import PolynomialManager
from controller.polynomial_controller import PolynomialController
from ui.widgets.base_page_widget import BaseOperationPage
from ui.pages.poly_page.poly_operation import PolynomialOpWidget

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

        page_title = "Operaciones con {Polinomios}"
        intro_text = (
            "👋 Bienvenido a la sección de operaciones con polinomios.\n\n"
            "📌 En esta sección podrás realizar operaciones combinadas con polinomios.\n"
            "📌 Tambien podrás calcular raíces, derivadas, integrales y evaluar polinomios.\n"
        )

        intro_image_path = "assets/images/intro/polynomial.png"

        super().__init__(manager, controller, operations, intro_text, intro_image_path, page_title)

    def execute_current_operation(self):
        # Encontrar la clave visible desde la clave interna
        visible_key = next((k for k, v in self.operations.items() if v[0] == self.current_operation), None)
        if not visible_key:
            self.show_message_dialog("🔴 ERROR", "#f44336", f"No se encontró una operación visible para la clave interna '{self.current_operation}'")
            return

        widget = self.operation_widgets.get(visible_key)
        if not widget:
            self.show_message_dialog("🔴 ERROR", "#f44336", "No se encontró el widget de la operación.")
            return

        is_valid, error_msg = widget.validate_operation()
        if not is_valid:
            self.show_message_dialog("🟡 VALIDACIÓN", "#ffcc32", error_msg)
            return

        try:
            op_key = self.current_operation

            if op_key == "operaciones_combinadas":
                expression = widget.collect_polynomials()[0]
                if not expression:
                    self.show_message_dialog("🟡 VALIDACIÓN", "#ffcc32", "Se necesita una expresión para evaluar")
                    return
                result = self.controller.execute_operation(op_key, expression)

            elif op_key == "evaluacion":
                x_value = widget.get_evaluation_value()
                if x_value is None or x_value.strip() == "":
                    self.show_message_dialog("🟡 VALIDACIÓN", "#ffcc32", "Se necesita un valor x para evaluar los polinomios")
                    return
                try:
                    x_value = float(x_value)
                except ValueError:
                    self.show_message_dialog("🟡 VALIDACIÓN", "#ffcc32", "El valor de x no es válido")
                    return
                
                polynomials = widget.collect_polynomials()
                if not polynomials:
                    self.show_message_dialog("🟡 ADVERTENCIA", "#ffcc32", "No hay polinomios para evaluar")
                    return

                self.manager.polynomials.clear()
                for poly in polynomials:
                    self.manager.add_polynomial(poly)
                result = self.controller.execute_operation(op_key, x_value)

            else:
                polynomials = widget.collect_polynomials()
                if not polynomials:
                    self.show_message_dialog("🟡 ADVERTENCIA", "#ffcc32", "No hay polinomios para operar.")
                    return

                self.manager.polynomials.clear()
                for poly in polynomials:
                    self.manager.add_polynomial(poly)
                result = self.controller.execute_operation(op_key)

            html = widget.prepare_result_display(result)
            self.show_result(result, html)

        except ValueError as e:
            self.show_message_dialog("🔴 ERROR", "#f44336", str(e))
        except Exception as e:
            self.show_message_dialog("🔴 ERROR", "#f44336", f"Error inesperado: {str(e)}")

    def show_result(self, result, message):
        widget = self.operation_widgets.get(
            next((k for k, v in self.operations.items() if v[0] == self.current_operation), None)
        )
        
        if widget and hasattr(widget, "result_display"):
            widget.result_display.setText(message)
            