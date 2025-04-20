import numpy as np
from model.vector_manager import VectorManager
from controller.vector_controller import VectorController
from ui.pages.vector_page.vector_operation import VectorOpWidget
from ui.pages.base_page import BaseOperationPage

class VectorPage(BaseOperationPage):
    def __init__(self, manager: VectorManager):
        controller = VectorController(manager)

        operations = {
            "Operaciones Básicas": ("operaciones_basicas", VectorOpWidget),
            "Magnitud": ("magnitud", VectorOpWidget),
            "Producto punto": ("producto_punto", VectorOpWidget),
            "Producto cruzado": ("producto_cruzado", VectorOpWidget),
        }

        intro_text = (
            "Bienvenido a la sección de operaciones con vectores.\n\n"
            "Puedes realizar operaciones básicas (suma, resta, división, división por escalar),\n"
            "obtener magnitud y operaciones para hallar el producto de vectores.\n"
        )

        intro_image_path = "assets/images/vector_intro.png"
        page_title = "Operaciones con Vectores"
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
            self.show_result("Error", "No se encontró una operación visible para la clave interna")
            return

        widget = self.operation_widgets.get(visible_key)
        if not widget:
            self.show_result("Error", "No se encontró el widget de la operación.")
            return

        try:
            op_key = self.current_operation
            expression = widget.get_input_expression()
            
            if not expression:
                self.show_result("Validación", "Se necesita una expresión para evaluar")
                return

            result = self.controller.execute_operation(op_key, expression)
            self.show_result("Resultado", result)

        except ValueError as e:
            self.show_result("Error", str(e))
        except Exception as e:
            self.show_result("Error", f"Error inesperado: {str(e)}")

    def show_result(self, message, result):
        try:
            # Obtener el widget actual
            visible_key = next((k for k, v in self.operations.items() if v[0] == self.current_operation), None)
            if not visible_key:
                return

            widget = self.operation_widgets.get(visible_key)
            if not widget:
                return

            # Formatear el resultado
            if isinstance(result, (list, np.ndarray)):
                content = f"[{', '.join(f'{x:.4f}' for x in result)}]"
            else:
                content = str(result)

            # Mostrar en el widget de operación
            widget.result_display.setText(
                f"<div style='font-family: Dosis; color: #aaa;'>Resultado:</div>"
                f"<div style='font-family: Cambria Math;'>{content}</div>"
            )

        except Exception as e:
            print(f"Error showing result: {str(e)}")
