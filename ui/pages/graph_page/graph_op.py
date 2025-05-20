from PySide6.QtWidgets import QVBoxLayout, QVBoxLayout, QWidget
from ui.widgets.expression_op_widget import ExpressionOpWidget
from controller.graph_controller import GraphController
from utils.components.spinbox_utils import create_float_spinbox
from utils.layout.create_range_row import create_range_row as create_range_layout

class BaseGraphWidget(ExpressionOpWidget):
    """Widget base para visualización de gráficas"""
    def __init__(self, manager, controller, operation_type, input_label, placeholder):
        super().__init__(manager, controller, operation_type, placeholder=placeholder, input_label=input_label, use_dialog_for_result=True)
        self.canvas = None
        self.calculate_button.setText("Graficar")
    
    def create_range_row(self, label_text, min_control, max_control, default_min=-10.0, default_max=10.0):
        """Crea una fila de controles para un rango (min/max) unidos"""
        layout, _, _ = create_range_layout(
            label_text=f"📌 {label_text}", 
            min_label="", 
            max_label="", 
            default_min=default_min, 
            default_max=default_max,
            min_control=min_control,
            max_control=max_control,
            label_width=100,
            spacing=2
        )
        return layout
    
    def display_result(self, result):
        """Procesa el resultado para mostrarlo en diálogo o directamente"""
        if hasattr(result, 'draw'):
            try:
                self.process_operation_result(result)
            except Exception as e:
                error_message = f"<div style='color: #D32F2F;'>❌ Error mostrando gráfica: {str(e)}</div>"
                self.process_operation_result(error_message)
        else:
            super().display_result(result)

    def clear_result(self):
        if self.canvas:
            self.result_container.layout().removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None
    
    def cleanup(self):
        self.clear_result()
        super().cleanup()

class Graph2DWidget(BaseGraphWidget):
    def __init__(self, manager=GraphController, controller=GraphController, operation_type="2d_graph"):
        input_label = "Ingrese los rangos y la función a graficar en 2D."
        placeholder = "Puede ingresar varias funciones separadas por comas. Ejemplo: x^2, x^3, x^4"
        super().__init__(manager, controller, operation_type, input_label, placeholder)
        self.add_inputs()

    def add_inputs(self):
        self.range_widget = QWidget()
        range_layout = QVBoxLayout(self.range_widget)
        range_layout.setContentsMargins(20, 0, 0, 0)
        
        self.x_min = create_float_spinbox(default_val=-10.0)
        self.x_max = create_float_spinbox(default_val=10.0)
        
        x_row = self.create_range_row("Rango x", self.x_min, self.x_max)
        self.input_layout.insertLayout(2, x_row)
        self.layout.insertWidget(2, self.range_widget)

    def get_inputs(self):
        return {"expression": self.expression_input.toPlainText(),"x_range": (self.x_min.value(), self.x_max.value())}

    def validate_operation(self):
        expressions = self.expression_input.toPlainText()
        try:
            if not expressions:
                raise ValueError("Debe ingresar al menos una función.")
            if len(expressions.split(',')) > 5:
                raise ValueError("Máximo 5 funciones permitidas.")
            return True, ""
        except ValueError as e:
            return False, str(e)

    def perform_operation(self):
        valid, msg = self.validate_operation()
        try:
            if not valid:
                raise ValueError(msg)
            result = self.controller.execute_operation("2d_graph", self.get_inputs())
            return True, result
        except Exception as e:
            return False, str(e)

    def on_calculate_clicked(self):
        success, result = self.perform_operation()
        if success:
            self.process_operation_result(result)
        else:
            error_message = f"<div style='color: #D32F2F;'>❌ Error: {result}</div>"
            self.process_operation_result(error_message)

class Graph3DWidget(BaseGraphWidget):
    def __init__(self, manager=GraphController, controller=GraphController, operation_type="3d_graph"):
        input_label = "Ingrese los rangos y la función a graficar en 3D."
        placeholder = "Ejemplo: x^2 + y^2"
        super().__init__(manager, controller, operation_type, input_label, placeholder)
        self.add_inputs()

    def add_inputs(self):
        self.range_widget = QWidget()
        main_layout = QVBoxLayout(self.range_widget)
        main_layout.setContentsMargins(20, 0, 0, 0)
        main_layout.setSpacing(4)

        self.x_min = create_float_spinbox(default_val=-10.0)
        self.x_max = create_float_spinbox(default_val=10.0)
        self.y_min = create_float_spinbox(default_val=-10.0)
        self.y_max = create_float_spinbox(default_val=10.0)
        
        x_row = self.create_range_row("Rango x", self.x_min, self.x_max)
        self.input_layout.insertLayout(2, x_row)
        
        y_row = self.create_range_row("Rango y", self.y_min, self.y_max)
        self.input_layout.insertLayout(2, y_row)
        
        self.layout.insertWidget(2, self.range_widget)

    def get_inputs(self):
        return {"expression": self.expression_input.toPlainText(),"x_range": (self.x_min.value(), self.x_max.value()),"y_range": (self.y_min.value(), self.y_max.value())}

    def validate_operation(self):
        expr = self.expression_input.toPlainText()
        try:
            if not expr:
                raise ValueError("La expresión no puede estar vacía.")
            return True, ""
        except ValueError as e:
            return False, str(e)

    def perform_operation(self):
        valid, msg = self.validate_operation()
        try:
            if not valid:
                raise ValueError(msg)
            result = self.controller.execute_operation("3d_graph", self.get_inputs())
            return True, result
        except Exception as e:
            return False, str(e)

    def on_calculate_clicked(self):
        success, result = self.perform_operation()
        if success:
            self.process_operation_result(result)
        else:
            error_message = f"<div style='color: #D32F2F;'>❌ Error: {result}</div>"
            self.process_operation_result(error_message)
