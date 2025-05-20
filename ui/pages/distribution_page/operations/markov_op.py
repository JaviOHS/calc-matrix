from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QHBoxLayout
from ..distribution_base import DistributionBaseOpWidget
from ..method_config import METHOD_CONFIG, MARKOV_CONFIG
from utils.formating.formatting import format_math_expression
from utils.components.two_column import TwoColumnWidget

class MarkovOperation(DistributionBaseOpWidget):
    """Clase para las operaciones de simulación epidémica de Markov"""
    def __init__(self, parent_widget):
        self.parent = parent_widget
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz para simulación de epidemias usando la configuración"""
        self.parent.title_label.hide()
        two_column_widget = TwoColumnWidget(column1_label="Configuración de población", column2_label="Parámetros de simulación")
        
        # Configurar el selector de método
        markov_method_container = QWidget()
        markov_method_layout = QHBoxLayout(markov_method_container)
        markov_method_layout.setContentsMargins(0, 0, 0, 0)
        
        markov_method_layout.addWidget(QLabel("🟠 Algoritmo aleatorio:"))
        self.markov_method_combo = QComboBox()
        for key, config in METHOD_CONFIG.items():
            self.markov_method_combo.addItem(config["display_name"], key)
        markov_method_layout.addWidget(self.markov_method_combo)
        markov_method_layout.addStretch()

        # Crear contenedores para cada columna
        population_container = self.create_parameter_container(MARKOV_CONFIG["population_params"])
        rates_container = self.create_parameter_container(MARKOV_CONFIG["rate_params"])
        simulation_container = self.create_parameter_container(MARKOV_CONFIG["simulation_params"])

        # Añadir widgets a las columnas
        two_column_widget.add_to_column1(markov_method_container)
        two_column_widget.add_to_column1(population_container)
        two_column_widget.add_to_column1(rates_container)
        two_column_widget.add_to_column2(simulation_container)

        # Añadir el widget de dos columnas al layout principal
        self.parent.input_layout.addWidget(two_column_widget)
        self.parent.input_layout.setContentsMargins(0, 0, 0, 0)

    def perform_operation(self, controller):
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
            result = controller.execute_operation("markov_epidemic", **params)
            
            if result.get("success", False):
                epidemic_data = result.get("result", {})
                formatted_output = format_math_expression(expr=params, result=epidemic_data, operation_type="markov_epidemic")
                return True, {"html": formatted_output, "canvas": epidemic_data.get("canvas"), "image_path": None}
            else:
                return False, result.get("error", "Error desconocido en la simulación")
                
        except Exception as e:
            return False, str(e)