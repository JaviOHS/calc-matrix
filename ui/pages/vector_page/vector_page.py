import numpy as np
from model.vector_manager import VectorManager
from controller.vector_controller import VectorController
from ui.pages.vector_page.vector_operation import VectorOpWidget
from ui.widgets.base_page_widget import BaseOperationPage
from utils.formatting import format_math_expression

class VectorPage(BaseOperationPage):
    def __init__(self, manager: VectorManager):
        controller = VectorController(manager)

        operations = {
            "Operaciones Básicas": ("operaciones_basicas", VectorOpWidget),
            "Magnitud": ("magnitud", VectorOpWidget),
            "Producto punto": ("producto_punto", VectorOpWidget),
            "Producto cruzado": ("producto_cruzado", VectorOpWidget),
        }

        page_title = "Operaciones con {Vectores}"
        intro_text = (
            "👋 Bienvenido a la sección de operaciones con vectores.\n\n"
            "📌 Podrás realizar operaciones básicas con vectores, como: suma, resta, división por escalar).\n"
            "📌 Tambien podrás obtener la magnitud de un vector y realizar operaciones para hallar el producto de vectores.\n"
        )

        intro_image_path = "assets/images/intro/vector.png"
        super().__init__(manager, controller, operations, intro_text, intro_image_path, page_title)
        
    def execute_current_operation(self):
        # Encontrar la clave visible desde la clave interna
        visible_key = next((k for k, v in self.operations.items() if v[0] == self.current_operation), None)
        if not visible_key:
            self.show_message_dialog("🔴 ERROR", "#f44336", "No se encontró una operación visible para la clave interna")
            return

        widget = self.operation_widgets.get(visible_key)
        if not widget:
            self.show_message_dialog("🔴 ERROR", "#f44336", "No se encontró el widget de la operación.")
            return

        try:
            op_key = self.current_operation
            expression = widget.get_input_expression()
            
            if not expression:
                self.show_message_dialog("🟡 VALIDACIÓN", "#ffcc32", "Se necesita una expresión para evaluar")
                return

            result = self.controller.execute_operation(op_key, expression)
            self.show_result("Resultado", result)

        except ValueError as e:
            self.show_message_dialog("🔴 ERROR", "#f44336", str(e))
        except Exception as e:
            self.show_message_dialog("🔴 ERROR", "#f44336", f"Error inesperado: {str(e)}")

    def show_result(self, message, result):
        try:
            visible_key = next((k for k, v in self.operations.items() if v[0] == self.current_operation), None)
            if not visible_key:
                return

            widget = self.operation_widgets.get(visible_key)
            if not widget:
                return
            formatted_html = format_math_expression(widget.get_input_expression(), result, "vector")
            widget.result_display.setText(formatted_html)

        except Exception as e:
            print(f"Error showing result: {str(e)}")
