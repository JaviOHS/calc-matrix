from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QTextEdit, QHBoxLayout
from ui.widgets.math_operation_widget import MathOperationWidget
from PySide6.QtGui import QTextCharFormat, QFont, QPixmap

class ExpressionOpWidget(MathOperationWidget):
    def __init__(self, manager, controller, operation_type=None, placeholder="", input_label="", image_path="assets/images/placeholder.png"):
        super().__init__(manager, controller, operation_type)
        self.operation_type = operation_type
        self.placeholder = placeholder
        self.input_label_text = input_label
        self.image_path = image_path
        self.setup_ui() # Para botones de cancelar y calcular

    def setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)

        title_label = QLabel(self.input_label_text)
        title_label.setAlignment(Qt.AlignLeft)
        self.layout.addWidget(title_label)

        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(8)

        self.expression_input = QTextEdit()
        self.expression_input.setPlaceholderText(self.placeholder)
        self.expression_input.setMaximumHeight(100)
        input_layout.addWidget(self.expression_input)

        self.result_container = QWidget()
        result_layout = QHBoxLayout(self.result_container)
        result_layout.setContentsMargins(0, 0, 0, 0)
        result_layout.setSpacing(8)

        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setFrameStyle(QTextEdit.NoFrame)
        self.result_display.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.result_display.setMinimumHeight(70)
        self.result_display.setStyleSheet("font-family: Dosis; font-size: 18px; font-weight: 600;")
        self.result_display.setText("⭐ Aquí se mostrará la solución")
        result_layout.addWidget(self.result_display, stretch=1)

        if self.image_path:
            self.preview_image = QLabel()
            pixmap = QPixmap(self.image_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaledToHeight(120, Qt.SmoothTransformation)
                self.preview_image.setPixmap(pixmap)
            result_layout.addWidget(self.preview_image, alignment=Qt.AlignRight)

        input_layout.addWidget(self.result_container)
        self.layout.addWidget(input_widget)

        buttons = self.create_buttons()
        self.layout.addWidget(buttons)
        self.setLayout(self.layout)

        self.setup_expression_formatting()

    def get_input_expression(self):
        return self.expression_input.toPlainText().strip()

    def display_result(self, html):
        self.result_display.setText(html)

    def setup_expression_formatting(self):
        """Configura el formateo automático de expresiones"""
        self.expression_input.textChanged.connect(self.format_expression_in_input)

    def format_expression_in_input(self):
        """Formatea la expresión matemática en tiempo real"""
        cursor = self.expression_input.textCursor()
        position = cursor.position()
        text = self.expression_input.toPlainText()
        self.expression_input.blockSignals(True)

        # Construir un nuevo documento formateado
        self.expression_input.clear()
        new_cursor = self.expression_input.textCursor()

        base_format = QTextCharFormat()
        base_format.setFont(QFont("Cambria Math", 14))

        super_format = QTextCharFormat(base_format)
        super_format.setVerticalAlignment(QTextCharFormat.AlignSuperScript)

        i = 0
        while i < len(text):
            if text[i] == '^':
                new_cursor.insertText('^', base_format)
                i += 1
                # Formatear superíndices
                start = i
                while i < len(text) and text[i].isdigit():
                    new_cursor.insertText(text[i], super_format)
                    i += 1
            else:
                new_cursor.insertText(text[i], base_format)
                i += 1

        # Restaurar posición del cursor
        new_cursor.setPosition(min(position, len(self.expression_input.toPlainText())))
        self.expression_input.setTextCursor(new_cursor)
        self.expression_input.blockSignals(False)
