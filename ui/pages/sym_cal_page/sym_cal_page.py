from ui.widgets.base_page import BasePage
from model.sym_cal_manager import SymCalManager
from controller.sym_cal_controller import SymCalController
from ui.pages.sym_cal_page.operations.integral_op import IntegralOperation
from ui.pages.sym_cal_page.operations.derivative_op import DerivativeOperation
from ui.pages.sym_cal_page.operations.edo_op import DifferentialEqOperation

class SymCalPage(BasePage):
    def __init__(self, navigate_callback=None, manager=SymCalManager()):
        self.controller = SymCalController(manager)
        
        super().__init__(navigate_callback, page_key="sym_cal", controller=self.controller, manager=manager)

        self.operations = {
            "Derivación": ("derivative", DerivativeOperation),
            "Integración": ("integral", IntegralOperation),
            "Ecuaciones Diferenciales": ("differential_equation", DifferentialEqOperation),
        }

    def execute_current_operation(self):
        visible_key = next((k for k, v in self.operations.items() if v[0] == self.current_operation), None)
        if not visible_key:
            self.show_message_dialog("🔴 ERROR", "#f44336", f"No se encontró operación para clave '{self.current_operation}'")
            return

        widget = self.operation_widgets.get(visible_key)
        if not widget:
            self.show_message_dialog("🔴 ERROR", "#f44336", "No se encontró el widget de la operación.")
            return
        
        # Capturar el resultado y posible error del widget
        success, message = widget.on_calculate_clicked()
        if not success:
            # Mostrar mensaje de error en un diálogo
            self.show_message_dialog("🔴 ERROR", "#f44336", message)
    
    def show_result(self, result, message):
        widget = self.operation_widgets.get(
            next((k for k, v in self.operations.items() if v[0] == self.current_operation), None)
        )
        
        if widget and hasattr(widget, "result_display"):
            widget.result_display.setText(message)
