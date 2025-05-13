from ui.widgets.base_page import BasePage
from controller.graph_controller import GraphController
from model.graph_manager import GraphManager
from ui.pages.graph_page.graph_op import Graph2DWidget, Graph3DWidget

class GraphPage(BasePage):
    def __init__(self, navigate_callback=None, manager=GraphManager()):
        self.controller = GraphController(manager)

        super().__init__(navigate_callback, page_key="graph", controller=self.controller, manager=manager)

        self.operations = {
            "Gráficas 2D": ("graficas_2d", Graph2DWidget),
            "Gráficas 3D": ("graficas_3d", Graph3DWidget),
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
            inputs = widget.get_inputs()

            if not inputs.get("expression"):
                self.show_message_dialog("🟡 VALIDACIÓN", "#ffcc32", "Se necesita una expresión para evaluar.")
                return

            result = self.controller.execute_operation(op_key, inputs)
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

            widget.display_result(result)
        except Exception as e:
            self.show_message_dialog("🔴 ERROR", "#f44336", f"Error inesperado: {str(e)}")
