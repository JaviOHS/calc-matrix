from .base_operation import BaseSymCalOperation
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget, QComboBox, QVBoxLayout
from PySide6.QtCore import Qt
from utils.components.spinbox_utils import create_float_spinbox
from utils.components.two_column import TwoColumnWidget

class IntegralOperation(BaseSymCalOperation):
    def __init__(self, manager, controller):
        super().__init__(manager=manager, controller=controller, operation_type="integral", placeholder="Ejemplo: 2x^2 + 2x", input_label="Ingrese expresión",)
        self.setup_integral_inputs()
    
    def setup_integral_inputs(self):
        """Configura los inputs para límites de integración usando una estructura de dos columnas"""
        self.title_label.hide()
        result_container = self.detach_result_container()

        two_column_widget = TwoColumnWidget(column1_label="Configuración", column2_label="Resultado", expression_label=self.input_label_text)
        two_column_widget.add_to_expression(self.expression_input)
        
        # Columna 1: Configuración
        config_container = QWidget()
        config_layout = QVBoxLayout(config_container)
        config_layout.setContentsMargins(0, 0, 0, 0)
        config_layout.setSpacing(5)
        
        # Fila para tipo de integral
        type_row = QWidget()
        type_layout = QHBoxLayout(type_row)
        type_layout.setContentsMargins(0, 0, 0, 0)
        type_layout.addWidget(QLabel("🟠 Tipo de integral:"))
        
        self.integral_type = QComboBox()
        self.integral_type.addItem("Indefinida", "indefinite")
        self.integral_type.addItem("Definida", "definite")
        self.integral_type.setFixedWidth(160)
        self.integral_type.currentTextChanged.connect(self.toggle_limits_visibility)
        type_layout.addWidget(self.integral_type)
        type_layout.addStretch()
        
        # Fila para límites
        self.limits_input_widget = QWidget()
        limits_layout = QHBoxLayout(self.limits_input_widget)
        limits_layout.setContentsMargins(0, 0, 0, 0)
        limits_layout.setSpacing(5)
        
        limits_layout.addWidget(QLabel("📌 Límites: x ="))
        self.lower_limit = create_float_spinbox(default_val=0)
        self.lower_limit.setFixedWidth(60)
        limits_layout.addWidget(self.lower_limit)
        
        limits_layout.addWidget(QLabel("→"))
        self.upper_limit = create_float_spinbox(default_val=1)
        self.upper_limit.setFixedWidth(60)
        limits_layout.addWidget(self.upper_limit)
        limits_layout.addStretch()
        
        # Añadir filas al contenedor de configuración
        config_layout.addWidget(type_row)
        config_layout.addWidget(self.limits_input_widget)
        
        # Añadir el contenedor de configuración a la primera columna
        two_column_widget.add_to_column1(config_container)
        
        # Añadir el contenedor de resultado a la segunda columna
        two_column_widget.add_to_column2(result_container)
        
        # Insertar el widget de dos columnas en el layout principal
        self.layout.insertWidget(1, two_column_widget)
        
        # Ocultar límites inicialmente
        self.limits_input_widget.setVisible(False)
    
    def toggle_limits_visibility(self, integral_type):
        """Muestra u oculta los límites de integración según el tipo seleccionado"""
        self.limits_input_widget.setVisible(integral_type == "Definida")
        self.layout.update()
    
    def execute_operation(self):
        expression = self.get_input_expression().strip()
        if self.integral_type.currentData() == "definite":
            limits = (self.lower_limit.value(), self.upper_limit.value())
            return self.controller.compute_integral(expression, limits)
        return self.controller.compute_integral(expression)
