from model.vector_manager import VectorManager
from controller.vector_controller import VectorController
from ui.pages.vector_page.vector_operation import VectorOpWidget
from ui.widgets.base_page import BasePage
from utils.formating.formatting import format_math_expression

class VectorPage(BasePage):
    def __init__(self, navigate_callback=None, manager=VectorManager()):
        self.controller = VectorController(manager)

        super().__init__(navigate_callback, page_key="vector", controller=self.controller, manager=manager)

        self.operations = {
            "Operaciones Básicas": ("basic_operations", VectorOpWidget),
            "Magnitud": ("magnitude", VectorOpWidget),
            "Producto punto": ("dot_product", VectorOpWidget),
            "Producto cruzado": ("cross_product", VectorOpWidget),
        }

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
