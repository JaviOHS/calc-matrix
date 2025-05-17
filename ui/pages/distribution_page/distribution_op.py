from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QHBoxLayout, QSpinBox, QDoubleSpinBox
from ui.widgets.expression_op_widget import ExpressionOpWidget
from utils.spinbox_utils import create_int_spinbox
from controller.distribution_controller import DistributionController
from model.distribution_manager import DistributionManager
from utils.formatting import format_math_expression
from .method_config import METHOD_CONFIG

class DistributionOpWidget(ExpressionOpWidget):
    def __init__(self, manager=DistributionManager, controller=DistributionController, operation_type=None):
        super().__init__(manager, controller, operation_type, input_label="Seleccione el método e ingrese los parámetros:", allow_expression=False)
        self.setup_distribution_inputs()
        self.calculate_button.clicked.connect(self.on_calculate_clicked)

    def setup_distribution_inputs(self):
        parent_layout = self.input_layout if hasattr(self, 'input_layout') else self.layout
        
        # Crear y agregar el selector de método directamente al layout principal
        self.method_selector = self.create_method_selector()
        parent_layout.addWidget(self.method_selector)
    
        self.method_combo.currentIndexChanged.connect(self.update_dynamic_fields) # Conectar la señal para actualizar campos
       
        self.dynamic_fields = {} # Inicializar diccionario para campos dinámicos
        self.update_dynamic_fields() # Inicializar los campos dinámicos (se agregarán directamente al layout principal)

        self.calculate_button.setText("Generar números")

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
        # Determinar el layout correcto para agregar/eliminar widgets
        parent_layout = self.input_layout if hasattr(self, 'input_layout') else self.layout
        
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
        # Usar directamente el ComboBox en lugar del contenedor
        display_name = self.method_combo.currentText()
        for key, config in METHOD_CONFIG.items():
            if config["display_name"] == display_name:
                return key
        return "mersenne" # Valor por defecto

    def perform_operation(self):
        try:
            method = self.get_method_name()
            inputs = {"algorithm": method}
            
            # Recopilar valores de todos los campos dinámicos
            for field_name, widget in self.dynamic_fields.items():
                # Buscar específicamente un QSpinBox o QDoubleSpinBox
                spinbox = widget.findChild(QSpinBox) or widget.findChild(QDoubleSpinBox)
                if spinbox:
                    inputs[field_name] = spinbox.value()
                else:
                    # Alternativa: buscar por posición en el layout (el spinbox suele ser el segundo widget)
                    layout = widget.layout()
                    if layout and layout.count() > 1:
                        spinbox_widget = layout.itemAt(1).widget()
                        if hasattr(spinbox_widget, 'value'):
                            inputs[field_name] = spinbox_widget.value()
            
            # Si es ruido_fisico, agregamos explícitamente seed=None para evitar errores
            if method == "ruido_fisico":
                inputs["seed"] = None

            result = self.controller.execute_operation("generar_numeros", **inputs)

            if result["success"]:
                formatted_output = format_math_expression(
                    expr=inputs,
                    result=result["numbers"],
                    operation_type="distribution",
                    method=method
                )
                return True, formatted_output
            else:
                return False, result["error"]

        except Exception as e:
            return False, str(e)

    def on_calculate_clicked(self):
        success, result = self.perform_operation()
        if success:
            self.display_result(result)
        else:
            error_msg = f"<span style='color: red;'>Error: {result}</span>"
            self.display_result(error_msg)
            