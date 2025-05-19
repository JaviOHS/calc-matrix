from PySide6.QtWidgets import (QSpinBox, QDoubleSpinBox, QWidget, QLabel, 
                               QHBoxLayout, QVBoxLayout, QFrame, QGroupBox)
from ..dis_base import DistributionBaseOpWidget
from ..method_config import METHOD_CONFIG, TRANSFORM_CONFIG
from utils.formating.formatting import format_math_expression
class RandomOperation(DistributionBaseOpWidget):
    """Clase para las operaciones de generación de números aleatorios y transformación de distribuciones"""
    
    def __init__(self, parent_widget):
        """
        Inicializa la operación de generación de números aleatorios
        
        Args:
            parent_widget: El widget padre que contiene esta operación
        """
        self.parent = parent_widget
        self.dynamic_fields = {}
        self.transform_fields = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz para generación de números aleatorios y transformación"""
        # Crear contenedor principal con dos columnas
        main_container = QWidget()
        main_layout = QHBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # ===== COLUMNA 1: GENERACIÓN DE NÚMEROS =====
        generation_group = QGroupBox("Generación de números aleatorios")
        generation_layout = QVBoxLayout(generation_group)
        
        # Selector de método de generación
        method_container, self.method_combo = self.create_method_selector(METHOD_CONFIG, label_text="🎲 Método:")
        generation_layout.addWidget(method_container)
        
        # Contenedor para los campos dinámicos de generación
        self.generation_fields_container = QWidget()
        self.generation_fields_layout = QVBoxLayout(self.generation_fields_container)
        self.generation_fields_layout.setContentsMargins(0, 0, 0, 0)
        generation_layout.addWidget(self.generation_fields_container)
        
        generation_layout.addStretch()
        main_layout.addWidget(generation_group)
        
        # Separador visual
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        # ===== COLUMNA 2: TRANSFORMACIÓN =====
        transform_group = QGroupBox("Transformación de distribución")
        transform_layout = QVBoxLayout(transform_group)
        
        # Selector de método de transformación
        transform_method_container, self.transform_combo = self.create_method_selector(
            TRANSFORM_CONFIG, 
            default_key="normal", 
            label_text="🔄 Transformar a:"
        )
        transform_layout.addWidget(transform_method_container)
        
        # Contenedor para los campos dinámicos de transformación
        self.transform_fields_container = QWidget()
        self.transform_fields_layout = QVBoxLayout(self.transform_fields_container)
        self.transform_fields_layout.setContentsMargins(0, 0, 0, 0)
        transform_layout.addWidget(self.transform_fields_container)
        
        transform_layout.addStretch()
        main_layout.addWidget(transform_group)
        
        # Añadir el contenedor principal al layout del widget padre
        self.parent.input_layout.addWidget(main_container)
        
        # Conectar eventos
        self.method_combo.currentIndexChanged.connect(self.update_dynamic_fields)
        self.transform_combo.currentIndexChanged.connect(self.update_transform_fields)
        
        # Inicializar campos
        self.update_dynamic_fields()
        self.update_transform_fields()
    
    def update_dynamic_fields(self):
        """Actualiza los campos dinámicos de generación según el método seleccionado"""
        # Limpiar campos existentes
        self.clear_layout(self.generation_fields_layout)
        self.dynamic_fields.clear()

        # Obtener el método seleccionado
        method = self.get_method_name()
        
        # Crear campos según la configuración
        for field in METHOD_CONFIG[method]["fields"]:
            container = self.create_spinbox(
                field["label"],
                field["default"],
                field["min"],
                field["max"]
            )
            self.generation_fields_layout.addWidget(container)
            
            # Guardar referencia al widget para acceder a los valores después
            spinbox = container.findChild(QSpinBox) or container.findChild(QDoubleSpinBox)
            if spinbox:
                self.dynamic_fields[field["name"]] = spinbox
    
    def update_transform_fields(self):
        """Actualiza los campos dinámicos de transformación según la distribución seleccionada"""
        # Limpiar campos existentes
        self.clear_layout(self.transform_fields_layout)
        self.transform_fields.clear()
        
        # Obtener la distribución seleccionada
        distribution_type = self.get_transform_name()
        
        # Crear campos según la configuración de la distribución
        for field in TRANSFORM_CONFIG[distribution_type]["fields"]:
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            
            # Crear etiqueta
            label = QLabel(field["label"])
            layout.addWidget(label)
            
            # Crear el spinbox (entero o flotante según el tipo)
            if field["type"] == "float":
                spinbox = QDoubleSpinBox()
                spinbox.setDecimals(field.get("decimals", 2))
                spinbox.setSingleStep(field.get("step", 0.1))
            else:
                spinbox = QSpinBox()
                spinbox.setSingleStep(field.get("step", 1))
            
            # Configurar propiedades comunes
            spinbox.setMinimum(field["min"])
            spinbox.setMaximum(field["max"])
            spinbox.setValue(field["default"])
            if "width" in field:
                spinbox.setFixedWidth(field["width"])
            
            layout.addWidget(spinbox)
            layout.addStretch()
            
            # Almacenar el spinbox y añadirlo al layout
            self.transform_fields[field["name"]] = spinbox
            self.transform_fields_layout.addWidget(container)
    
    def clear_layout(self, layout):
        """Elimina todos los widgets de un layout"""
        if layout is None:
            return
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
    
    def get_method_name(self):
        """Obtiene el nombre del método seleccionado"""
        return self.get_method_by_name(self.method_combo, METHOD_CONFIG)
    
    def get_transform_name(self):
        """Obtiene el nombre de la transformación seleccionada"""
        return self.get_method_by_name(self.transform_combo, TRANSFORM_CONFIG)
    
    def perform_operation(self, controller):
        """Ejecuta la operación de generación de números aleatorios y su transformación"""
        try:
            # 1. Configurar parámetros para generar números aleatorios
            method = self.get_method_name()
            distribution_type = self.get_transform_name()
            
            inputs = {"algorithm": method}
            
            # Recopilar valores de campos de generación
            for field_name, spinbox in self.dynamic_fields.items():
                inputs[field_name] = spinbox.value()
            
            # Si es ruido_fisico, agregamos explícitamente seed=None para evitar errores
            if method == "ruido_fisico":
                inputs["seed"] = None
            
            # 2. Generar números aleatorios
            gen_result = controller.execute_operation("generar_numeros", **inputs)
            
            if not gen_result.get("success", False):
                return False, gen_result.get("error", "Error desconocido")
            
            # 3. Configurar parámetros para la transformación
            transform_params = {}
            for field_name, spinbox in self.transform_fields.items():
                transform_params[field_name] = spinbox.value()
            
            # 4. Transformar los números generados
            transform_result = controller.execute_operation(
                "transform_distribution",
                numbers=gen_result["numbers"],
                distribution_type=distribution_type,
                **transform_params
            )
            
            if not transform_result.get("success", False):
                return False, transform_result.get("error", "Error en la transformación")
            
            # 5. Preparar datos para format_math_expression
            operation_info = {
                "generation_method": method,
                "transform_method": distribution_type,
                "transform_params": transform_params,
                "seed": inputs.get("seed"),
                "original_numbers": gen_result["numbers"]
            }
            
            # Usar format_math_expression con una operación personalizada
            result_html = format_math_expression(
                expr=operation_info,
                result=transform_result["transformed"],
                operation_type="transform_distribution"
            )
            
            return True, result_html

        except Exception as e:
            return False, str(e)