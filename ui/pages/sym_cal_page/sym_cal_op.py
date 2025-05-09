from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget, QDoubleSpinBox, QComboBox, QVBoxLayout
from PySide6.QtCore import Qt
from ui.widgets.expression_op_widget import ExpressionOpWidget
from utils.formatting import format_math_expression

class SymCalOpWidget(ExpressionOpWidget):
    def __init__(self, manager, controller, operation_type=None):
        self.manager = manager
        self.controller = controller
        self.operation_type = operation_type
        use_dialog_for_result = True if operation_type == "ecuaciones_diferenciales" else False

        placeholder = "Ejemplo: 2x^2 + 2x"
        if operation_type == "ecuaciones_diferenciales":
            input_label = "Seleccione un método e ingrese la ecuación diferencial a resolver."
            placeholder = "Ejemplos válidos: \ny' = x + y || dy/dx = x + y"
        elif operation_type == "derivadas":
            input_label = "Ingresa una expresión para calcular la derivada:"
        else:
            input_label = "Ingresa una expresión y seleccione el tipo de integral a resolver."

        super().__init__(
            manager,
            controller,
            operation_type=operation_type,
            placeholder=placeholder,
            input_label=input_label,
            use_dialog_for_result=use_dialog_for_result
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
        """Configura los inputs para límites de integración en una única fila horizontal"""
        self.limits_widget = QWidget()
        limits_layout = QHBoxLayout(self.limits_widget)
        limits_layout.setContentsMargins(20, 0, 0, 0)
        
        # Selector para tipo de integral
        limits_layout.addWidget(QLabel("Tipo de integral:"))
        self.integral_type = QComboBox()
        self.integral_type.addItem("Integral indefinida", "indefinite")
        self.integral_type.addItem("Integral definida", "definite")
        self.integral_type.currentTextChanged.connect(self.toggle_limits_visibility)
        limits_layout.addWidget(self.integral_type)
        
        # Controles de límites en la misma fila
        self.limits_input_widget = QWidget()
        limits_input_layout = QHBoxLayout(self.limits_input_widget)
        limits_input_layout.setContentsMargins(10, 0, 0, 0)
        limits_input_layout.setSpacing(5)
        
        limits_input_layout.addWidget(QLabel("Desde x ="))
        self.lower_limit = QDoubleSpinBox()
        self.lower_limit.setRange(-1000, 1000)
        self.lower_limit.setValue(0)
        self.lower_limit.setDecimals(2)
        self.lower_limit.setAlignment(Qt.AlignCenter)
        self.lower_limit.setFixedWidth(70)
        limits_input_layout.addWidget(self.lower_limit)

        limits_input_layout.addWidget(QLabel("Hasta x ="))
        self.upper_limit = QDoubleSpinBox()
        self.upper_limit.setRange(-1000, 1000)
        self.upper_limit.setValue(1)
        self.upper_limit.setDecimals(2)
        self.upper_limit.setAlignment(Qt.AlignCenter)
        self.upper_limit.setFixedWidth(70)
        limits_input_layout.addWidget(self.upper_limit)
        
        # Agregar el widget de límites al layout principal
        limits_layout.addWidget(self.limits_input_widget)
        limits_layout.addStretch()
        
        # Insertar el widget completo en el layout de la interfaz
        self.layout.insertWidget(1, self.limits_widget)
        
        # Configurar estado inicial (oculto)
        self.limits_input_widget.setVisible(False)
        
    def toggle_limits_visibility(self, integral_type):
        """Muestra u oculta los límites de integración según el tipo seleccionado"""
        self.limits_input_widget.setVisible(integral_type == "Integral definida")
        self.layout.update()  # Actualizar la UI

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
        
        # Widget para parámetros comunes
        self.common_params_widget = QWidget()
        common_layout = QHBoxLayout(self.common_params_widget)
        common_layout.setContentsMargins(10, 0, 0, 0)
        common_layout.setSpacing(5)
        
        # Condición inicial
        common_layout.addWidget(QLabel("y("))
        self.euler_x0 = QDoubleSpinBox()
        self.euler_x0.setFixedWidth(70)
        self.euler_x0.setRange(-1000, 1000)
        self.euler_x0.setValue(0)  # Cambiar a 0 para el ejemplo de interés
        common_layout.addWidget(self.euler_x0)
        common_layout.addWidget(QLabel(") ="))
        self.euler_y0 = QDoubleSpinBox()
        self.euler_y0.setFixedWidth(70)
        self.euler_y0.setRange(-1000, 1000)
        self.euler_y0.setValue(1000)  # Cambiar a 1000 para el ejemplo de interés
        common_layout.addWidget(self.euler_y0)
        
        # Rango de solución
        common_layout.addWidget(QLabel("Rango:"))
        common_layout.addWidget(QLabel("x ="))
        self.euler_x_start = QDoubleSpinBox()
        self.euler_x_start.setFixedWidth(70)
        self.euler_x_start.setRange(-1000, 1000)
        self.euler_x_start.setValue(0)  # Cambiar a 0 para el ejemplo de interés
        common_layout.addWidget(self.euler_x_start)
        common_layout.addWidget(QLabel("a"))
        self.euler_x_end = QDoubleSpinBox()
        self.euler_x_end.setFixedWidth(70)
        self.euler_x_end.setRange(-1000, 1000)
        self.euler_x_end.setValue(10)  # Cambiar a 10 para el ejemplo de interés
        common_layout.addWidget(self.euler_x_end)
        
        # Widget solo para parámetros de Euler
        self.euler_step_widget = QWidget()
        euler_step_layout = QHBoxLayout(self.euler_step_widget)
        euler_step_layout.setContentsMargins(0, 0, 0, 0)
        euler_step_layout.setSpacing(5)
        
        # Paso h (solo para Euler)
        euler_step_layout.addWidget(QLabel("h ="))
        self.euler_h = QDoubleSpinBox()
        self.euler_h.setFixedWidth(70)
        self.euler_h.setRange(0.001, 5)
        self.euler_h.setValue(0.1)
        euler_step_layout.addWidget(self.euler_h)
        
        # Agregar widgets al layout
        common_layout.addWidget(self.euler_step_widget)
        common_layout.addStretch()
        container_layout.addWidget(self.common_params_widget)
        container_layout.addStretch()
        
        # Conectar señal para mostrar/ocultar parámetros específicos de Euler
        self.de_method_selector.currentTextChanged.connect(self.toggle_euler_step)
        
        # Insertar el contenedor en el layout principal
        self.layout.insertWidget(1, method_container)
        
        # Mostrar/ocultar parámetros según el método inicial
        self.toggle_euler_step(self.de_method_selector.currentText())

    def toggle_euler_step(self, method):
        """Muestra u oculta el parámetro de paso según la selección"""
        self.euler_step_widget.setVisible(method == "Método de Euler")
        self.layout.update()  # Ajustar el tamaño del widget

    def execute_operation(self):
        expression = self.get_input_expression().strip()
        if self.operation_type == "derivadas":
            result = self.controller.compute_derivative(expression)
        elif self.operation_type == "integrales":
            if hasattr(self, 'integral_type') and self.integral_type.currentData() == "definite":
                # Para integral definida
                limits = (self.lower_limit.value(), self.upper_limit.value())
                result = self.controller.compute_integral(expression, limits)
            else:
                # Para integral indefinida
                result = self.controller.compute_integral(expression)
        elif self.operation_type == "ecuaciones_diferenciales":
            # Código existente para ecuaciones diferenciales...
            x_range = (self.euler_x_start.value(), self.euler_x_end.value())
            initial_condition = (self.euler_x0.value(), self.euler_y0.value())
            
            if self.de_method_selector.currentData() == "analytical":
                result = self.controller.solve_differential_equation(expression, initial_condition=initial_condition, x_range=x_range)
            else:  # Euler
                h = self.euler_h.value()
                result = self.controller.solve_ode_euler(expression, initial_condition, x_range, h)
        else:
            raise ValueError("Tipo de operación desconocido.")
        return result

    def on_calculate_clicked(self):
        """Sobrescribe el método para manejar los resultados con canvas"""
        is_valid, error_message = self.validate_operation()
            
        if not is_valid:
           return False, error_message
        
        try:
            result = self.execute_operation()
            formatted_result = self.prepare_result_display(result)
            self.process_operation_result(formatted_result)
            return True, "Operación completada exitosamente"
        except Exception as e:
           return False, f"Error al calcular la operación: {str(e)}"
        
    def prepare_result_display(self, result):
        expr_str = self.get_input_expression().strip()
        try:
            if self.operation_type == "ecuaciones_diferenciales":
                parsed_expr = self.controller.parser.parse_equation(expr_str)
                method = self.de_method_selector.currentData() if hasattr(self, 'de_method_selector') else None
                
                # Si hay un canvas en el resultado (para métodos numéricos)
                if isinstance(result, dict) and "solution" in result and "canvas" in result:
                    html_content = format_math_expression(parsed_expr, result["solution"], self.operation_type, method=method)
                    # Devolver un diccionario con el HTML y el canvas
                    return {
                        "html": html_content,
                        "canvas": result["canvas"]
                    }
                else:
                    # Para soluciones sin canvas 
                    return format_math_expression(parsed_expr, result, self.operation_type, method=method)
            else:
                parsed_expr = self.controller.parser.parse_expression(expr_str)
                return format_math_expression(parsed_expr, result, self.operation_type)
        except Exception as e:
            raise ValueError(f"Ocurrió un error: {str(e)}")
        