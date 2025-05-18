from ui.widgets.base_page import BasePage
from model.distribution_manager import DistributionManager
from controller.distribution_controller import DistributionController
from ui.pages.distribution_page.distribution_op import DistributionOpWidget

class DistributionPage(BasePage):
    def __init__(self, navigate_callback=None, manager=DistributionManager()):
        self.controller = DistributionController(manager)
        
        super().__init__(navigate_callback, page_key="distribution", controller=self.controller, manager=manager)


        self.operations = {
            "Simulación de Números Aleatorios": ("distribucion", DistributionOpWidget),
            "Simulación de Monte Carlo": ("monte_carlo", DistributionOpWidget),
            "Propagación de Epidemias - Markov": ("markov_epidemic", DistributionOpWidget),
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
            self.show_message_dialog("🔴 ERROR", "#f44336", message)