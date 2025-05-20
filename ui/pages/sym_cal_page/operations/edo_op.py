from .base_operation import BaseSymCalOperation
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget, QComboBox, QVBoxLayout
from utils.components.spinbox_utils import create_float_spinbox
from utils.components.two_column import TwoColumnWidget

class DifferentialEqOperation(BaseSymCalOperation):
    def __init__(self, manager, controller):
        super().__init__( manager=manager, controller=controller, operation_type="differential_equation", placeholder="Ejemplos válidos: \ny'(x) = x + y || dy/dx = x + y", input_label="Ingrese ecuación diferencial", use_dialog_for_result=True)
        self.setup_differential_inputs()
    
    def setup_differential_inputs(self):
        """Configura los inputs adicionales para ecuaciones diferenciales"""
        self.title_label.hide()
        two_column_widget = TwoColumnWidget(expression_label=self.input_label_text, column1_label="Configuración básica", column2_label="Parámetros de simulación")
        two_column_widget.add_to_expression(self.expression_input)

        # Columna 1: Método y condición inicial
        method_container = QWidget()
        method_layout = QVBoxLayout(method_container)
        method_layout.setContentsMargins(0, 0, 0, 0)
        method_layout.setSpacing(5)

        # Selector de método
        method_row = QWidget()
        method_row_layout = QHBoxLayout(method_row)
        method_row_layout.setContentsMargins(0, 0, 0, 0)
        method_row_layout.addWidget(QLabel("🟠 Método:"))
        
        self.de_method_selector = QComboBox()
        self.de_method_selector.addItem("Analítico", "analytical")
        self.de_method_selector.addItem("Euler", "euler")
        self.de_method_selector.addItem("Heun", "heun")
        self.de_method_selector.addItem("RK4", "rk4")
        self.de_method_selector.addItem("Taylor 2° orden", "taylor")
        self.de_method_selector.setFixedWidth(180)
        method_row_layout.addWidget(self.de_method_selector)
        method_row_layout.addStretch()

        # Condición inicial
        initial_condition_row = QWidget()
        initial_condition_layout = QHBoxLayout(initial_condition_row)
        initial_condition_layout.setContentsMargins(0, 0, 0, 0)
        initial_condition_layout.addWidget(QLabel("🔍 y ("))
        self.numerical_x0 = create_float_spinbox(default_val=0)
        self.numerical_x0.setFixedWidth(60)
        initial_condition_layout.addWidget(self.numerical_x0)
        initial_condition_layout.addWidget(QLabel(") ="))
        self.numerical_y0 = create_float_spinbox(default_val=1)
        self.numerical_y0.setFixedWidth(60)
        initial_condition_layout.addWidget(self.numerical_y0)
        initial_condition_layout.addStretch()

        # Añadir filas al contenedor de método
        method_layout.addWidget(method_row)
        method_layout.addWidget(initial_condition_row)

        # Columna 2: Rango y paso
        params_container = QWidget()
        params_layout = QVBoxLayout(params_container)
        params_layout.setContentsMargins(0, 0, 0, 0)
        params_layout.setSpacing(5)

        # Rango
        range_row = QWidget()
        range_layout = QHBoxLayout(range_row)
        range_layout.setContentsMargins(0, 0, 0, 0)
        range_layout.addWidget(QLabel("📏 Rango x:"))
        self.numerical_x_start = create_float_spinbox(default_val=0)
        self.numerical_x_start.setFixedWidth(60)
        range_layout.addWidget(self.numerical_x_start)
        range_layout.addWidget(QLabel("→"))
        self.numerical_x_end = create_float_spinbox(default_val=10)
        self.numerical_x_end.setFixedWidth(60)
        range_layout.addWidget(self.numerical_x_end)
        range_layout.addStretch()

        # Paso h
        step_row = QWidget()
        step_layout = QHBoxLayout(step_row)
        step_layout.setContentsMargins(0, 0, 0, 0)
        self.step_label = QLabel("👣​ Paso h =")
        step_layout.addWidget(self.step_label)
        self.numerical_h = create_float_spinbox(min_val=0.001, max_val=5, default_val=1, step=0.1)
        self.numerical_h.setFixedWidth(60)
        step_layout.addWidget(self.numerical_h)
        step_layout.addStretch()

        # Añadir filas al contenedor de parámetros
        params_layout.addWidget(range_row)
        params_layout.addWidget(step_row)

        # Añadir contenedores a las columnas
        two_column_widget.add_to_column1(method_container)
        two_column_widget.add_to_column2(params_container)

        # Insertar el widget de dos columnas en el layout principal
        self.layout.insertWidget(1, two_column_widget)

        # Conectar señal para mostrar/ocultar parámetros específicos
        self.de_method_selector.currentTextChanged.connect(self.toggle_step)
        
        # Mostrar/ocultar parámetros según el método inicial
        self.toggle_step(self.de_method_selector.currentText())

    def toggle_step(self, method):
        """Muestra u oculta el parámetro de paso según la selección"""
        show_step = method in ["Euler", "Heun", "RK4", "Taylor 2° orden"]
        self.step_label.setVisible(show_step)
        self.numerical_h.setVisible(show_step)
        self.layout.update()

    def execute_operation(self):
        expression = self.get_input_expression().strip()
        x_range = (self.numerical_x_start.value(), self.numerical_x_end.value())
        initial_condition = (self.numerical_x0.value(), self.numerical_y0.value())
        
        method = self.de_method_selector.currentData()
        if method == "analytical":
            return self.controller.solve_differential_equation(
                expression, 
                initial_condition=initial_condition, 
                x_range=x_range
            )
        
        h = self.numerical_h.value()
        method_func = getattr(self.controller, f"solve_ode_{method}", None)
        if method_func:
            return method_func(expression, initial_condition, x_range, h)
        raise ValueError(f"Método numérico no implementado: {method}")