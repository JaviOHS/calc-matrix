from PySide6.QtWidgets import QWidget, QTextEdit, QHBoxLayout, QLabel, QComboBox, QVBoxLayout
from ..distribution_base import DistributionBaseOpWidget
from ..method_config import TRANSFORM_CONFIG
from utils.formating.formatting import format_math_expression
from utils.components.two_column import TwoColumnWidget

class TransformOp(DistributionBaseOpWidget):
    """Clase para las operaciones de transformación de distribuciones"""
    def __init__(self, parent_widget):
        self.parent = parent_widget
        self.parameters_fields = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz para transformación de distribuciones"""
        self.parent.title_label.hide()

        two_column_widget = TwoColumnWidget(
            column1_label=self.parent.input_label_text,
            column2_label="Configuración de distribución"
        )
        self.parent.input_layout.setContentsMargins(0, 0, 0, 0)
        two_column_widget.add_to_column1(self.parent.expression_input)

        # Configurar el selector de distribución en la segunda columna
        distribution_method_container = QWidget()
        distribution_method_layout = QHBoxLayout(distribution_method_container)
        distribution_method_layout.setContentsMargins(0, 0, 0, 0)
        distribution_method_layout.addWidget(QLabel("🎯 Tipo de distribución:"))
        self.distribution_combo = QComboBox()
        for key, config in TRANSFORM_CONFIG.items():
            self.distribution_combo.addItem(config["display_name"], key)
        
        # Conectar el cambio de selección para actualizar parámetros dinámicamente
        self.distribution_combo.currentTextChanged.connect(self.update_parameters)
        distribution_method_layout.addWidget(self.distribution_combo)
        distribution_method_layout.addStretch()

        two_column_widget.add_to_column2(distribution_method_container)
        
        # Crear contenedor para parámetros dinámicos
        self.parameters_container = QWidget()
        self.parameters_layout = QVBoxLayout(self.parameters_container)
        self.parameters_layout.setContentsMargins(0, 0, 0, 0)
        self.parameters_layout.setSpacing(5)
        
        two_column_widget.add_to_column2(self.parameters_container)
        
        # Inicializar con los parámetros de la primera distribución
        self.update_parameters()

        # Añadir el widget de dos columnas al layout principal
        self.parent.input_layout.addWidget(two_column_widget)
        self.parent.input_layout.setContentsMargins(0, 0, 0, 0)

    def update_parameters(self):
        """Actualiza los parámetros dinámicos según la distribución seleccionada"""
        # Limpiar campos existentes
        self.clear_layout(self.parameters_layout)
        self.parameters_fields.clear()
        
        # Obtener la distribución seleccionada
        distribution_type = self.get_distribution_name()
        
        # Crear campos según la configuración de la distribución
        for field in TRANSFORM_CONFIG[distribution_type]["fields"]:
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            
            # Etiqueta
            label = QLabel(field["label"])
            layout.addWidget(label)
            
            # Crear el spinbox según el tipo
            if field["type"] == "float":
                from utils.components.spinbox_utils import create_float_spinbox
                spinbox_container = create_float_spinbox(
                    min_val=field["min"],
                    max_val=field["max"],
                    default_val=field["default"],
                    step=field.get("step", 0.1),
                    decimals=field.get("decimals", 2),
                    width=field.get("width", 80)
                )
            else:
                from utils.components.spinbox_utils import create_int_spinbox
                spinbox_container = create_int_spinbox(
                    min_val=field["min"],
                    max_val=field["max"],
                    default_val=field["default"],
                    step=field.get("step", 1),
                    width=field.get("width", 80)
                )
            
            # Extraer el spinbox real y añadir el contenedor al layout
            spinbox = spinbox_container.spinbox
            layout.addWidget(spinbox_container)
            layout.addStretch()
            
            # Guardar el spinbox real
            self.parameters_fields[field["name"]] = spinbox
            self.parameters_layout.addWidget(container)
        
        # Añadir stretch al final para compactar los elementos
        self.parameters_layout.addStretch()

    def clear_layout(self, layout):
        """Elimina todos los widgets de un layout"""
        if layout is None:
            return
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def get_distribution_name(self):
        """Obtiene el nombre de la distribución seleccionada"""
        return self.get_method_by_name(self.distribution_combo, TRANSFORM_CONFIG)

    def perform_operation(self, controller):
        """Ejecuta la operación de transformación de distribución"""
        try:
            # 1. Obtener los números uniformes del input del usuario
            uniform_numbers_input = self.parent.get_input_expression().strip()
            
            if not uniform_numbers_input:
                return False, "Debe ingresar números uniformes para transformar."
            
            # 2. Obtener el tipo de distribución seleccionada
            distribution_type = self.get_distribution_name()
            
            # 3. Recopilar parámetros de la distribución
            transform_params = {}
            for field_name, spinbox in self.parameters_fields.items():
                transform_params[field_name] = spinbox.value()
            
            # 4. Ejecutar la transformación
            transform_result = controller.execute_operation(
                "transform_distribution",
                uniform_numbers=uniform_numbers_input,
                distribution_type=distribution_type,
                **transform_params
            )
            
            if not transform_result.get("success", False):
                return False, transform_result.get("error", "Error en la transformación...")
            
            # 5. Preparar datos para format_math_expression con estructura correcta
            operation_info = {
                "generation_method": "manual",  # Ya que son números ingresados manualmente
                "transform_method": distribution_type,
                "transform_params": transform_params,
                "original_numbers": transform_result.get("original", [])
            }
            
            # 6. Formatear el resultado usando el operation_type correcto
            result_html = format_math_expression(
                expr=operation_info, 
                result=transform_result.get("transformed", []), 
                operation_type="transform_distribution"
            )
            
            return True, {"html": result_html, "canvas": None}

        except Exception as e:
            return False, str(e)