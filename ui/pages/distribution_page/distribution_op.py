from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QHBoxLayout
from ui.widgets.expression_op_widget import ExpressionOpWidget
from controller.distribution_controller import DistributionController
from model.distribution_manager import DistributionManager
from .method_config import METHOD_CONFIG
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
        else:
            input_label = "Seleccione el método e ingrese los parámetros:"
            placeholder = None
            allow_expression = False
            use_dialog_for_result = False
            
        super().__init__(manager, controller, operation_type, input_label=input_label, placeholder=placeholder, allow_expression=allow_expression, use_dialog_for_result=use_dialog_for_result)
        
        # Configurar interfaz según la operación
        if operation_type == "monte_carlo":
            self.setup_monte_carlo_ui()
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
        """Configura la interfaz para integración Monte Carlo"""
        # Método de generación de números aleatorios (primera fila)
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

        # Límites, puntos y semilla (segunda fila)
        params_container = QWidget()
        params_layout = QHBoxLayout(params_container)
        params_layout.setContentsMargins(0, 0, 0, 0)
        
        # Límites de integración
        params_layout.addWidget(QLabel("📌 Límites: x ="))
        self.mc_lower_limit = create_float_spinbox(default_val=0)
        self.mc_lower_limit.setFixedWidth(60)
        params_layout.addWidget(self.mc_lower_limit)
        
        params_layout.addWidget(QLabel("→"))
        self.mc_upper_limit = create_float_spinbox(default_val=1)
        self.mc_upper_limit.setFixedWidth(60)
        params_layout.addWidget(self.mc_upper_limit)
        params_layout.addSpacing(65)
        
        # Número de puntos
        params_layout.addWidget(QLabel("📊 Número de puntos:"))
        self.mc_points = create_int_spinbox(min_val=100, max_val=1000000, default_val=10000, step=1000)
        self.mc_points.setFixedWidth(100)
        params_layout.addWidget(self.mc_points)
        params_layout.addSpacing(65)
        
        # Semilla
        params_layout.addWidget(QLabel("🔑 Semilla:"))
        self.mc_seed = create_int_spinbox(min_val=0, max_val=999999, default_val=42)
        self.mc_seed.setFixedWidth(100)
        params_layout.addWidget(self.mc_seed)
        params_layout.addSpacing(65)
        
        params_layout.addStretch()
        self.input_layout.addWidget(params_container)
        
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
        # Determinar qué operación realizar basada en operation_type
        if self.operation_type == "monte_carlo":
            return self.perform_monte_carlo_integration()
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
            # Recopilar datos de la interfaz
            expression = self.get_input_expression().strip()
                
            a = self.mc_lower_limit.value()
            b = self.mc_upper_limit.value()
            
            if a >= b:
                return False, "El límite inferior debe ser menor que el superior."
                
            n_points = self.mc_points.value()
            algorithm = self.mc_method_combo.currentData()
            seed = self.mc_seed.value()
            
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
                # Devolver el HTML en un diccionario junto con la indicación de no mostrar imagen
                return True, {"html": formatted_output, "canvas": None}
            else:
                return False, result.get("error", "Error desconocido.")
                
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

    def process_operation_result(self, result):
        """Sobrescribir el método para manejar el caso especial de Monte Carlo"""
        try:
            if self.operation_type == "monte_carlo" and isinstance(result, dict) and "html" in result:
                html_content = result.get("html")
                canvas = result.get("canvas")
                image_path = result.get("image_path")  # Puede ser None para no mostrar imagen
                
                if self.use_dialog_for_result:
                    self.canvas_dialog_manager.show_result_dialog(
                        html_content=html_content, 
                        canvas=canvas,
                        image_path=image_path
                    )
                else:
                    # Para el caso estándar, mostrar resultado en el widget
                    self.display_result(html_content)
                    if canvas:
                        self.show_canvas_dialog(canvas)
                return  # Salir del método si ya manejamos el caso especial
            
            # Para otros casos, llamar al método original
            super().process_operation_result(result)
        except Exception as e:
            error_html = f"<div style='color: #D32F2F;'>❌ Error al procesar el resultado: {str(e)}</div>"
            if self.use_dialog_for_result:
                self.show_result_in_dialog(error_html)
            else:
                self.display_result(error_html)
