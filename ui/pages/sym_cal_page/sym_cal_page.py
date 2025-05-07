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
            "Ecuaciones Diferenciales": ("ecuaciones_diferenciales", SymCalOpWidget),
        }

        page_title = "Cálculo Simbólico de {Funciones}"
        intro_text = (
            "👋 Bienvenido a la sección de operaciones simbólicas.\n\n"
            "📌 En esta sección podrás ingresar funciones y ecuaciones para resolver operaciones simbólicas.\n"
            "📌 Desde integrales y derivadas, hasta ecuaciones diferenciales."
        )

        intro_image_path = "assets/images/intro/sym_cal.png"
        super().__init__(manager, controller, operations, intro_text, intro_image_path, page_title)
        
    def execute_current_operation(self):
        visible_key = next((k for k, v in self.operations.items() if v[0] == self.current_operation), None)
        if not visible_key:
            self.show_message_dialog("🔴 ERROR", "#f44336", f"No se encontró operación para clave '{self.current_operation}'")
            return

        widget = self.operation_widgets.get(visible_key)
        if not widget:
            self.show_message_dialog("🔴 ERROR", "#f44336", "No se encontró el widget de la operación.")
            return

        is_valid, error_msg = widget.validate_operation()
        if not is_valid:
            self.show_message_dialog("🟡 VALIDACIÓN", "#ffcc32", error_msg)
            return

        try:
            result = widget.execute_operation()
            html = widget.prepare_result_display(result)
            
            # Asegúrate de que el widget tenga un QLabel para mostrar resultados
            if hasattr(widget, 'result_display'):
                widget.result_display.setText(html)
                widget.result_display.show()
            else:
                self.show_message_dialog("🔴 ERROR", "#f44336", "El widget no tiene un área de visualización de resultados.")
                
        except ValueError as e:
            self.show_message_dialog("🔴 ERROR", "#f44336", str(e))
        except Exception as e:
            self.show_message_dialog("🔴 ERROR", "#f44336", f"Error inesperado: {str(e)}")

    def show_result(self, result, message):
        widget = self.operation_widgets.get(
            next((k for k, v in self.operations.items() if v[0] == self.current_operation), None)
        )
        
        if widget and hasattr(widget, "result_display"):
            widget.result_display.setText(message)
