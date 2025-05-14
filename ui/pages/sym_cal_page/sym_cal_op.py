from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget, QComboBox, QVBoxLayout
from ui.widgets.expression_op_widget import ExpressionOpWidget
from utils.formatting import format_math_expression
from utils.spinbox_utils import create_spinbox
from utils.create_range_row import create_range_row

class SymCalOpWidget(ExpressionOpWidget):
    def __init__(self, manager, controller, operation_type=None):
        self.manager = manager
        self.controller = controller
        self.operation_type = operation_type
        use_dialog_for_result = True if operation_type == "ecuaciones_diferenciales" else False

        input_label = f"Ingresa una expresión para realizar cálculo de {operation_type.replace("_", " ")}:"
        placeholder = "Ejemplo: 2x^2 + 2x"
        
        if operation_type == "ecuaciones_diferenciales":
            placeholder = "Ejemplos válidos: \ny' = x + y || dy/dx = x + y"
        super().__init__(manager, controller, operation_type=operation_type, placeholder=placeholder, input_label=input_label, use_dialog_for_result=use_dialog_for_result)

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
        # Contenedor principal horizontal
        top_row = QWidget()
        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(24, 0, 12, 0)
        top_layout.setSpacing(5)

        # Etiqueta de tipo de integral
        instruction_label = QLabel("Tipo de integral:")
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
        limits_layout.setSpacing(5)

        limits_layout.addWidget(QLabel("📌 Límites: x ="))
        self.lower_limit = create_spinbox(default_val=0)
        self.lower_limit.setFixedWidth(60)
        limits_layout.addWidget(self.lower_limit)

        limits_layout.addWidget(QLabel("→"))
        self.upper_limit = create_spinbox(default_val=1)
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
        # Contenedor principal para todos los elementos
        method_container = QWidget()

        main_layout = QVBoxLayout(method_container)
        main_layout.setContentsMargins(20, 0, 20, 0)
        main_layout.setSpacing(5)  # Reducido de 10 a 5
        
        # Selector de método (fila 1)
        method_row = QHBoxLayout()
        method_row.setContentsMargins(0, 0, 0, 0)
        method_row.addWidget(QLabel("Seleccione el método a utilizar:"))
        
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
        
        # Fila 2: Condición inicial + Rango + Paso h
        second_row = QHBoxLayout()
        second_row.setContentsMargins(0, 0, 0, 0)
        second_row.setSpacing(15)  # Ajusta el espacio entre los grupos principales

        # Condición inicial
        initial_layout = QHBoxLayout()
        initial_layout.setSpacing(2)  # Reducido el espacio entre elementos
        initial_layout.addWidget(QLabel("🟠​ y ("))
        self.numerical_x0 = create_spinbox(default_val=0)
        initial_layout.addWidget(self.numerical_x0)
        initial_layout.addWidget(QLabel(") ="))
        self.numerical_y0 = create_spinbox(default_val=1)
        initial_layout.addWidget(self.numerical_y0)
        initial_widget = QWidget()
        initial_widget.setLayout(initial_layout)
        second_row.addWidget(initial_widget)

        # Rango
        range_layout, self.numerical_x_start, self.numerical_x_end = create_range_row(
            label_text="📌 Rango x", 
            min_label="", 
            max_label="", 
            default_min=0, 
            default_max=10,
            spacing=2  # Reducido el espaciado
        )
        range_widget = QWidget()
        range_widget.setLayout(range_layout)
        second_row.addWidget(range_widget)

        # Paso h
        step_layout = QHBoxLayout()
        step_layout.setSpacing(2)  # Reducido el espacio entre elementos
        step_layout.addWidget(QLabel("👣​ Paso h ="))
        self.numerical_h = create_spinbox(min_val=0.001, max_val=5, default_val=1, step=0.1)
        step_layout.addWidget(self.numerical_h)
        self.numerical_step_widget = QWidget()
        self.numerical_step_widget.setLayout(step_layout)
        second_row.addWidget(self.numerical_step_widget)

        # Añadir stretch al final para empujar todo hacia la izquierda
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
        self.numerical_step_widget.setVisible(method in ["Euler", "Heun", "RK4", "Taylor 2° orden"])
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
