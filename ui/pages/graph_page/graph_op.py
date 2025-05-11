from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QVBoxLayout, QWidget
from ui.widgets.expression_op_widget import ExpressionOpWidget
from controller.graph_controller import GraphController
from utils.spinbox_utils import create_spinbox

class BaseGraphWidget(ExpressionOpWidget):
    """Widget base para visualización de gráficas"""
    def __init__(self, manager, controller, operation_type, input_label, placeholder):
        super().__init__(manager, controller, operation_type, placeholder=placeholder, input_label=input_label, use_dialog_for_result=True)
        self.canvas = None
        self.calculate_button.setText("Graficar")
    
    def create_range_row(self, label_text, min_control, max_control, default_min=-10.0, default_max=10.0):
        """Crea una fila de controles para un rango (min/max)"""
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        # Label Min
        label_from = QLabel(f"Desde {label_text}:")
        label_from.setFixedWidth(70)
        layout.addWidget(label_from)
        
        # Spinbox Min
        min_control.setValue(default_min)
        layout.addWidget(min_control)
        
        # Label Max
        label_to = QLabel(f"Hasta {label_text}:")
        label_to.setFixedWidth(70)
        layout.addWidget(label_to)
        
        # Spinbox Max
        max_control.setValue(default_max)
        layout.addWidget(max_control)
        
        layout.addStretch()
        return layout
    
    def display_result(self, result):
        if self.use_dialog_for_result and hasattr(result, 'draw'):
            self.show_canvas_dialog(result)
        else:
            self.result_display.setText(str(result))

    def clear_result(self):
        if self.canvas:
            self.result_container.layout().removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None
    
    def cleanup(self):
        self.clear_result()
        super().cleanup()

class Graph2DWidget(BaseGraphWidget):
    def __init__(self, manager=GraphController, controller=GraphController, operation_type=None):
        input_label = "Ingrese una función para realizar una gráfica en 2D:"
        placeholder = "Puede ingresar varias funciones separadas por comas. Ejemplo: x^2, x^3, x^4"
        super().__init__(manager, controller, operation_type, input_label, placeholder)
        self.add_range_inputs()

    def add_range_inputs(self):
        self.range_widget = QWidget()
        range_layout = QVBoxLayout(self.range_widget)
        range_layout.setContentsMargins(20, 0, 0, 0)
        
        # Crear controles usando la función de utilidad
        self.x_min = create_spinbox(default_val=-10.0)
        self.x_max = create_spinbox(default_val=10.0)
        
        # Armar la fila de rango X
        x_row = self.create_range_row("x", self.x_min, self.x_max)
        range_layout.addLayout(x_row)
        
        self.layout.insertWidget(2, self.range_widget)

    def get_inputs(self):
        return {
            "expression": self.get_input_expression(),
            "x_range": (self.x_min.value(), self.x_max.value())
        }

    def validate_operation(self):
        expressions = self.get_input_expression()
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
            result = self.controller.execute_operation("graficas_2d", self.get_inputs())
            return True, result
        except Exception as e:
            return False, str(e)

    def on_calculate_clicked(self):
        success, result = self.perform_operation()
        if success:
            self.display_result(result)
        else:
            print("Error:", result)

class Graph3DWidget(BaseGraphWidget):
    def __init__(self, manager=GraphController, controller=GraphController, operation_type=None):
        input_label = "Ingrese una función para realizar una gráfica en 3D:"
        placeholder = "Ejemplo: x^2 + y^2"
        super().__init__(manager, controller, operation_type, input_label, placeholder)
        self.add_range_inputs()

    def add_range_inputs(self):
        self.range_widget = QWidget()
        main_layout = QVBoxLayout(self.range_widget)
        main_layout.setContentsMargins(20, 0, 0, 0)
        main_layout.setSpacing(10)

        # Crear controles
        self.x_min = create_spinbox(default_val=-10.0)
        self.x_max = create_spinbox(default_val=10.0)
        self.y_min = create_spinbox(default_val=-10.0)
        self.y_max = create_spinbox(default_val=10.0)
        
        # Armar la fila de rango X
        x_row = self.create_range_row("x", self.x_min, self.x_max)
        main_layout.addLayout(x_row)
        
        # Armar la fila de rango Y
        y_row = self.create_range_row("y", self.y_min, self.y_max)
        main_layout.addLayout(y_row)
        
        self.layout.insertWidget(2, self.range_widget)

    def get_inputs(self):
        return {
            "expression": self.get_input_expression(),
            "x_range": (self.x_min.value(), self.x_max.value()),
            "y_range": (self.y_min.value(), self.y_max.value())
        }

    def validate_operation(self):
        expr = self.get_input_expression()
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
            result = self.controller.execute_operation("graficas_3d", self.get_inputs())
            return True, result
        except Exception as e:
            return False, str(e)

    def on_calculate_clicked(self):
        success, result = self.perform_operation()
        if success:
            self.display_result(result)
        else:
            print("Error:", result)
