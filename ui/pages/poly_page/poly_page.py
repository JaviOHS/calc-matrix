from model.polynomial_manager import PolynomialManager
from controller.polynomial_controller import PolynomialController
from ui.widgets.base_page import BasePage
from ui.pages.poly_page.poly_operation import PolynomialOpWidget

class PolynomialPage(BasePage):
    def __init__(self, navigate_callback=None, manager=PolynomialManager()):
        self.controller = PolynomialController(manager)

        super().__init__(navigate_callback, page_key="polynomial", controller=self.controller, manager=manager)

        self.operations = {
            "Operaciones Combinadas": ("combined_operations", PolynomialOpWidget),
            "Raíces": ("roots", PolynomialOpWidget),
            "Derivación": ("derivative", PolynomialOpWidget),
            "Integración": ("integral", PolynomialOpWidget),
            "Evaluación": ("evaluation", PolynomialOpWidget),
        }
        
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
        
        widget.execute_operation()
