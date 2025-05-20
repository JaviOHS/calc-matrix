from PySide6.QtWidgets import QVBoxLayout, QVBoxLayout, QWidget
from ui.widgets.expression_op_widget import ExpressionOpWidget
from controller.graph_controller import GraphController
from utils.components.spinbox_utils import create_float_spinbox
from utils.layout.create_range_row import create_range_row as create_range_layout
from utils.components.two_column import TwoColumnWidget

class BaseGraphWidget(ExpressionOpWidget):
    """Widget base para visualización de gráficas"""
    def __init__(self, manager, controller, operation_type, input_label, placeholder):
        super().__init__(manager, controller, operation_type, placeholder=placeholder, input_label=input_label, use_dialog_for_result=True)
        self.canvas = None
        self.calculate_button.setText("Graficar")
    
    def create_range_row(self, label_text, min_control, max_control, default_min=-10.0, default_max=10.0):
        """Crea una fila de controles para un rango (min/max) unidos"""
        layout, _, _ = create_range_layout(
            label_text=f"📍 {label_text}", 
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
        input_label = "Ingrese las funciones a graficar en 2D"
        placeholder = "Puede ingresar funciones separadas por comas\n(Ej: x^2, sin(x), cos(x))"
        super().__init__(manager, controller, operation_type, input_label, placeholder)
        self.add_inputs()

    def add_inputs(self):
        # Crear widget de dos columnas
        self.title_label.hide()
        two_column_widget = TwoColumnWidget(column1_label=self.input_label_text, column2_label="Rangos")

        # Columna 1: Usar directamente el expression_input heredado
        two_column_widget.add_to_column1(self.expression_input)

        # Columna 2: Rangos
        range_container = QWidget()
        range_layout = QVBoxLayout(range_container)
        range_layout.setContentsMargins(0, 0, 0, 0)
        
        self.x_min = create_float_spinbox(default_val=-10.0)
        self.x_max = create_float_spinbox(default_val=10.0)
        x_row = self.create_range_row("Rango x", self.x_min, self.x_max)
        range_layout.addLayout(x_row)

        # Añadir widget de rangos a la segunda columna
        two_column_widget.add_to_column2(range_container)

        # Añadir el widget de dos columnas al layout principal
        self.layout.insertWidget(1, two_column_widget)

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
        input_label = "Ingrese función a graficar en 3D"
        placeholder = "Ejemplo: x^2 + y^2"
        super().__init__(manager, controller, operation_type, input_label, placeholder)
        self.add_inputs()

    def add_inputs(self):
        # Crear widget de dos columnas
        self.title_label.hide()
        two_column_widget = TwoColumnWidget(column1_label=self.input_label_text, column2_label="Rangos")

        # Columna 1: Usar directamente el expression_input heredado
        two_column_widget.add_to_column1(self.expression_input)

        # Columna 2: Rangos
        range_container = QWidget()
        range_layout = QVBoxLayout(range_container)
        range_layout.setContentsMargins(0, 0, 0, 0)
        
        # Configurar rangos X e Y
        self.x_min = create_float_spinbox(default_val=-10.0)
        self.x_max = create_float_spinbox(default_val=10.0)
        self.y_min = create_float_spinbox(default_val=-10.0)
        self.y_max = create_float_spinbox(default_val=10.0)
        
        # Crear filas de rangos
        x_row = self.create_range_row("Rango x", self.x_min, self.x_max)
        y_row = self.create_range_row("Rango y", self.y_min, self.y_max)
        
        # Añadir filas al layout de rangos
        range_layout.addLayout(x_row)
        range_layout.addLayout(y_row)

        # Añadir widget de rangos a la segunda columna
        two_column_widget.add_to_column2(range_container)

        # Añadir el widget de dos columnas al layout principal
        self.layout.insertWidget(1, two_column_widget)

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
