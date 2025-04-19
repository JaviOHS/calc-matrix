import re
from model.polynomial_manager import PolynomialManager
from model.polynomial_model import Polynomial
from controller.polynomial_controller import PolynomialController
from ui.pages.base_page import BaseOperationPage
from ui.pages.poly_page.poly_operation import PolynomialOpcWidget
from PySide6.QtWidgets import QMessageBox

class PolynomialPage(BaseOperationPage):
    def __init__(self, manager: PolynomialManager):
        controller = PolynomialController(manager)

        operations = {
            "Operaciones Combinadas": ("operaciones_combinadas", PolynomialOpcWidget),
            "Raíces": ("raices", PolynomialOpcWidget),
            "Derivación": ("derivacion", PolynomialOpcWidget),
            "Integración": ("integracion", PolynomialOpcWidget),
            "Evaluación": ("evaluacion", PolynomialOpcWidget),
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
        super().prepare_operation(operation_key)
        # Obtener la clave interna y la clase del widget
        op_key, widget_class = self.operations[operation_key]
        self.current_operation = operation_key  # Usamos operation_key en lugar de op_key
        
        # Actualizar título
        self.title_label.setText(f"{self.page_title} - {operation_key}")
        
        # Crear el widget con los parámetros correctos
        try:
            widget = widget_class(self.manager, self.controller, op_key)
        except TypeError:
            widget = widget_class(self.manager, self.controller)
            
        widget.calculate_button.clicked.connect(self.execute_current_operation)
        widget.cancel_button.clicked.connect(self.reset_interface)

        # Almacenar el widget usando operation_key como clave
        self.operation_widgets[operation_key] = widget
        
        # Agregar y mostrar el widget
        self.stacked_widget.addWidget(widget)
        self.stacked_widget.setCurrentWidget(widget)

    def execute_current_operation(self):
        # Acceder al widget usando self.current_operation (que ahora es operation_key)
        widget = self.operation_widgets.get(self.current_operation)
        if not widget:
            QMessageBox.critical(self, "Error", "No se encontró el widget de la operación.")
            return

        is_valid, error_msg = widget.validate_operation()
        if not is_valid:
            QMessageBox.warning(self, "Validación", error_msg)
            return

        try:
            # Obtener la clave interna real para la operación
            op_key = self.operations[self.current_operation][0]
            
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

            self.show_result(result, f"{self.current_operation.replace('_', ' ').capitalize()} realizada correctamente")

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")

    def show_result(self, result, message):
        self.result_label.setText(message)
        self.result_preview_label.clear()

        def format_polynomial_html(text: str) -> str:
            formatted = text.replace(' ', '').replace('+', ' + ').replace('-', ' - ')
            formatted = formatted.replace('*', '·').replace('/', ' ÷ ').replace('**', '^')
            formatted = re.sub(r'\^(\d+)', r'<sup>\1</sup>', formatted)
            return f"<span style='font-family: Cambria Math; color: #ffffff;'>{formatted}</span>"

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