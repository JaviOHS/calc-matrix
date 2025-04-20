from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from ui.pages.base_page import BaseOperationPage
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

        intro_image_path = "assets/images/sym_cal_intro.png"
        page_title = "Operaciones Simbólicas"
        super().__init__(manager, controller, operations, intro_text, intro_image_path, page_title)
        
    def prepare_operation(self, operation_key):
        op_key, widget_class = self.operations[operation_key]
        self.current_operation = op_key
        super().prepare_operation(operation_key)
        self.title_label.setText(f"{self.page_title} - {operation_key}")

    def execute_current_operation(self):
        pass

    def show_result(self, message, result):
        pass