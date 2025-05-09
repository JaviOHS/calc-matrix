from ui.widgets.base_page_widget import BaseOperationPage
from controller.graph_controller import GraphController
from model.graph_manager import GraphManager
from ui.pages.graph_page.graph_op import Graph2DWidget, Graph3DWidget

class GraphPage(BaseOperationPage):
    def __init__(self, manager: GraphManager):
        controller = GraphController(manager)

        operations = {
            "Gráficas 2D": ("graficas_2d", Graph2DWidget),
            "Gráficas 3D": ("graficas_3d", Graph3DWidget),
        }

        page_title = "Gráficas de {Funciones}"
        intro_text = (
            "👋 Bienvenido a la sección de gráfica de funciones.\n\n"
            "📌 Esta sección es útil para visualizar funciones y entender su comportamiento.\n"
            "📌 Puedes ingresar funciones matemáticas y ver sus gráficas en diferentes dimensiones\n"
        )

        intro_image_path = "assets/images/intro/graph.png"
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
