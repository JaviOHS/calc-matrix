from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QTextEdit, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from ui.widgets.math_operation_widget import MathOperationWidget
from ui.widgets.expression_components.expression_buttons_panel import ExpressionButtonsPanel
from ui.widgets.expression_components.expression_formatter_input import ExpressionFormatterInput
from ui.dialogs.dialog_factory import DialogFactory
from utils.components.image_utils import create_image_label

class ExpressionOpWidget(MathOperationWidget):
    def __init__(self, manager, controller, operation_type=None, placeholder="", input_label="", image_path="assets/images/placeholder.png", allow_expression: bool = True, use_dialog_for_result: bool = False):
        super().__init__(manager, controller, operation_type)
        self.operation_type = operation_type
        self.placeholder = placeholder
        self.input_label_text = input_label
        self.image_path = image_path
        self.allow_expression = allow_expression
        self.use_dialog_for_result = use_dialog_for_result
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario para el widget de expresiones matemáticas"""
        self.layout = QVBoxLayout()
        self.layout.setSpacing(12)
        self.layout.setContentsMargins(20, 15, 20, 15)

        # Input section
        input_section = QWidget()
        input_layout = QVBoxLayout(input_section)
        input_layout.setSpacing(8)
        input_layout.setContentsMargins(20, 0, 20, 0)

        self.input_layout = input_layout
        self.input_section = input_section

        # Solo mostrar title_label si no estamos usando TwoColumnWidget
        self.title_label = QLabel(self.input_label_text)
        self.title_label.setObjectName("expressionLabel")
        input_layout.addWidget(self.title_label)
        
        # Solo agregar el QTextEdit de expresión si allow_expression es True
        if self.allow_expression:
            self.expression_input = QTextEdit()
            self.expression_input.setObjectName("expressionInput")
            self.expression_input.setPlaceholderText(self.placeholder)
            self.expression_input.setMaximumHeight(150)
            input_layout.addWidget(self.expression_input)

            self.expression_formatter = ExpressionFormatterInput(self.expression_input)
        
        # Solo agregar contenedor de resultado si use_dialog_for_result es False
        if not self.use_dialog_for_result:
            self.result_container = self._create_result_container()
            input_layout.addWidget(self.result_container)

        self.layout.addWidget(input_section)

        controls = QWidget()
        controls_layout = QHBoxLayout(controls)
        controls_layout.setContentsMargins(0, 5, 0, 0)
        controls_layout.setSpacing(20)

        # Solo agregar el panel de botones de expresión si allow_expression es True
        if self.allow_expression:
            expression_buttons = ExpressionButtonsPanel(self.expression_input)
            controls_layout.addWidget(expression_buttons, alignment=Qt.AlignLeft)

        action_buttons = self.create_buttons()
        action_buttons.setObjectName("actionButtons") 
        controls_layout.addWidget(action_buttons, alignment=Qt.AlignRight)

        self.layout.addWidget(controls)
        self.layout.addStretch() # Fuerza que todo lo demás se mantenga arriba
        self.setLayout(self.layout)

    def _create_result_container(self):
        """Crea el contenedor de resultado que puede ser reusado por clases derivadas"""
        result_section = QWidget()
        result_section.setObjectName("resultSection")
        result_section.setMaximumHeight(150)
        result_layout = QHBoxLayout(result_section)
        result_layout.setContentsMargins(4, 4, 4, 4)
        result_layout.setSpacing(8)
        
        self.result_display = QTextEdit()
        self.result_display.setObjectName("resultDisplay")
        self.result_display.setReadOnly(True)
        self.result_display.setFrameStyle(QTextEdit.NoFrame)
        self.result_display.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.result_display.document().setDocumentMargin(5)
        self.result_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.result_display.setText("⭐ Aquí se mostrará la solución")
        result_layout.addWidget(self.result_display)

        if self.image_path:
            self.preview_image = create_image_label(self.image_path, height=80)
            self.preview_image.setObjectName("previewImage")
            result_layout.addWidget(self.preview_image, alignment=Qt.AlignRight)
            
        return result_section

    def detach_result_container(self):
        """Desprende el contenedor de resultado de su posición actual y lo devuelve"""
        if hasattr(self, 'result_container') and self.result_container:
            parent_layout = self.result_container.parent().layout()
            if parent_layout:
                parent_layout.removeWidget(self.result_container)
            return self.result_container
        return None

    def get_input_expression(self):
        if hasattr(self, 'expression_input'):
            return self.expression_input.toPlainText().strip()
        return ""

    def display_result(self, html):
        if not self.use_dialog_for_result and hasattr(self, 'result_display'):
            self.result_display.setText(html)

    def process_operation_result(self, result):
        """Procesa el resultado de la operación para mostrarlo adecuadamente"""
        try:
            params = self._get_operation_params() # Crear un diccionario con parámetros adicionales según el tipo de operación
            
            # Usar la fábrica de diálogos para mostrar el resultado apropiado
            if self.use_dialog_for_result:
                DialogFactory.show_result_dialog(result=result, operation_type=self.operation_type,parent=self,**params)
            else:
                # Si no usamos diálogo, mostrar en el widget interno
                if isinstance(result, dict) and "html" in result:
                    self.display_result(result["html"])
                    
                    # Si hay canvas, mostrarlo en un diálogo aparte
                    if "canvas" in result and result["canvas"]:
                        DialogFactory.show_canvas_dialog(canvas=result["canvas"],operation_type=self.operation_type,parent=self,**params)
                else:
                    self.display_result(result) # El resultado es directamente HTML

        except Exception as e:
            error_html = f"<div style='color: #D32F2F;'>❌ Error al procesar el resultado: {str(e)}</div>"
            if self.use_dialog_for_result:
                DialogFactory.show_message_dialog(title="❌ ERROR",message=error_html,title_color="#d32f2f",image_name="error.png",parent=self)
            else:
                self.display_result(error_html)
    
    def _get_operation_params(self):
        """Obtiene parámetros adicionales según el tipo de operación"""
        params = {}
        
        # Parámetros para ecuaciones diferenciales
        if self.operation_type == "differential_equation":
            # Verificar si tenemos los atributos necesarios
            if all(hasattr(self, attr) for attr in ['numerical_x_start', 'numerical_x_end', 'numerical_x0', 'numerical_y0', 'de_method_selector']):
                params.update({
                    "equation": self.get_input_expression().strip(),
                    "x_range": (self.numerical_x_start.spinbox.value(), self.numerical_x_end.spinbox.value()),
                    "initial_condition": (self.numerical_x0.spinbox.value(), self.numerical_y0.spinbox.value()),
                    "method": self.de_method_selector.currentData(),
                    "h": self.numerical_h.spinbox.value() if hasattr(self, 'numerical_h') else 0.1,
                    "sym_model": self.controller.manager.model if hasattr(self.controller, 'manager') else None
                })
        
        return params
