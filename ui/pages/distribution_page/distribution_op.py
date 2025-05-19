from ui.widgets.expression_op_widget import ExpressionOpWidget
from controller.distribution_controller import DistributionController
from model.distribution_manager import DistributionManager
from .dis_operations.random_op import RandomOperation
from .dis_operations.monte_carlo_op import MonteCarloOp
from .dis_operations.markov_op import MarkovOperation

class DistributionOpWidget(ExpressionOpWidget):
    def __init__(self, manager=DistributionManager, controller=DistributionController, operation_type=None):
        self.operation_type = operation_type
        self.operation_handler = None
        
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
        elif operation_type == "transform_distribution":
            input_label = "Transformación de distribuciones:"
            placeholder = None
            allow_expression = False
            use_dialog_for_result = True
        else:
            input_label = "Seleccione el método e ingrese los parámetros:"
            placeholder = None
            allow_expression = False
            use_dialog_for_result = False
            
        super().__init__(manager, controller, operation_type, input_label=input_label, 
                        placeholder=placeholder, allow_expression=allow_expression, 
                        use_dialog_for_result=use_dialog_for_result)
        
        # Configurar interfaz según la operación
        self.setup_operation_handler()

    def setup_operation_handler(self):
        """Configura el manejador específico según el tipo de operación"""
        if self.operation_type == "monte_carlo":
            self.operation_handler = MonteCarloOp(self)
        elif self.operation_type == "markov_epidemic":
            self.operation_handler = MarkovOperation(self)
        else:
            # Por defecto, generación de números aleatorios
            self.operation_handler = RandomOperation(self)

    def perform_operation(self):
        """Delega la operación al manejador específico"""
        if self.operation_handler:
            return self.operation_handler.perform_operation(self.controller)
        return False, "No se ha configurado un manejador de operación"

    def on_calculate_clicked(self):
        success, result = self.perform_operation()
        if success:
            self.process_operation_result(result)
            return True, "Operación realizada con éxito"
        else:
            error_msg = f"{result}"
            return False, error_msg

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
                    },
                    "transform_distribution": {
                        "title": "🔄 TRANSFORMACIÓN DE DISTRIBUCIÓN",
                        "title_color": "#9C27B0"
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