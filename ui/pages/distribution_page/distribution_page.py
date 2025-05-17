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
        }