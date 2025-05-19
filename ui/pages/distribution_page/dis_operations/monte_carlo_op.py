from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QHBoxLayout, QLabel, QComboBox
from ..dis_base import DistributionBaseOpWidget
from ..method_config import METHOD_CONFIG, MONTE_CARLO_CONFIG
from utils.formating.formatting import format_math_expression

class MonteCarloOp(DistributionBaseOpWidget):
    """Clase para las operaciones de integración Monte Carlo"""
    
    def __init__(self, parent_widget):
        """
        Inicializa la operación de integración Monte Carlo
        
        Args:
            parent_widget: El widget padre que contiene esta operación
        """
        self.parent = parent_widget
        self.setup_ui()
        
    def setup_ui(self):
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
        self.parent.input_layout.addWidget(mc_method_container)

        # Parámetros de Monte Carlo
        params_container = self.create_parameter_container(MONTE_CARLO_CONFIG["fields"])
        self.parent.input_layout.addWidget(params_container)
    
    def perform_operation(self, controller):
        """Ejecuta la operación de integración Monte Carlo"""
        try:
            # Recopilar datos de la interfaz usando el sufijo _spinbox
            expression = self.parent.get_input_expression().strip()
                
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
            result = controller.execute_operation("monte_carlo_integration", **params)
                
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