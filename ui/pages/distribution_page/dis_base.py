from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QHBoxLayout
from ui.widgets.expression_op_widget import ExpressionOpWidget
from utils.spinbox_utils import create_int_spinbox, create_float_spinbox

class DistributionBaseOpWidget:
    """Clase base para operaciones de distribución"""
    
    def create_method_selector(self, config_dict, default_key="mersenne", label_text="🟠 Método:"):
        method_container = QWidget()
        method_layout = QHBoxLayout(method_container)
        method_layout.setContentsMargins(0, 0, 0, 0)

        method_label = QLabel(label_text)
        method_combo = QComboBox()
        
        # Usar la configuración para poblar el selector
        method_combo.addItems([config["display_name"] for config in config_dict.values()])
        method_combo.setCurrentText(config_dict[default_key]["display_name"])

        method_layout.addWidget(method_label)
        method_layout.addWidget(method_combo)
        method_layout.addStretch()

        return method_container, method_combo
    
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
    
    def get_method_by_name(self, method_combo, config_dict):
        """Obtiene el nombre clave del método seleccionado en un combo box"""
        display_name = method_combo.currentText()
        for key, config in config_dict.items():
            if config["display_name"] == display_name:
                return key
        return next(iter(config_dict.keys()))  # Valor por defecto (primera clave)