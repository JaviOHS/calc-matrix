
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

        self.flow_layout_widget = QWidget()
        self.operations_buttons = FlowLayout(self.flow_layout_widget)
        self.layout.addWidget(self.flow_layout_widget)
        self.add_operation_buttons()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.intro_widget)
        self.layout.addWidget(self.stacked_widget)

        self.setLayout(self.layout)

    def add_operation_buttons(self):
        for label, (op_key, _) in self.operations.items():
            btn = QPushButton(label)
            btn.setProperty("class", "operation-button")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumHeight(40)
            btn.setMinimumWidth(120)
            btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            btn.clicked.connect(lambda _, k=label: self.prepare_operation(k))
            self.operation_buttons_map[label] = btn
            self.operations_buttons.addWidget(btn)

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

from PySide6.QtWidgets import QLayout, QSizePolicy
from PySide6.QtCore import QPoint, QRect, QSize

class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=10):
        super().__init__(parent)
        self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)
        self.item_list = []

    def addItem(self, item):
        self.item_list.append(item)

    def count(self):
        return len(self.item_list)

    def itemAt(self, index):
        if 0 <= index < len(self.item_list):
            return self.item_list[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.item_list):
            return self.item_list.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self.item_list:
            size = size.expandedTo(item.minimumSize())
        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def doLayout(self, rect, test_only):
        x = rect.x()
        y = rect.y()
        line_height = 0

        for item in self.item_list:
            widget = item.widget()
            space_x = self.spacing()
            space_y = self.spacing()
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y()
