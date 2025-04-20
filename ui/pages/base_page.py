
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout, QStackedWidget, QMessageBox, QTableWidgetItem, QTableWidget, QSizePolicy, QGridLayout

class BaseOperationPage(QWidget):
    def __init__(self, manager, controller, operations_dict, intro_text, intro_image_path, page_title):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.manager = manager
        self.controller = controller
        self.operations = operations_dict
        self.current_operation = None
        self.operation_widgets = {}
        self.result_widget = None
        self.operation_buttons_map = {}

        self.intro_text = intro_text
        self.intro_image_path = intro_image_path
        self.page_title = page_title

        self.intro_widget = self.create_intro_widget()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.title_label = QLabel(self.page_title)
        self.title_label.setObjectName("title_label")
        self.title_label.setAlignment(Qt.AlignLeft)
        self.layout.addWidget(self.title_label)

        label = QLabel("Opciones disponibles:")
        self.layout.addWidget(label)

        self.operations_buttons = QHBoxLayout()
        self.add_operation_buttons()
        self.layout.addLayout(self.operations_buttons)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.intro_widget)
        self.layout.addWidget(self.stacked_widget)

        self.setLayout(self.layout)

    def add_operation_buttons(self):
        # Crear un layout de cuadrícula para mejor distribución
        grid_layout = QGridLayout()
        row, col = 0, 0
        max_cols = 4  # Máximo de botones por fila
        
        for label, (op_key, _) in self.operations.items():
            btn = QPushButton(label)
            btn.setProperty("class", "operation-button")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumHeight(40)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMinimumWidth(120)  # Ancho mínimo para mantener legibilidad
            
            btn.clicked.connect(lambda _, k=label: self.prepare_operation(k))
            
            grid_layout.addWidget(btn, row, col)
            self.operation_buttons_map[label] = btn
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Reemplazar el QHBoxLayout con el QGridLayout
        self.operations_buttons.addLayout(grid_layout)

    def reset_interface(self):
        # Si hay una operación actual, mantenerla activa
        if self.current_operation:
            widget = self.operation_widgets.get(self.current_operation)
            if widget:
                widget.cleanup()  # Limpiar datos anteriores
                self.manager.clear()
                self.stacked_widget.setCurrentWidget(widget)
                return

        # Si no hay operación actual, ir al intro
        self.current_operation = None
        self.title_label.setText(self.page_title)
        self.manager.clear()

        for widget in self.operation_widgets.values():
            widget.cleanup()

        self.stacked_widget.setCurrentWidget(self.intro_widget)

        for btn in self.operation_buttons_map.values():
            btn.setProperty("active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

    def prepare_operation(self, operation_key):
        op_key, widget_class = self.operations[operation_key]
        self.current_operation = op_key
        self.title_label.setText(self.page_title)

        # Desactivar botones anteriores
        for label, btn in self.operation_buttons_map.items():
            is_active = (label == operation_key)
            btn.setProperty("active", is_active)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

        # Crear y mostrar widget correspondiente
        try:
            widget = widget_class(self.manager, self.controller, op_key)
        except TypeError:
            widget = widget_class(self.manager, self.controller)
        widget.calculate_button.clicked.connect(self.execute_current_operation)
        widget.cancel_button.clicked.connect(self.reset_interface)

        self.operation_widgets[operation_key] = widget
        self.stacked_widget.addWidget(widget)
        self.stacked_widget.setCurrentWidget(widget)

    def execute_current_operation(self):
        """Debe ser implementado por la subclase."""
        raise NotImplementedError("Subclases deben implementar este método.")

    def show_result(self, result, message):
        """Interfaz :>"""
        raise NotImplementedError("Subclases deben implementar este método.")

    def create_intro_widget(self):
        intro_widget = QWidget()
        main_layout = QHBoxLayout()  # Layout principal horizontal (izquierda: texto, derecha: imagen)
        main_layout.setContentsMargins(0, 60, 20, 20)  # Izquierda, Arriba, Derecha, Abajo

        # Lado izquierdo (texto + botón)
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Texto de introducción
        intro_label = QLabel(self.intro_text)
        intro_label.setWordWrap(True)
        intro_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        left_layout.addWidget(intro_label)

        # Botón "Empezar"
        start_button = QPushButton("Empezar")
        start_button.setFixedWidth(150)
        start_button.setObjectName("start_button")
        start_button.setCursor(Qt.PointingHandCursor)
        start_button.clicked.connect(self.start_first_operation)
        left_layout.addWidget(start_button, alignment=Qt.AlignLeft)

        main_layout.addLayout(left_layout)

        # Imagen a la derecha
        if self.intro_image_path:
            pixmap = QPixmap(self.intro_image_path)
            image_label = QLabel()
            image_label.setPixmap(pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            image_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            main_layout.addWidget(image_label)

        intro_widget.setLayout(main_layout)
        return intro_widget

    def start_first_operation(self):
        if self.operations:
            first_label = next(iter(self.operations))
            self.prepare_operation(first_label)