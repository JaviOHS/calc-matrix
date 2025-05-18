from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QTextEdit, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from ui.widgets.math_operation_widget import MathOperationWidget
from ui.widgets.expression_components.expression_buttons_panel import ExpressionButtonsPanel
from ui.widgets.expression_components.expression_formatter_input import ExpressionFormatterInput
from ui.dialogs.canvas_dialog_manager import CanvasDialogManager
from utils.image_utils import create_image_label

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

        self.input_layout = input_layout # Guardar la referencia al layout de entrada

        # Label más sutil
        title_label = QLabel(self.input_label_text)
        title_label.setObjectName("expressionLabel")
        input_layout.addWidget(title_label)

        # Inicializar canvas_dialog_manager siempre, independientemente de allow_expression
        self.canvas_dialog_manager = CanvasDialogManager(self)

        # Solo agregar el QTextEdit de expresión si allow_expression es True
        if self.allow_expression:
            self.expression_input = QTextEdit()
            self.expression_input.setObjectName("expressionInput")
            self.expression_input.setPlaceholderText(self.placeholder)
            self.expression_input.setMaximumHeight(90)
            input_layout.addWidget(self.expression_input)

            self.expression_formatter = ExpressionFormatterInput(self.expression_input)
        
        # Result section (if needed)
        if not self.use_dialog_for_result:
            result_section = QWidget()
            result_section.setObjectName("resultSection")
            result_layout = QHBoxLayout(result_section)
            result_layout.setContentsMargins(8, 4, 8, 4)
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

            input_layout.addWidget(result_section)

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
        
    def get_input_expression(self):
        if hasattr(self, 'expression_input'):
            return self.expression_input.toPlainText().strip()
        return ""

    def display_result(self, html):
        if not self.use_dialog_for_result and hasattr(self, 'result_display'):
            self.result_display.setText(html)

    def show_canvas_dialog(self, canvas):
        self.canvas_dialog_manager.show_canvas_dialog(canvas)

    def show_result_in_dialog(self, html_content, canvas=None):
        """Muestra el resultado en un diálogo, combinando HTML y canvas si está disponible"""
        self.canvas_dialog_manager.show_result_dialog(html_content, canvas)

    def process_operation_result(self, result):
        """Procesa el resultado de la operación para mostrarlo adecuadamente"""
        try:
            # CASO ESPECIAL: Ecuaciones diferenciales con capacidad de comparación
            if self.operation_type == "ecuaciones_diferenciales" and isinstance(result, dict) and "canvas" in result:
                # Verificar si tenemos los atributos necesarios para la comparación
                if all(hasattr(self, attr) for attr in ['numerical_x_start', 'numerical_x_end', 'numerical_x0', 'numerical_y0', 'de_method_selector']):
                    # Extraer HTML y canvas
                    html_content = result.get("html")
                    canvas = result["canvas"]
                    
                    # Obtener parámetros para el diálogo especializado
                    equation = self.get_input_expression().strip()
                    x_range = (self.numerical_x_start.value(), self.numerical_x_end.value())
                    initial_condition = (self.numerical_x0.value(), self.numerical_y0.value())
                    method = self.de_method_selector.currentData()
                    h = self.numerical_h.value() if hasattr(self, 'numerical_h') else 0.1
                    
                    # Obtener modelo simbólico si está disponible
                    sym_model = self.controller.manager.model if hasattr(self.controller, 'manager') else None
                    
                    # Mostrar diálogo especializado con opción de comparación Y el HTML
                    if self.use_dialog_for_result:
                        self.canvas_dialog_manager.show_ode_solution_dialog(
                            canvas=canvas,
                            equation=equation,
                            initial_condition=initial_condition,
                            x_range=x_range,
                            h=h,
                            method=method,
                            sym_model=sym_model,
                            title="🟢 SOLUCIÓN DE EDO",
                            html_content=html_content  # Pasar el HTML para mostrarlo
                        )
                    else:
                        # Mostrar HTML en el widget y canvas en diálogo separado
                        self.display_result(html_content)
                        self.canvas_dialog_manager.show_ode_solution_dialog(
                            canvas=canvas,
                            equation=equation,
                            initial_condition=initial_condition,
                            x_range=x_range,
                            h=h,
                            method=method,
                            sym_model=sym_model,
                            title="🟢 SOLUCIÓN DE EDO"
                        )
                    return  # Importante: terminar aquí si ya manejamos el caso
            
            # COMPORTAMIENTO ESTÁNDAR PARA EL RESTO DE CASOS
            html_content = None
            canvas = None
            
            if isinstance(result, dict) and "html" in result:
                html_content = result.get("html")
                canvas = result.get("canvas")
                
                if self.use_dialog_for_result:
                    self.show_result_in_dialog(html_content, canvas)
                else:
                    # Solo mostrar el HTML en el widget de resultado
                    self.display_result(html_content)
                    
                    # Si hay un canvas pero no estamos usando diálogo, mostrar canvas por separado
                    if canvas:
                        self.show_canvas_dialog(canvas)
            else:
                # El resultado es directamente HTML (comportamiento anterior)
                if self.use_dialog_for_result:
                    self.show_result_in_dialog(result)
                else:
                    self.display_result(result)
        except Exception as e:
            error_html = f"<div style='color: #D32F2F;'>❌ Error al procesar el resultado: {str(e)}</div>"
            if self.use_dialog_for_result:
                self.show_result_in_dialog(error_html)
            else:
                self.display_result(error_html)
