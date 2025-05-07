from PySide6.QtWidgets import QHBoxLayout, QLabel, QSpinBox, QWidget, QDoubleSpinBox, QComboBox, QVBoxLayout
from PySide6.QtCore import Qt
from ui.widgets.expression_op_widget import ExpressionOpWidget
from utils.formatting import format_math_expression

class SymCalOpWidget(ExpressionOpWidget):
    def __init__(self, manager, controller, operation_type=None):
        self.manager = manager
        self.controller = controller
        self.operation_type = operation_type

        if operation_type == "ecuaciones_diferenciales":
            input_label = "Seleccione un método e ingrese la ecuación diferencial a resolver."
            placeholder = "Ejemplos válidos: \ny' = x + y || dy/dx = x + y"
        else:
            input_label = f"Ingresa una expresión para realizar cálculo de {operation_type.replace('_', ' ')}:"
            placeholder = "Ejemplo: 2x^2 + 2x"

        super().__init__(
            manager,
            controller,
            operation_type=operation_type,
            placeholder=placeholder,
            input_label=input_label,
            use_dialog_for_result=False
        )

        self.add_additional_inputs()

    def validate_operation(self):
        expression = self.get_input_expression().strip()
        if not expression:
            return False, "Por favor ingresa una expresión para continuar."
        try:
            if self.operation_type == "ecuaciones_diferenciales":
                self.controller.parser.parse_equation(expression)
            else:
                self.controller.parser.parse_expression(expression)
            return True, ""
        except Exception as e:
            return False, f"Expresión inválida: {str(e)}"

    def add_additional_inputs(self):
        if self.operation_type == "integrales":
            self.add_integral_limits_inputs()
        elif self.operation_type == "ecuaciones_diferenciales":
            self.add_differential_equation_inputs()

    def add_integral_limits_inputs(self):
        """Configura los inputs para límites de integración"""
        self.limits_widget = QWidget()
        limits_layout = QHBoxLayout(self.limits_widget)
        limits_layout.setContentsMargins(20, 0, 0, 0)

        limits_layout.addWidget(QLabel("Desde x ="))
        self.lower_limit = QSpinBox()
        self.lower_limit.setRange(-1000, 1000)
        self.lower_limit.setValue(0)
        self.lower_limit.setAlignment(Qt.AlignCenter)
        limits_layout.addWidget(self.lower_limit)

        limits_layout.addWidget(QLabel("Hasta x ="))
        self.upper_limit = QSpinBox()
        self.upper_limit.setRange(-1000, 1000)
        self.upper_limit.setValue(1)
        self.upper_limit.setAlignment(Qt.AlignCenter)
        limits_layout.addWidget(self.upper_limit)
        limits_layout.addStretch()

        self.layout.insertWidget(1, self.limits_widget)

    def add_differential_equation_inputs(self):
        """Configura los inputs adicionales para ecuaciones diferenciales"""
        # Contenedor principal para todos los elementos
        method_container = QWidget()
        container_layout = QHBoxLayout(method_container)
        container_layout.setContentsMargins(20, 0, 20, 0)
        
        # Selector de método
        self.de_method_selector = QComboBox()
        self.de_method_selector.addItem("Solución Analítica", "analytical")
        self.de_method_selector.addItem("Método de Euler", "euler")
        container_layout.addWidget(QLabel("Método:"))
        container_layout.addWidget(self.de_method_selector)
        
        # Widget para parámetros de Euler (inicialmente oculto)
        self.euler_params_widget = QWidget()
        euler_layout = QHBoxLayout(self.euler_params_widget)
        euler_layout.setContentsMargins(10, 0, 0, 0)
        euler_layout.setSpacing(5)
        
        # Condición inicial
        euler_layout.addWidget(QLabel("y("))
        self.euler_x0 = QDoubleSpinBox()
        self.euler_x0.setFixedWidth(70)
        self.euler_x0.setRange(-1000, 1000)
        self.euler_x0.setValue(1)
        euler_layout.addWidget(self.euler_x0)
        euler_layout.addWidget(QLabel(") ="))
        self.euler_y0 = QDoubleSpinBox()
        self.euler_y0.setFixedWidth(70)
        self.euler_y0.setRange(-1000, 1000)
        self.euler_y0.setValue(2)
        euler_layout.addWidget(self.euler_y0)
        
        # Rango de solución
        euler_layout.addWidget(QLabel("Rango:"))
        euler_layout.addWidget(QLabel("x ="))
        self.euler_x_start = QDoubleSpinBox()
        self.euler_x_start.setFixedWidth(70)
        self.euler_x_start.setRange(-1000, 1000)
        self.euler_x_start.setValue(1)
        euler_layout.addWidget(self.euler_x_start)
        euler_layout.addWidget(QLabel("a"))
        self.euler_x_end = QDoubleSpinBox()
        self.euler_x_end.setFixedWidth(70)
        self.euler_x_end.setRange(-1000, 1000)
        self.euler_x_end.setValue(2)
        euler_layout.addWidget(self.euler_x_end)
        
        # Paso h
        euler_layout.addWidget(QLabel("h ="))
        self.euler_h = QDoubleSpinBox()
        self.euler_h.setFixedWidth(70)
        self.euler_h.setRange(0.001, 1)
        self.euler_h.setValue(0.1)
        euler_layout.addWidget(self.euler_h)
        
        euler_layout.addStretch()
        self.euler_params_widget.hide()
        
        # Añadir los parámetros al contenedor principal
        container_layout.addWidget(self.euler_params_widget)
        container_layout.addStretch()
        
        # Conectar señal para mostrar/ocultar parámetros
        self.de_method_selector.currentTextChanged.connect(self.toggle_euler_params)
        
        # Insertar el contenedor en el layout principal
        self.layout.insertWidget(1, method_container)

    def toggle_euler_params(self, method):
        """Muestra u oculta los parámetros del método de Euler según la selección"""
        self.euler_params_widget.setVisible(method == "Método de Euler")
        self.layout.update() # Ajustar el tamaño del widget

    def execute_operation(self):
        expression = self.get_input_expression().strip()
        if self.operation_type == "derivadas":
            result = self.controller.compute_derivative(expression)
        elif self.operation_type == "integrales":
            limits = (self.lower_limit.value(), self.upper_limit.value())
            result = self.controller.compute_integral(expression, limits)
        elif self.operation_type == "ecuaciones_diferenciales":
            if self.de_method_selector.currentData() == "analytical":
                result = self.controller.solve_differential_equation(expression)
            else:  # Euler
                initial_condition = (self.euler_x0.value(), self.euler_y0.value())
                x_range = (self.euler_x_start.value(), self.euler_x_end.value())
                h = self.euler_h.value()
                result = self.controller.solve_ode_euler(expression, initial_condition, x_range, h)
        else:
            raise ValueError("Tipo de operación desconocido.")
        return result

    def prepare_result_display(self, result):
        expr_str = self.get_input_expression().strip()
        try:
            if self.operation_type == "ecuaciones_diferenciales":
                parsed_expr = self.controller.parser.parse_equation(expr_str)
                method = self.de_method_selector.currentData() if hasattr(self, 'de_method_selector') else None
                return format_math_expression(parsed_expr, result, self.operation_type, method=method)
            else:
                parsed_expr = self.controller.parser.parse_expression(expr_str)
                return format_math_expression(parsed_expr, result, self.operation_type)
        except Exception as e:
            raise ValueError(f"Ocurrió un error: {str(e)}")