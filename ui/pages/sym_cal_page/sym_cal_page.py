from ui.widgets.base_page_widget import BaseOperationPage
from model.sym_cal_manager import SymCalManager
from controller.sym_cal_controller import SymCalController
from ui.pages.sym_cal_page.sym_cal_op import SymCalOpWidget

class SymCalPage(BaseOperationPage):
    def __init__(self, manager: SymCalManager):
        controller = SymCalController(manager)

        operations = {
            "Derivadas": ("derivadas", SymCalOpWidget),
            "Integrales": ("integrales", SymCalOpWidget),
        }

        intro_text = (
            "Bienvenido a la sección de operaciones simbólicas\n\n"
            "Puedes resolver operaciones como derivadas e integrales.\n"
        )

        intro_image_path = "assets/images/intro/sym_cal.png"
        page_title = "Operaciones Simbólicas"
        super().__init__(manager, controller, operations, intro_text, intro_image_path, page_title)
        
    def execute_current_operation(self):
        pass

    def show_result(self, message, result):
        pass