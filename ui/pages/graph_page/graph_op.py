from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QSpinBox, QVBoxLayout, QWidget
from ui.widgets.expression_op_widget import ExpressionOpWidget
from controller.graph_controller import GraphController

class Graph2DWidget(ExpressionOpWidget):
    def __init__(self, manager=GraphController, controller=GraphController, operation_type=None):
        input_label = f"Ingrese una función para realizar {operation_type.replace('_', ' ')}:"
        placeholder = "Ejemplo: x^2 + 2^x + 1"
        super().__init__(manager, controller, operation_type, placeholder=placeholder, input_label=input_label, use_dialog_for_result=True)
        self.canvas = None
        self.add_range_inputs()
        
    def add_range_inputs(self):
        self.range_widget = QWidget()
        x_layout = QHBoxLayout(self.range_widget)
        x_layout.setContentsMargins(0, 0, 0, 0)
        x_layout.setSpacing(10)

        x_label_from = QLabel("Desde x:")
        x_label_from.setFixedWidth(70)
        x_layout.addWidget(x_label_from)

        self.x_min = QSpinBox()
        self.x_min.setRange(-100, 100)
        self.x_min.setValue(-10)
        self.x_min.setFixedWidth(80)
        x_layout.addWidget(self.x_min)

        x_label_to = QLabel("Hasta x:")
        x_label_to.setFixedWidth(70)
        x_layout.addWidget(x_label_to)

        self.x_max = QSpinBox()
        self.x_max.setRange(-100, 100)
        self.x_max.setValue(10)
        self.x_max.setFixedWidth(80)
        x_layout.addWidget(self.x_max)

        x_layout.addStretch()
        self.layout.insertWidget(2, self.range_widget)

    def get_inputs(self):
        return {
            "expression": self.get_input_expression(),
            "x_range": (self.x_min.value(), self.x_max.value())
        }

    def display_result(self, result):
        if self.use_dialog_for_result:
            # Si es canvas, lo mostramos en el dialogo personalizado
            if hasattr(result, 'draw'):
                self.show_canvas_dialog(result)
        else:
            self.result_display.setText(str(result))

    def clear_result(self):
        if self.canvas:
            self.result_container.layout().removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

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
            self.controller.generate_canvas_2d(self.get_inputs())
        except ValueError as e:
            return False, str(e)

    def on_calculate_clicked(self):
        result = self.perform_operation()
        if result:
            self.display_result(result)

    def cleanup(self):
        self.clear_result()
        super().cleanup()
    
class Graph3DWidget(ExpressionOpWidget):
    def __init__(self, manager=GraphController, controller=GraphController, operation_type=None):
        input_label = f"Ingrese una función para realizar {operation_type.replace('_', ' ')}:"
        placeholder = "Ejemplo: x^2 + y^2"
        super().__init__(manager, controller, operation_type, placeholder=placeholder, input_label=input_label, use_dialog_for_result=True)
        self.canvas = None
        self.add_range_inputs()

    def add_range_inputs(self):
        self.range_widget = QWidget()
        main_layout = QVBoxLayout(self.range_widget)  # Layout principal vertical
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)

        # Layout para X
        x_layout = QHBoxLayout()
        x_layout.setSpacing(10)

        x_label_from = QLabel("Desde x:")
        x_label_from.setFixedWidth(70)
        x_layout.addWidget(x_label_from)

        self.x_min = QSpinBox()
        self.x_min.setRange(-100, 100)
        self.x_min.setValue(-10)
        self.x_min.setFixedWidth(80)
        x_layout.addWidget(self.x_min)

        x_label_to = QLabel("Hasta x:")
        x_label_to.setFixedWidth(70)
        x_layout.addWidget(x_label_to)

        self.x_max = QSpinBox()
        self.x_max.setRange(-100, 100)
        self.x_max.setValue(10)
        self.x_max.setFixedWidth(80)
        x_layout.addWidget(self.x_max)

        x_layout.addStretch()
        main_layout.addLayout(x_layout)  # Añadir layout de X al principal

        # Layout para Y
        y_layout = QHBoxLayout()
        y_layout.setSpacing(10)

        y_label_from = QLabel("Desde y:")
        y_label_from.setFixedWidth(70)
        y_layout.addWidget(y_label_from)

        self.y_min = QSpinBox()
        self.y_min.setRange(-100, 100)
        self.y_min.setValue(-10)
        self.y_min.setFixedWidth(80)
        y_layout.addWidget(self.y_min)

        y_label_to = QLabel("Hasta y:")
        y_label_to.setFixedWidth(70)
        y_layout.addWidget(y_label_to)

        self.y_max = QSpinBox()
        self.y_max.setRange(-100, 100)
        self.y_max.setValue(10)
        self.y_max.setFixedWidth(80)
        y_layout.addWidget(self.y_max)

        y_layout.addStretch()
        main_layout.addLayout(y_layout)

        self.layout.insertWidget(2, self.range_widget)

    def get_inputs(self):
        x_range = (self.x_min.value(), self.x_max.value())
        y_range = (self.y_min.value(), self.y_max.value())
        return {
            "expression": self.get_input_expression(),
            "x_range": x_range,
            "y_range": y_range
        }

    def display_result(self, result):
        if self.use_dialog_for_result:
            # Si es canvas, lo mostramos en el dialogo personalizado
            if hasattr(result, 'draw'):
                self.show_canvas_dialog(result)
        else:
            self.result_display.setText(str(result))

    def clear_result(self):
        if self.canvas:
            self.result_container.layout().removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

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
            # Debes capturar y retornar el resultado del controlador
            result = self.controller.generate_canvas_3d(self.get_inputs())
            return True, result  # Retornar estado y resultado
        except Exception as e:
            return False, str(e)

    def on_calculate_clicked(self):
        result = self.perform_operation()
        if result:
            self.display_result(result)

    def cleanup(self):
        self.clear_result()
        super().cleanup()
