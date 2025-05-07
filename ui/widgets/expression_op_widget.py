from utils.resources import resource_path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QTextEdit, QHBoxLayout
from ui.widgets.math_operation_widget import MathOperationWidget
from PySide6.QtGui import QTextCharFormat, QFont, QPixmap
from ui.dialogs.message_dialog import MessageDialog
from PySide6.QtWidgets import QPushButton, QGridLayout

class ExpressionOpWidget(MathOperationWidget):
    def __init__(self, manager, controller, operation_type=None, placeholder="", input_label="", image_path="assets/images/placeholder.png", use_dialog_for_result: bool = False):
        super().__init__(manager, controller, operation_type)
        self.operation_type = operation_type
        self.placeholder = placeholder
        self.input_label_text = input_label
        self.image_path = image_path
        self.use_dialog_for_result = use_dialog_for_result
        self.setup_ui() # Para botones de cancelar y calcular

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

        # Panel de botones de símbolos
        expression_buttons = self.create_expression_buttons()
        combined_layout.addWidget(expression_buttons, alignment=Qt.AlignLeft)

        # Contenedor de botones de acción alineado completamente a la derecha
        action_buttons_container = QWidget()
        action_buttons_layout = QHBoxLayout(action_buttons_container)
        action_buttons_layout.setContentsMargins(0, 0, 0, 0)
        action_buttons_layout.addStretch()
        action_buttons_layout.addWidget(self.create_buttons())
        combined_layout.addWidget(action_buttons_container, alignment=Qt.AlignRight | Qt.AlignBottom)

        self.layout.addWidget(combined_panel)

        self.layout.addStretch()
        self.setLayout(self.layout)
        self.setup_expression_formatting()

    def get_input_expression(self):
        return self.expression_input.toPlainText().strip()

    def display_result(self, html):
        if not self.use_dialog_for_result and hasattr(self, 'result_display'):
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

    def show_canvas_dialog(self, canvas):
        if canvas:
            canvas.setFixedSize(500, 300)
            canvas.draw()
            dialog = MessageDialog(
                title="🟢 ÉXITO GENERANDO GRÁFICA",
                title_color="#7cb342",
                image_name="success.png",
                parent=self,
                custom_widget=canvas
            )
            dialog.exec()

    def create_expression_buttons(self):
        symbols = [
            ("^", "^"), ("√", "sqrt("), ("π", "pi"), ("e", "e"), ("ln", "ln("),
            ("log", "log("), ("sin", "sin("), ("cos", "cos("), ("tan", "tan("),
            ("y'", "y'(x)"), ("y''", "y''(x)"), ("=", "="), 
            ("+", "+"), ("-", "-"), ("*", "*"), ("/", "/"),
            ("(", "("), (")", ")"), ("{", "{"), ("}", "}"),
            ("[", "["), ("]", "]"), ("{", "{"), ("}", "}"),
        ]

        button_panel = QWidget()
        layout = QGridLayout(button_panel)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(8)

        for index, (label, insert_text) in enumerate(symbols):
            button = QPushButton(label)
            button.setMinimumSize(42, 42)
            button.setObjectName("ctaButton")
            button.setStyleSheet("font-size: 14px;")
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(lambda _, text=insert_text: self.insert_symbol(text))
            layout.addWidget(button, index // 8, index % 8)

        return button_panel

    def insert_symbol(self, text):
        cursor = self.expression_input.textCursor()
        cursor.insertText(text)
        self.expression_input.setTextCursor(cursor)
        self.expression_input.setFocus()
        