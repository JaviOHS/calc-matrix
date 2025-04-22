from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize, QPoint
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QStackedWidget, QLabel, QSizePolicy
import os
from ui.dialogs.message_dialog import MessageDialog
from ui.widgets.floating_sidebar import FloatingSidebar

class BaseOperationPage(QWidget):
    def __init__(self, manager, controller, operations_dict, intro_text, intro_image_path, page_title):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)
        self.manager = manager
        self.controller = controller
        self.operations = operations_dict
        self.current_operation = None
        self.operation_widgets = {}

        self.intro_text = intro_text
        self.intro_image_path = intro_image_path
        self.page_title = page_title

        self.intro_widget = self.create_intro_widget()
        self.init_ui()

    def init_ui(self):
        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Contenedor principal para el contenido
        self.content_container = QWidget()
        self.content_container.setObjectName("contentContainer")
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(0)

        # Contenedor para el título
        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # Título
        self.title_label = QLabel(self.page_title)
        self.title_label.setObjectName("title_label")
        self.title_label.setAlignment(Qt.AlignLeft)
        title_layout.addWidget(self.title_label)

        self.content_layout.addWidget(title_container)

        # Stacked widget para el contenido principal
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.intro_widget)
        self.content_layout.addWidget(self.stacked_widget, 1)

        # Botón flotante
        self.toggle_button = QPushButton(self.content_container)
        self.toggle_button.setIcon(QIcon(os.path.join("assets", "icons", "options.svg")))
        self.toggle_button.setText("Opciones")
        self.toggle_button.setIconSize(QSize(24, 24))
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        self.toggle_button.setObjectName("toggle_button")
        self.toggle_button.setCursor(Qt.PointingHandCursor)
        self.toggle_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.toggle_button.adjustSize()

        # Colocar el botón inicialmente
        self.toggle_button.move(self.width() - self.toggle_button.width() - 10, 60)

        # Sidebar
        self.sidebar = FloatingSidebar()
        self.sidebar.setVisible(False)
        self.add_operation_buttons()

        # Añadir al layout principprepare_operational
        self.layout.addWidget(self.content_container)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_button_position()


    def toggle_sidebar(self):
        if self.sidebar.isVisible():
            self.sidebar.hide()
        else:
            self.sidebar.show()
            self.sidebar.raise_()
            # Posicionamos el sidebar relativo al botón
            button_pos = self.toggle_button.pos()
            sidebar_pos = self.content_container.mapToGlobal(button_pos)
            sidebar_pos += QPoint(-self.sidebar.width() // 2 + self.toggle_button.width() // 2, 
                                self.toggle_button.height() + 5)
            self.sidebar.move(self.mapFromGlobal(sidebar_pos))

    def add_operation_buttons(self):
        for label, (op_key, _) in self.operations.items():
            self.sidebar.add_button(label, lambda _, k=label: self.prepare_operation(k))

    def reset_interface(self):
        if self.current_operation:
            widget = self.operation_widgets.get(self.current_operation)
            if widget:
                widget.cleanup()
                self.manager.clear()
                self.stacked_widget.setCurrentWidget(widget)
                return

        self.current_operation = None
        self.title_label.setText(self.page_title)
        self.manager.clear()

        for widget in self.operation_widgets.values():
            widget.cleanup()

        self.stacked_widget.setCurrentWidget(self.intro_widget)
        self.sidebar.set_active(None)

    def prepare_operation(self, operation_key):
        op_key, widget_class = self.operations[operation_key]
        self.current_operation = op_key
        self.title_label.setText(self.page_title)

        self.sidebar.set_active(operation_key)

        if operation_key not in self.operation_widgets:
            try:
                widget = widget_class(self.manager, self.controller, op_key)
            except TypeError:
                widget = widget_class(self.manager, self.controller)

            widget.calculate_button.clicked.connect(self.execute_current_operation)
            widget.cancel_button.clicked.connect(self.reset_interface)

            self.operation_widgets[operation_key] = widget
            self.stacked_widget.addWidget(widget)

        widget = self.operation_widgets[operation_key]
        self.stacked_widget.setCurrentWidget(widget)
        self.toggle_button.setText(operation_key)
        self.toggle_button.adjustSize()
        self.update_button_position()

    def update_button_position(self):
        if hasattr(self, 'toggle_button') and hasattr(self, 'title_label'):
            margin_right = 10
            button_initial_y = 28

            if self.height() > 600:
                title_height = self.title_label.height()
                button_vertical_position = self.title_label.pos().y() + title_height // 2 - self.toggle_button.height() // 2
                self.toggle_button.move(self.width() - self.toggle_button.width() - margin_right, button_vertical_position)
            else:
                self.toggle_button.move(self.width() - self.toggle_button.width() - margin_right, button_initial_y)

    def create_intro_widget(self):
        intro_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 60, 20, 20)

        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        intro_label = QLabel(self.intro_text)
        intro_label.setWordWrap(True)
        intro_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        left_layout.addWidget(intro_label)

        start_button = QPushButton("Empezar")
        start_button.setFixedWidth(150)
        start_button.setObjectName("start_button")
        start_button.setCursor(Qt.PointingHandCursor)
        start_button.clicked.connect(self.start_first_operation)
        left_layout.addWidget(start_button, alignment=Qt.AlignLeft)

        main_layout.addLayout(left_layout)

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

    def show_message_dialog(self, title: str, message: str, image_name: str = "error.png"):
        dialog = MessageDialog(title, message, image_name, parent=self)
        dialog.exec()

    def execute_current_operation(self):
        raise NotImplementedError("Subclases deben implementar este método.")

    def show_result(self, result, message):
        raise NotImplementedError("Subclases deben implementar este método.")
    