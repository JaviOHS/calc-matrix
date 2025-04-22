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

        intro_text = (
            "Bienvenido a la sección de gráfica de funciones.\n\n"
            "Aquí podrás visualizar gráficas en 2 y en 3 dimensiones\n"
        )

        intro_image_path = "assets/images/intro/graph.png"
        page_title = "Creación de Gráficas"
        super().__init__(manager, controller, operations, intro_text, intro_image_path, page_title)
        
    def prepare_operation(self, operation_key):
        op_key, widget_class = self.operations[operation_key]
        self.current_operation = op_key
        super().prepare_operation(operation_key)
        self.title_label.setText(f"{self.page_title} - {operation_key}")

    def execute_current_operation(self):
        widget = self.operation_widgets.get(self.current_operation)
        if not widget:
            return

        inputs = widget.get_inputs()
        self.manager.set_inputs(self.current_operation, inputs)

        # Verificar si es operación 2D o 3D
        if self.current_operation == "graficas_2d":
            canvas = self.controller.generate_canvas_2d(inputs)
        else:
            return
            
        widget.display_result(canvas)

    def show_result(self, message, result):
        pass