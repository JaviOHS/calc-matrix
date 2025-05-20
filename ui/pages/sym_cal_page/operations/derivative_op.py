from .base_operation import BaseSymCalOperation
from PySide6.QtWidgets import QWidget
from utils.components.two_column import TwoColumnWidget

class DerivativeOperation(BaseSymCalOperation):
    def __init__(self, manager, controller):
        super().__init__(manager=manager, controller=controller, operation_type="derivative", placeholder="Ejemplo: 2x^2 + 2x", input_label="Ingrese expresión")
        self.setup_two_column_layout()
    
    def setup_two_column_layout(self):
        """Configura una interfaz de dos columnas simple con expresión y resultado"""
        self.title_label.hide()
        result_container = self.detach_result_container() # Obtener el contenedor de resultado existente desde la clase base
        
        two_column_widget = TwoColumnWidget(column1_label=self.input_label_text, column2_label="Resultado",)
        two_column_widget.add_to_column1(self.expression_input)
        two_column_widget.add_to_column2(result_container)

        self.layout.insertWidget(1, two_column_widget)
    
    def execute_operation(self):
        expression = self.get_input_expression().strip()
        return self.controller.compute_derivative(expression)