from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QHBoxLayout
from ui.widgets.expression_op_widget import ExpressionOpWidget
from controller.distribution_controller import DistributionController
from model.distribution_manager import DistributionManager
from .method_config import *
from utils.formatting import format_math_expression
from utils.spinbox_utils import create_int_spinbox, create_float_spinbox

class DistributionOpWidget(ExpressionOpWidget):
    def __init__(self, manager=DistributionManager, controller=DistributionController, operation_type=None):
        self.operation_type = operation_type
        
        # Configurar etiqueta según el tipo de operación
        if operation_type == "monte_carlo":
            input_label = "Ingrese los parámetros para la integración por Monte Carlo:"
            placeholder = "Ejemplo: x^2 + 3x + 2"
            allow_expression = True
            use_dialog_for_result = True
        elif operation_type == "markov_epidemic":
            input_label = "Ingrese los parámetros para la simulación de epidemias:"
            placeholder = None
            allow_expression = False
            use_dialog_for_result = True
        else:
            input_label = "Seleccione el método e ingrese los parámetros:"
            placeholder = None
            allow_expression = False
            use_dialog_for_result = False
            
        super().__init__(manager, controller, operation_type, input_label=input_label, placeholder=placeholder, allow_expression=allow_expression, use_dialog_for_result=use_dialog_for_result)
        
        # Configurar interfaz según la operación
        if operation_type == "monte_carlo":
            self.setup_monte_carlo_ui()
        elif operation_type == "markov_epidemic":
            self.setup_markov_epidemic_ui()
        else:
            self.setup_distribution_ui()

    def setup_distribution_ui(self):
        """Configura la interfaz para generación de números aleatorios"""
        # Configurar los widgets de generación de números
        self.method_selector = self.create_method_selector()
        self.input_layout.addWidget(self.method_selector)
        
        self.dynamic_fields = {}
        self.method_combo.currentIndexChanged.connect(self.update_dynamic_fields)
        self.update_dynamic_fields()  # Inicializar campos

    def setup_monte_carlo_ui(self):
        """Configura la interfaz para integración Monte Carlo usando la configuración"""
        # Método selector
        mc_method_container = QWidget()
        mc_method_layout = QHBoxLayout(mc_method_container)
        mc_method_layout.setContentsMargins(0, 0, 0, 0)
        
        mc_method_layout.addWidget(QLabel("🟠 Algoritmo aleatorio:"))
        self.mc_method_combo = QComboBox()
        for key, config in METHOD_CONFIG.items():
            self.mc_method_combo.addItem(config["display_name"], key)
        mc_method_layout.addWidget(self.mc_method_combo)
        
        mc_method_layout.addStretch()
        self.input_layout.addWidget(mc_method_container)

        # Parámetros de Monte Carlo
        params_container = self.create_parameter_container(MONTE_CARLO_CONFIG["fields"])
        self.input_layout.addWidget(params_container)
        
    def setup_markov_epidemic_ui(self):
        """Configura la interfaz para simulación de epidemias usando la configuración"""
        # Método selector
        markov_method_container = QWidget()
        markov_method_layout = QHBoxLayout(markov_method_container)
        markov_method_layout.setContentsMargins(0, 0, 0, 0)
        
        markov_method_layout.addWidget(QLabel("🟠 Algoritmo aleatorio:"))
        self.markov_method_combo = QComboBox()
        for key, config in METHOD_CONFIG.items():
            self.markov_method_combo.addItem(config["display_name"], key)
        markov_method_layout.addWidget(self.markov_method_combo)
        
        markov_method_layout.addStretch()
        self.input_layout.addWidget(markov_method_container)

        # Parámetros de población
        self.input_layout.addWidget(
            self.create_parameter_container(MARKOV_CONFIG["population_params"])
        )
        
        # Parámetros de tasas
        self.input_layout.addWidget(
            self.create_parameter_container(MARKOV_CONFIG["rate_params"])
        )
        
        # Parámetros de simulación
        self.input_layout.addWidget(
            self.create_parameter_container(MARKOV_CONFIG["simulation_params"])
        )

    def create_method_selector(self):
        method_container = QWidget()
        method_layout = QHBoxLayout(method_container)
        method_layout.setContentsMargins(0, 0, 0, 0)

        method_label = QLabel("🟠 Método:")
        self.method_combo = QComboBox()  # Guarda una referencia al QComboBox
        
        # Usar la configuración para poblar el selector
        self.method_combo.addItems([config["display_name"] for config in METHOD_CONFIG.values()])
        self.method_combo.setCurrentText(METHOD_CONFIG["mersenne"]["display_name"])

        method_layout.addWidget(method_label)
        method_layout.addWidget(self.method_combo)
        method_layout.addStretch()

        return method_container

    def update_dynamic_fields(self):
        # Determinar el layout correcto
        parent_layout = self.input_layout
        
        # Limpiar campos dinámicos existentes
        for widget in self.dynamic_fields.values():
            parent_layout.removeWidget(widget)
            widget.deleteLater()
        self.dynamic_fields.clear()

        # Obtener el método seleccionado
        method = self.get_method_name()
        
        # Crear campos según la configuración
        for field in METHOD_CONFIG[method]["fields"]:
            self.dynamic_fields[field["name"]] = self.create_spinbox(
                field["label"],
                field["default"],
                field["min"],
                field["max"]
            )
            parent_layout.addWidget(self.dynamic_fields[field["name"]])

    def create_spinbox(self, label_text, default_val, min_val, max_val):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(label_text)
        spinbox = create_int_spinbox(default_val=default_val, min_val=min_val, max_val=max_val)

        layout.addWidget(label)
        layout.addWidget(spinbox)
        layout.addStretch()

        return container

    def get_method_name(self):
        # Usar directamente el ComboBox
        display_name = self.method_combo.currentText()
        for key, config in METHOD_CONFIG.items():
            if config["display_name"] == display_name:
                return key
        return "mersenne"  # Valor por defecto

    def perform_operation(self):
        if self.operation_type == "monte_carlo":
            return self.perform_monte_carlo_integration()
        elif self.operation_type == "markov_epidemic":
            return self.perform_markov_epidemic_simulation()
        else:
            return self.perform_random_generation()

    def perform_random_generation(self):
        try:
            method = self.get_method_name()
            inputs = {"algorithm": method}
            
            # Recopilar valores de todos los campos dinámicos
            from PySide6.QtWidgets import QSpinBox, QDoubleSpinBox
            for field_name, widget in self.dynamic_fields.items():
                # Buscar específicamente un QSpinBox o QDoubleSpinBox
                spinbox = widget.findChild(QSpinBox) or widget.findChild(QDoubleSpinBox)
                if spinbox:
                    inputs[field_name] = spinbox.value()
            
            # Si es ruido_fisico, agregamos explícitamente seed=None para evitar errores
            if method == "ruido_fisico":
                inputs["seed"] = None

            result = self.controller.execute_operation("generar_numeros", **inputs)

            if result.get("success", False):
                from utils.formatting import format_math_expression
                formatted_output = format_math_expression(
                    expr=inputs,
                    result=result["numbers"],
                    operation_type="distribution",
                    method=method
                )
                return True, formatted_output
            else:
                return False, result.get("error", "Error desconocido")

        except Exception as e:
            return False, str(e)

    def perform_monte_carlo_integration(self):
        try:
            # Recopilar datos de la interfaz usando el sufijo _spinbox
            expression = self.get_input_expression().strip()
                
            a = self.lower_limit_spinbox.value()
            b = self.upper_limit_spinbox.value()
            
            if a >= b:
                return False, "El límite inferior debe ser menor que el superior."
                
            n_points = self.points_spinbox.value()
            algorithm = self.mc_method_combo.currentData()
            seed = self.seed_spinbox.value()
            
            # Preparar los parámetros para el controlador
            params = {
                "expression": expression,
                "a": a,
                "b": b,
                "n_points": n_points,
                "algorithm": algorithm,
                "seed": seed
            }
            
            # Ejecutar la operación correspondiente
            result = self.controller.execute_operation("monte_carlo_integration", **params)
                
            # Procesar el resultado
            if result.get("success", False):
                formatted_output = format_math_expression(
                    expr=expression,
                    result=result,
                    operation_type="monte_carlo",
                    method="integration"
                )
                return True, {
                    "html": formatted_output,
                    "canvas": None  # Asegurar que no se envía canvas
                }
            else:
                return False, result.get("error", "Error desconocido.")
            
        except Exception as e:
            return False, str(e)

    def perform_markov_epidemic_simulation(self):
        """Ejecuta la simulación del modelo de Markov para epidemias"""
        try:
            # Recopilar parámetros de la interfaz usando el sufijo _spinbox
            params = {
                "population": self.population_spinbox.value(),
                "initial_infected": self.initial_infected_spinbox.value(),
                "initial_recovered": self.initial_recovered_spinbox.value(),
                "beta": self.beta_spinbox.value(),
                "gamma": self.gamma_spinbox.value(),
                "days": self.days_spinbox.value(),
                "dt": self.dt_spinbox.value(),
                "algorithm": self.markov_method_combo.currentData(),
                "seed": self.seed_spinbox.value()
            }
            
            # Ejecutar simulación a través del controlador
            result = self.controller.execute_operation("markov_epidemic", **params)
            
            if result.get("success", False):
                epidemic_data = result.get("result", {})
                
                # Usar el formateador para generar el HTML
                formatted_output = format_math_expression(
                    expr=params,
                    result=epidemic_data,
                    operation_type="markov_epidemic"
                )
                
                return True, {
                    "html": formatted_output,
                    "canvas": epidemic_data.get("canvas"),
                    "image_path": None
                }
            else:
                return False, result.get("error", "Error desconocido en la simulación")
                
        except Exception as e:
            return False, str(e)

    def on_calculate_clicked(self):
        success, result = self.perform_operation()
        if success:
            self.process_operation_result(result)
            return True, "Operación realizada con éxito"
        else:
            error_msg = f"{result}"
            return False, error_msg
        
    def create_parameter_container(self, fields, spacing=20):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        for field in fields:
            layout.addWidget(QLabel(field["label"]))
            
            if field["type"] == "float":
                spinbox = create_float_spinbox(
                    min_val=field["min"],
                    max_val=field["max"],
                    default_val=field["default"],
                    step=field.get("step", 0.1),
                    decimals=field.get("decimals", 2),
                    width=field["width"]
                )
            else:  # int
                spinbox = create_int_spinbox(
                    min_val=field["min"],
                    max_val=field["max"],
                    default_val=field["default"],
                    step=field.get("step", 1),
                    width=field["width"]
                )
                
            setattr(self, f"{field['name']}_spinbox", spinbox)
            layout.addWidget(spinbox)
            
            if spacing:
                layout.addSpacing(spacing)
                
        layout.addStretch()
        return container

    def process_operation_result(self, result):
        """Procesa el resultado de la operación para mostrar en el diálogo"""
        try:
            if isinstance(result, dict) and "html" in result:
                html_content = result.get("html")
                canvas = result.get("canvas")
                
                dialog_config = {
                    "markov_epidemic": {
                        "title": "🦠 SIMULACIÓN DE EPIDEMIA",
                        "title_color": "#ff8103"
                    },
                    "monte_carlo": {
                        "title": "📊 INTEGRACIÓN MONTE CARLO",
                        "title_color": "#2196F3"
                    }
                }
                
                # Obtener la configuración específica para el tipo de operación
                config = dialog_config.get(self.operation_type, {})
                
                self.canvas_dialog_manager.show_result_dialog(
                    html_content=html_content,
                    canvas=canvas,
                    title=config.get("title"),
                    title_color=config.get("title_color"),
                    image_path=None  # Forzar None para no mostrar imagen
                )
                return
            
            # Para otros casos, usar el comportamiento por defecto
            super().process_operation_result(result)
            
        except Exception as e:
            error_html = f"<div style='color: #D32F2F;'>❌ Error al procesar el resultado: {str(e)}</div>"
            if self.use_dialog_for_result:
                self.show_result_in_dialog(error_html)
            else:
                self.display_result(error_html)
