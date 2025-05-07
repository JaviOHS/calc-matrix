from utils.resources import resource_path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QTextEdit, QHBoxLayout
from PySide6.QtGui import QPixmap

from ui.widgets.math_operation_widget import MathOperationWidget
from ui.widgets.expression_components.expression_buttons_panel import ExpressionButtonsPanel
from ui.widgets.expression_components.expression_formatter_input import ExpressionFormatterInput
from ui.widgets.expression_components.canvas_dialog_manager import CanvasDialogManager

class ExpressionOpWidget(MathOperationWidget):
    def __init__(self, manager, controller, operation_type=None, placeholder="", input_label="", image_path="assets/images/placeholder.png", use_dialog_for_result: bool = False):
        super().__init__(manager, controller, operation_type)
        self.operation_type = operation_type
        self.placeholder = placeholder
        self.input_label_text = input_label
        self.image_path = image_path
        self.use_dialog_for_result = use_dialog_for_result
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)

        title_label = QLabel(self.input_label_text)
        title_label.setAlignment(Qt.AlignLeft)
        self.layout.addWidget(title_label)
        title_label.setContentsMargins(20, 0, 0, 0)

        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        input_layout.setContentsMargins(20, 0, 0, 0)
        input_layout.setSpacing(8)

        self.expression_input = QTextEdit()
        self.expression_input.setPlaceholderText(self.placeholder)
        self.expression_input.setMaximumHeight(100)
        input_layout.addWidget(self.expression_input)
        
        # Configuración del formateador de expresiones
        self.expression_formatter = ExpressionFormatterInput(self.expression_input)
        
        # Configuración del gestor de diálogo de canvas
        self.canvas_dialog_manager = CanvasDialogManager(self)

        if not self.use_dialog_for_result:
            self.result_container = QWidget()
            result_layout = QHBoxLayout(self.result_container)
            result_layout.setContentsMargins(0, 0, 0, 0)
            result_layout.setSpacing(8)

            self.result_display = QTextEdit()
            self.result_display.setReadOnly(True)
            self.result_display.setFrameStyle(QTextEdit.NoFrame)
            self.result_display.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.result_display.setMinimumHeight(70)
            self.result_display.setStyleSheet("font-size: 18px; font-weight: 600;")
            self.result_display.setText("⭐ Aquí se mostrará la solución")
            result_layout.addWidget(self.result_display, stretch=1)

            if self.image_path:
                self.preview_image = QLabel()
                pixmap = QPixmap(resource_path(self.image_path))
                if not pixmap.isNull():
                    pixmap = pixmap.scaledToHeight(120, Qt.SmoothTransformation)
                    self.preview_image.setPixmap(pixmap)
                result_layout.addWidget(self.preview_image, alignment=Qt.AlignRight)

            input_layout.addWidget(self.result_container)

        self.layout.addWidget(input_widget, alignment=Qt.AlignTop)

        # Contenedor combinado para símbolos y acciones
        combined_panel = QWidget()
        combined_layout = QHBoxLayout(combined_panel)
        combined_layout.setContentsMargins(0, 10, 0, 0)
        combined_layout.setSpacing(30)

        # Panel de botones de expresión
        expression_buttons = ExpressionButtonsPanel(self.expression_input)
        combined_layout.addWidget(expression_buttons, alignment=Qt.AlignLeft)

        # Contenedor de botones de acción alineado a la derecha
        action_buttons_container = QWidget()
        action_buttons_layout = QHBoxLayout(action_buttons_container)
        action_buttons_layout.setContentsMargins(0, 0, 0, 0)
        action_buttons_layout.addStretch()
        action_buttons_layout.addWidget(self.create_buttons())
        combined_layout.addWidget(action_buttons_container, alignment=Qt.AlignRight | Qt.AlignBottom)

        self.layout.addWidget(combined_panel)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def get_input_expression(self):
        return self.expression_input.toPlainText().strip()

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
            # Extraer HTML y canvas si el resultado es un diccionario con ambos
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
