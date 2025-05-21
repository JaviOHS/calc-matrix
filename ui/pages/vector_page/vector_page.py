from model.vector_manager import VectorManager
from controller.vector_controller import VectorController
from ui.pages.vector_page.vector_operation import VectorOpWidget
from ui.widgets.base_page import BasePage

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
        visible_key = next((k for k, v in self.operations.items() if v[0] == self.current_operation), None)
        if not visible_key:
            self.show_message_dialog("🔴 ERROR", "#f44336", "No se encontró una operación visible para la clave interna")
            return

        widget = self.operation_widgets.get(visible_key)
        if not widget:
            self.show_message_dialog("🔴 ERROR", "#f44336", "No se encontró el widget de la operación.")
            return
        
        widget.execute_operation()