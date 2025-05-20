from ui.widgets.expression_op_widget import ExpressionOpWidget
from controller.distribution_controller import DistributionController
from model.distribution_manager import DistributionManager
from .operations.random_op import RandomOperation
from .operations.monte_carlo_op import MonteCarloOp
from .operations.markov_op import MarkovOperation

class DistributionOpWidget(ExpressionOpWidget):
    def __init__(self, manager=DistributionManager, controller=DistributionController, operation_type=None):
        self.operation_type = operation_type
        self.operation_handler = None
        
        # Configurar etiqueta según el tipo de operación
        if operation_type == "monte_carlo":
            input_label = "Ingrese expresión para integración de Monte Carlo"
            placeholder = "Ejemplo: x^2 + 3x + 2"
            allow_expression = True
            use_dialog_for_result = True
            button_text = "Calcular"
        elif operation_type == "markov_epidemic":
            input_label = None
            placeholder = None
            allow_expression = False
            use_dialog_for_result = True
            button_text = "Simular"
        else:
            input_label = "Generación de números aleatorios"
            placeholder = None
            allow_expression = False
            use_dialog_for_result = True
            button_text = "Generar"
            
        super().__init__(manager, controller, operation_type, input_label=input_label, placeholder=placeholder, allow_expression=allow_expression, use_dialog_for_result=use_dialog_for_result)
        
        self.calculate_button.setText(button_text)
        self.setup_operation_handler()

    def setup_operation_handler(self):
        """Configura el manejador específico según el tipo de operación"""
        if self.operation_type == "monte_carlo":
            self.operation_handler = MonteCarloOp(self)
        elif self.operation_type == "markov_epidemic":
            self.operation_handler = MarkovOperation(self)
        else:
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
                # Importar el diálogo especializado
                from ui.dialogs.simple.distribution_dialog import DistributionDialog
                
                # Crear y mostrar el diálogo apropiado
                dialog = DistributionDialog(operation_type=self.operation_type,result_data=result,parent=self)
                dialog.exec()
            else:
                # Para otros casos, usar el comportamiento por defecto
                super().process_operation_result(result)
                
        except Exception as e:
            error_html = f"<div style='color: #D32F2F;'>❌ Error al procesar el resultado: {str(e)}</div>"
            if self.use_dialog_for_result:
                self.show_result_in_dialog(error_html)
            else:
                self.display_result(error_html)
                