from utils.resources import resource_path
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget, QLabel, QMenu, QWidgetAction
from ui.dialogs.message_dialog import MessageDialog
from ui.widgets.action_buttons import ActionButton

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
        self.page_title = page_title  # Formato: "Operaciones con {Ej. Matrices}"

        self.intro_widget = self.create_intro_widget()
        self.init_ui()

    def init_ui(self):
        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 30, 40, 30)
        self.layout.setSpacing(0)

        # Contenedor para el título de operación (visible solo durante operaciones)
        self.operation_title_container = QWidget()
        self.operation_title_container.hide()  # Oculto inicialmente
        
        operation_title_layout = QHBoxLayout(self.operation_title_container)
        operation_title_layout.setContentsMargins(30, 20, 10, 10)
        
        self.operation_title_label = QLabel()
        self.operation_title_label.setObjectName("operationTitle")
        
        operation_title_layout.addWidget(self.operation_title_label)
        operation_title_layout.addStretch() # Esto empuja el botón de opciones hacia la derecha

        # Botón de opciones alineado a la derecha
        self.toggle_button = ActionButton.options()
        self.toggle_button.clicked.connect(self.show_dropdown_menu)
        self.toggle_button.hide()

        operation_title_layout.addWidget(self.toggle_button)  # Añado el botón al layout

        self.layout.addWidget(self.operation_title_container)

        # Contenedor principal (texto izquierda, imagen derecha)
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(40)

        # Sección de texto (izquierda) 
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(30, 40, 30, 40)  # Añadidos márgenes internos como en MainHomePage
        text_layout.setSpacing(20)

        # Título con formato especial para la parte naranja
        title_label = QLabel()
        title_label.setObjectName("heroTitle")
        
        # Procesamos el título para separar la parte naranja
        if "{" in self.page_title and "}" in self.page_title:
            parts = self.page_title.split("{")
            main_text = parts[0]
            orange_text = parts[1].replace("}", "")
            title_label.setText(f"{main_text}<span style='color:#ff8103;'>{orange_text}</span>")
        else:
            title_label.setText(self.page_title)

        text_layout.addWidget(title_label)

        # Descripción con viñetas
        description = QLabel(self.intro_text)
        description.setObjectName("heroDescription")
        description.setWordWrap(True)
        text_layout.addWidget(description)

        # Contenedor para botón y texto
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(20)

        button = ActionButton.primary("Empezar")
        button.clicked.connect(self.start_first_operation)

        # Texto al lado del botón
        footer_text = QLabel("📚 Disfruta del mundo de las matemáticas. ")
        footer_text.setObjectName("footerText")

        button_layout.addWidget(button)
        button_layout.addWidget(footer_text)
        button_layout.addStretch()

        text_layout.addWidget(button_container)
        text_layout.addStretch()

        # Añadir sección de texto al contenedor principal (izquierda)
        container_layout.addWidget(text_widget, 6)  # Mayor peso para el texto

        # Sección de imagen (derecha) 
        if self.intro_image_path:
            image_widget = QWidget()
            image_layout = QVBoxLayout(image_widget)
            image_layout.setContentsMargins(30, 40, 30, 40)
            image_layout.setSpacing(0)

            # Contenedor de imagen
            image_container = QWidget()
            image_container_layout = QVBoxLayout(image_container)
            image_container_layout.setContentsMargins(0, 0, 0, 0)

            # Cargar y mostrar imagen
            image = QLabel()
            pixmap = QPixmap(resource_path(self.intro_image_path))
            image.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            image.setAlignment(Qt.AlignCenter)
            image_container_layout.addWidget(image)

            image_layout.addWidget(image_container)
            container_layout.addWidget(image_widget, 4)  # Menor peso para la imagen

        # Stacked widget para manejar la vista de introducción vs operación
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(container)
        self.layout.addWidget(self.stacked_widget)

    def create_intro_widget(self):
        return QWidget()

    def show_dropdown_menu(self):
        menu = QMenu(self)
        menu.setObjectName("operationsMenu")
        
        # Opcional: Añadir un widget separador para crear espacio al principio
        spacer = QWidgetAction(menu)
        spacer_widget = QWidget()
        spacer_widget.setFixedHeight(10)  # Altura del margen
        spacer_widget.setStyleSheet("background-color: transparent;")
        spacer.setDefaultWidget(spacer_widget)
        menu.addAction(spacer)
        
        # Añadir las opciones reales del menú
        for label, (op_key, _) in self.operations.items():
            action = QAction(label, self)
            action.triggered.connect(lambda _, k=label: self.prepare_operation(k))
            menu.addAction(action)
        
        # Ajustar posición para que aparezca debajo del botón con un pequeño margen
        position = self.toggle_button.mapToGlobal(QPoint(0, self.toggle_button.height() + 5))
        menu.exec_(position)

    def prepare_operation(self, operation_key):
        self.toggle_button.show()
        if hasattr(self, 'main_title_container'):
            self.main_title_container.hide()
        op_key, widget_class = self.operations[operation_key]
        self.current_operation = op_key
        
        # Actualizar título de operación
        object_name = self.get_object_name()
        operation_title = f"{operation_key} de <span style='color:#ff8103;'>{object_name}</span>"
        self.operation_title_label.setText(operation_title)
        self.operation_title_container.show()
        
        if operation_key not in self.operation_widgets:
            try:
                widget = widget_class(self.manager, self.controller, op_key)
            except TypeError:
                widget = widget_class(self.manager, self.controller)

            # Configurar título en el widget si es necesario
            if hasattr(widget, 'set_operation_title'):
                widget.set_operation_title(operation_title)

            widget.calculate_button.clicked.connect(self.execute_current_operation)
            widget.cancel_button.clicked.connect(self.reset_interface)

            self.operation_widgets[operation_key] = widget
            self.stacked_widget.addWidget(widget)

        widget = self.operation_widgets[operation_key]
        self.stacked_widget.setCurrentWidget(widget)
        self.toggle_button.adjustSize()

    def get_object_name(self):
        if "{" in self.page_title and "}" in self.page_title:
            return self.page_title.split("{")[1].replace("}", "")
        return "Objeto"

    def reset_interface(self):
        self.toggle_button.hide()

        if self.current_operation:
            widget = self.operation_widgets.get(self.current_operation)
            if widget:
                widget.cleanup()
                self.manager.clear()
                
        self.current_operation = None
        self.operation_title_container.hide()
        self.stacked_widget.setCurrentIndex(0)
        self.layout.update()

    def start_first_operation(self):
        if self.operations:
            first_label = next(iter(self.operations))
            self.prepare_operation(first_label)

    def show_message_dialog(self, title: str, title_color: str, message: str, image_name: str = "error.png"):
        dialog = MessageDialog(title, title_color, message, image_name, parent=self)
        dialog.exec()

    def execute_current_operation(self):
        raise NotImplementedError("Subclases deben implementar este método.")

    def show_result(self, result, message):
        raise NotImplementedError("Subclases deben implementar este método.")
