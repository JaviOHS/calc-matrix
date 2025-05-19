from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget, QComboBox, QVBoxLayout
from ui.widgets.expression_op_widget import ExpressionOpWidget
from utils.formating.formatting import format_math_expression
from utils.spinbox_utils import create_float_spinbox

class SymCalOpWidget(ExpressionOpWidget):
    def __init__(self, manager, controller, operation_type=None):
        self.manager = manager
        self.controller = controller
        self.operation_type = operation_type
        use_dialog_for_result = True if operation_type == "differential_equation" else False

        input_label = f"Ingresa una expresión para realizar cálculo de {operation_type.replace("_", " ")}:"
        placeholder = "Ejemplo: 2x^2 + 2x"
        
        if operation_type == "differential_equation":
            placeholder = "Ejemplos válidos: \n- y' = x + y\n- dy/dx = x + y"
        super().__init__(manager, controller, operation_type=operation_type, placeholder=placeholder, input_label=input_label, use_dialog_for_result=use_dialog_for_result)

        self.add_additional_inputs()

    def validate_operation(self):
        expression = self.get_input_expression().strip()
        if not expression:
            return False, "Por favor ingresa una expresión para continuar."
        try:
            if self.operation_type == "differential_equation":
                self.controller.parser.parse_equation(expression)
            else:
                self.controller.parser.parse_expression(expression)
            return True, ""
        except Exception as e:
            return False, f"Expresión inválida: {str(e)}"

    def add_additional_inputs(self):
        if self.operation_type == "integral":
            self.add_integral_limits_inputs()
        elif self.operation_type == "differential_equation":
            self.add_differential_equation_inputs()

    def add_integral_limits_inputs(self):
        """Configura los inputs para límites de integración"""
        # Contenedor principal horizontal
        top_row = QWidget()
        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(24, 0, 12, 0)
        top_layout.setSpacing(5)

        # Etiqueta de tipo de integral
        instruction_label = QLabel("🟠 Tipo de integral:")
        top_layout.addWidget(instruction_label)

        # ComboBox de tipo
        self.integral_type = QComboBox()
        self.integral_type.addItem("Indefinida", "indefinite")
        self.integral_type.addItem("Definida", "definite")
        self.integral_type.currentTextChanged.connect(self.toggle_limits_visibility)
        self.integral_type.setFixedWidth(160)
        top_layout.addWidget(self.integral_type)

        # Contenedor para límites
        self.limits_input_widget = QWidget()
        limits_layout = QHBoxLayout(self.limits_input_widget)
        limits_layout.setContentsMargins(20, 0, 0, 0)

        limits_layout.addWidget(QLabel("📌 Límites: x ="))
        self.lower_limit = create_float_spinbox(default_val=0)
        self.lower_limit.setFixedWidth(60)
        limits_layout.addWidget(self.lower_limit)

        limits_layout.addWidget(QLabel("→"))
        self.upper_limit = create_float_spinbox(default_val=1)
        self.upper_limit.setFixedWidth(60)
        limits_layout.addWidget(self.upper_limit)

        top_layout.addWidget(self.limits_input_widget)
        top_layout.addStretch()

        self.layout.insertWidget(0, top_row)
        self.limits_input_widget.setVisible(False)

    def toggle_limits_visibility(self, integral_type):
        """Muestra u oculta los límites de integración según el tipo seleccionado"""
        self.limits_input_widget.setVisible(integral_type == "Definida")
        self.layout.update()  # Actualizar la UI

    def add_differential_equation_inputs(self):
        """Configura los inputs adicionales para ecuaciones diferenciales"""
        method_container = QWidget()
        main_layout = QVBoxLayout(method_container)
        main_layout.setContentsMargins(20, 0, 20, 0)
        
        # Selector de método (fila 1)
        method_row = QHBoxLayout()
        method_row.setContentsMargins(10, 0, 0, 0)
        method_row.addWidget(QLabel("🟠 Método:"))
        
        self.de_method_selector = QComboBox()
        self.de_method_selector.addItem("Analítico", "analytical")
        self.de_method_selector.addItem("Euler", "euler")
        self.de_method_selector.addItem("Heun", "heun")
        self.de_method_selector.addItem("RK4", "rk4")
        self.de_method_selector.addItem("Taylor 2° orden", "taylor")
        self.de_method_selector.setFixedWidth(180)
        method_row.addWidget(self.de_method_selector)
        method_row.addStretch()
        main_layout.addLayout(method_row)
        
        # Fila 2: Todo en un solo QHBoxLayout
        second_row = QHBoxLayout()
        second_row.setContentsMargins(10, 0, 0, 0)
        second_row.setSpacing(5)  # Espaciado base entre widgets

        # Condición inicial
        second_row.addWidget(QLabel("📌 y ("))
        self.numerical_x0 = create_float_spinbox(default_val=0)
        self.numerical_x0.setFixedWidth(60)
        second_row.addWidget(self.numerical_x0)
        second_row.addWidget(QLabel(") ="))
        self.numerical_y0 = create_float_spinbox(default_val=1)
        self.numerical_y0.setFixedWidth(60)
        second_row.addWidget(self.numerical_y0)

        # Agregar espacio entre secciones
        second_row.addSpacing(85)

        # Rango
        second_row.addWidget(QLabel("📏 Rango x:"))
        self.numerical_x_start = create_float_spinbox(default_val=0)
        self.numerical_x_start.setFixedWidth(60)
        second_row.addWidget(self.numerical_x_start)
        second_row.addWidget(QLabel("→"))
        self.numerical_x_end = create_float_spinbox(default_val=10)
        self.numerical_x_end.setFixedWidth(60)
        second_row.addWidget(self.numerical_x_end)

        # Agregar espacio entre secciones
        second_row.addSpacing(85)

        # Paso h
        self.step_label = QLabel("👣​ Paso h =")
        second_row.addWidget(self.step_label)
        self.numerical_h = create_float_spinbox(min_val=0.001, max_val=5, default_val=1, step=0.1)
        self.numerical_h.setFixedWidth(60)
        second_row.addWidget(self.numerical_h)

        second_row.addStretch()
        main_layout.addLayout(second_row)
        
        # Conectar señal para mostrar/ocultar parámetros específicos
        self.de_method_selector.currentTextChanged.connect(self.toggle_step)
        
        # Insertar el contenedor en el layout principal
        self.layout.insertWidget(1, method_container)
        
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
        if self.operation_type == "derivative":
            result = self.controller.compute_derivative(expression)
        elif self.operation_type == "integral":
            if hasattr(self, 'integral_type') and self.integral_type.currentData() == "definite":
                # Para integral definida
                limits = (self.lower_limit.value(), self.upper_limit.value())
                result = self.controller.compute_integral(expression, limits)
            else:
                # Para integral indefinida
                result = self.controller.compute_integral(expression)
        elif self.operation_type == "differential_equation":
            x_range = (self.numerical_x_start.value(), self.numerical_x_end.value())
            initial_condition = (self.numerical_x0.value(), self.numerical_y0.value())
            
            method = self.de_method_selector.currentData()
            if method == "analytical":
                result = self.controller.solve_differential_equation(expression, initial_condition=initial_condition, x_range=x_range)
            else:
                # Usar el método numérico correspondiente
                h = self.numerical_h.value()
                method_func = getattr(self.controller, f"solve_ode_{method}", None)
                if method_func:
                    result = method_func(expression, initial_condition, x_range, h)
                else:
                    raise ValueError(f"Método numérico no implementado: {method}")
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
            if self.operation_type in ["derivative", "integral", "differential_equation"]:
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
