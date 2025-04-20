from PySide6.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QSpinBox
from PySide6.QtCore import Qt
from widgets.math_operation_widget import MathOperationWidget

class Graph2DWidget(MathOperationWidget):
    def __init__(self, manager, controller, operation_type=None):
        super().__init__(manager, controller, operation_type)
        self.setup_ui()
        self.canvas = None

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Función matemática
        func_layout = QHBoxLayout()
        func_layout.setSpacing(10)
        func_label = QLabel("Función f(x):")
        func_label.setFixedWidth(100)
        func_layout.addWidget(func_label)
        self.function_input = QLineEdit("x**2 + 2*x + 1")
        func_layout.addWidget(self.function_input)
        layout.addLayout(func_layout)

        # Rango X
        x_layout = QHBoxLayout()
        x_layout.setSpacing(5)
        
        x_label_from = QLabel("Desde x:")
        x_label_from.setFixedWidth(60)
        x_layout.addWidget(x_label_from)
        
        self.x_min = QSpinBox()
        self.x_min.setRange(-100, 100)
        self.x_min.setValue(-10)
        self.x_min.setFixedWidth(80)
        self.x_min.setAlignment(Qt.AlignCenter)
        x_layout.addWidget(self.x_min)
        
        x_label_to = QLabel("Hasta x:")
        x_label_to.setFixedWidth(60)
        x_layout.addWidget(x_label_to)
        
        self.x_max = QSpinBox()
        self.x_max.setRange(-100, 100)
        self.x_max.setValue(10)
        self.x_max.setFixedWidth(80)
        self.x_max.setAlignment(Qt.AlignCenter)
        x_layout.addWidget(self.x_max)
        
        x_layout.addStretch(1)
        layout.addLayout(x_layout)

        # Botones
        buttons_widget = self.create_buttons("Cancelar", "Graficar")
        self.cancel_button.clicked.connect(self.cleanup)
        self.calculate_button.clicked.connect(self.on_calculate_clicked)
        layout.addWidget(buttons_widget)

        # Área para la gráfica
        self.result_area = QVBoxLayout()
        layout.addLayout(self.result_area)

    def get_inputs(self):
        return {
            "expression": self.function_input.text(),
            "x_range": (self.x_min.value(), self.x_max.value())
        }

    def display_result(self, canvas):
        self.clear_result()
        if canvas:
            self.canvas = canvas
            self.result_area.addWidget(canvas)
            canvas.draw()  # Importante: refrescar el canvas

    def clear_result(self):
        if self.canvas:
            self.result_area.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

    def validate_operation(self):
        expr = self.function_input.text().strip()
        if not expr:
            return False, "Debes ingresar una función válida."
        return True, ""

    def perform_operation(self):
        valid, msg = self.validate_operation()
        if not valid:
            print(msg)  # O mostrar un QMessageBox
            return None
        return self.controller.generate_canvas_2d(self.get_inputs())

    def on_calculate_clicked(self):
        result = self.perform_operation()
        if result:
            self.display_result(result)

    def cleanup(self):
        self.clear_result()
        super().cleanup()
    
class Graph3DWidget(MathOperationWidget):
    def __init__(self, manager, controller, operation_type=None):
        super().__init__(manager, controller, operation_type)
        self.setup_ui()
        self.canvas = None
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Función Z = f(x, y)
        func_layout = QHBoxLayout()
        func_layout.setSpacing(10)
        func_label = QLabel("Función Z = f(x, y):")
        func_label.setFixedWidth(120)
        func_layout.addWidget(func_label)
        self.function_input = QLineEdit("x * np.exp(-x**2 - y**2)")
        func_layout.addWidget(self.function_input)
        layout.addLayout(func_layout)

        # Rango X
        x_layout = QHBoxLayout()
        x_layout.setSpacing(10)
        
        x_label_from = QLabel("Desde X:")
        x_label_from.setFixedWidth(80)
        x_layout.addWidget(x_label_from)
        
        self.x_min = QSpinBox()
        self.x_min.setRange(-100, 100)
        self.x_min.setValue(-2)
        self.x_min.setFixedWidth(80)
        self.x_min.setAlignment(Qt.AlignCenter)
        x_layout.addWidget(self.x_min)
        
        x_label_to = QLabel("Hasta X:")
        x_label_to.setFixedWidth(80)
        x_layout.addWidget(x_label_to)
        
        self.x_max = QSpinBox()
        self.x_max.setRange(-100, 100)
        self.x_max.setValue(2)
        self.x_max.setFixedWidth(80)
        self.x_max.setAlignment(Qt.AlignCenter)
        x_layout.addWidget(self.x_max)
        
        x_layout.addStretch(1)
        layout.addLayout(x_layout)

        # Rango Y
        y_layout = QHBoxLayout()
        y_layout.setSpacing(10)

        y_label_from = QLabel("Desde Y:")
        y_label_from.setFixedWidth(80)
        y_layout.addWidget(y_label_from)
        
        self.y_min = QSpinBox()
        self.y_min.setRange(-100, 100)
        self.y_min.setValue(-2)
        self.y_min.setFixedWidth(80)
        self.y_min.setAlignment(Qt.AlignCenter)
        y_layout.addWidget(self.y_min)

        y_label_to = QLabel("Hasta Y:")
        y_label_to.setFixedWidth(80)
        y_layout.addWidget(y_label_to)
        
        self.y_max = QSpinBox()
        self.y_max.setRange(-100, 100)
        self.y_max.setValue(2)
        self.y_max.setFixedWidth(80)
        self.y_max.setAlignment(Qt.AlignCenter)
        y_layout.addWidget(self.y_max)

        y_layout.addStretch(1)
        layout.addLayout(y_layout)

        # Botones
        buttons_widget = self.create_buttons("Cancelar", "Graficar")
        self.cancel_button.clicked.connect(self.cleanup)
        self.calculate_button.clicked.connect(self.on_calculate_clicked)
        layout.addWidget(buttons_widget)

        # Área para la gráfica
        self.result_area = QVBoxLayout()
        layout.addLayout(self.result_area)

    def get_inputs(self):
        return {
            "expression": self.function_input.text(),
            "x_range": (self.x_min.value(), self.x_max.value()),
            "y_range": (self.y_min.value(), self.y_max.value()),
        }

    def display_result(self, canvas):
        self.clear_result()
        if canvas:
            self.canvas = canvas
            self.result_area.addWidget(canvas)
            canvas.draw()

    def clear_result(self):
        if self.canvas:
            self.result_area.removeWidget(self.canvas)
            self.canvas.deleteLater()
            self.canvas = None

    def perform_operation(self):
        return self.controller.generate_canvas_3d(self.get_inputs())

    def on_calculate_clicked(self):
        result = self.perform_operation()
        if result:
            self.display_result(result)

    def cleanup(self):
        self.clear_result()
        super().cleanup()
