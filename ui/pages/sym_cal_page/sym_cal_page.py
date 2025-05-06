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

        page_title = "Operaciones {Simbólicas}"
        intro_text = (
            "👋 Bienvenido a la sección de operaciones simbólicas\n\n"
            "📌 En esta sección podrás ingresar funciones y ecuaciones para resolver operaciones simbólicas.\n"
            "📌 Integrales, derivadas y ecuaciones diferenciales."
        )

        intro_image_path = "assets/images/intro/sym_cal.png"
        super().__init__(manager, controller, operations, intro_text, intro_image_path, page_title)
        
    def execute_current_operation(self):
        visible_key = next((k for k, v in self.operations.items() if v[0] == self.current_operation), None)
        if not visible_key:
            self.show_message_dialog("🔴 ERROR", f"No se encontró operación para clave '{self.current_operation}'")
            return

        widget = self.operation_widgets.get(visible_key)
        if not widget:
            self.show_message_dialog("🔴 ERROR", "No se encontró el widget de la operación.")
            return

        is_valid, error_msg = widget.validate_operation()
        if not is_valid:
            self.show_message_dialog("🟡 VALIDACIÓN", error_msg)
            return

        try:
            result = widget.execute_operation()
            html = widget.prepare_result_display(result)
            self.show_result(result, html)
        except ValueError as e:
            self.show_message_dialog("🔴 ERROR", str(e))
        except Exception as e:
            self.show_message_dialog("🔴 ERROR", f"Error inesperado: {str(e)}")

    def show_result(self, result, message):
        widget = self.operation_widgets.get(
            next((k for k, v in self.operations.items() if v[0] == self.current_operation), None)
        )
        
        if widget and hasattr(widget, "result_display"):
            widget.result_display.setText(message)
