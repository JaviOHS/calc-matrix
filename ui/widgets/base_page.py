from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame, QScrollArea, QStackedWidget, QMenu, QWidgetAction
from PySide6.QtCore import Qt
from utils.components.image_utils import create_image_label
from utils.core.content_manager import ContentManager
from utils.components.action_buttons import ActionButton
from ui.dialogs.simple.message_dialog import MessageDialog
from utils.formating.format_title import format_title, highlight_last_word
from utils.core.component_factory import create_info_item
from utils.core.educational_content import EducationalContentManager
from PySide6.QtGui import QAction
from PySide6.QtCore import QPoint

class BasePage(QWidget):
    def __init__(self, navigate_callback=None, page_key=None, controller=None, manager=None):
        super(BasePage, self).__init__()
        self.navigate_callback = navigate_callback
        self.page_key = page_key
        self.controller = controller
        self.manager = manager
        
        # Para contenido dinámico desde JSON
        self.content_manager = ContentManager.get_instance()
        self.page_content = self.content_manager.get_page_content(self.page_key) if self.page_key else {}
        
        # Para operaciones matemáticas
        self.operations = {}  # Será configurado por las clases derivadas si es necesario
        self.current_operation = None
        self.operation_widgets = {}
        
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # Contenedor para el título de operación (visible solo durante operaciones)
        self.operation_title_container = QWidget()
        self.operation_title_container.hide()  # Oculto inicialmente
        
        operation_title_layout = QHBoxLayout(self.operation_title_container)
        # Reducir los márgenes para que el título tenga más espacio horizontal
        operation_title_layout.setContentsMargins(20, 15, 10, 10)
        
        self.operation_title_label = QLabel()
        self.operation_title_label.setObjectName("operationTitle")
        self.operation_title_label.setMaximumHeight(60)
        self.operation_title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        operation_title_layout.addWidget(self.operation_title_label)
        operation_title_layout.addStretch()

        # Botón de opciones alineado a la derecha
        self.toggle_button = ActionButton.options()
        self.toggle_button.clicked.connect(self.show_dropdown_menu)
        self.toggle_button.hide()

        operation_title_layout.addWidget(self.toggle_button)
        main_layout.addWidget(self.operation_title_container)

        # Widget apilado para manejar diferentes vistas
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Crear y añadir la vista de intro
        self.intro_view = self.create_intro_view()
        self.stacked_widget.addWidget(self.intro_view)

    def create_intro_view(self):
        # Crear un área de desplazamiento para contenido largo
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Cambiar la política de scroll horizontal a nunca mostrar
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        container = QFrame()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(40)

        # Panel de contenido principal - establecer políticas de tamaño
        self.text_panel = QFrame()
        self.text_panel.setObjectName("contentPanel")
        self.text_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.text_panel.setMinimumWidth(350)
        self.text_panel.setMaximumWidth(600)
        
        self.text_layout = QVBoxLayout(self.text_panel)
        self.text_layout.setSpacing(24)
        self.text_layout.setContentsMargins(28, 28, 28, 28)

        self.setup_text_content()

        # Imagen con efectos visuales - puede comprimirse si es necesario
        image_panel = QFrame()
        image_panel.setObjectName("imagePanel")
        image_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        image_panel.setMinimumWidth(250)

        image_layout = QVBoxLayout(image_panel)
        image_layout.setContentsMargins(20, 20, 20, 0)

        image_container = QFrame()
        image_container_layout = QVBoxLayout(image_container)
        image_container_layout.setContentsMargins(0, 0, 0, 0)

        # Usar la utilidad para crear la imagen
        image = create_image_label(self.get_image_path(), width=self.get_image_width(), height=self.get_image_height())
        image_container_layout.addWidget(image, 0, Qt.AlignCenter)

        image_layout.addWidget(image_container)
        
        # Agregar contenido educativo adicional
        self.setup_educational_content(image_layout)

        # Añadir los paneles al layout con proporciones flexibles
        container_layout.addWidget(self.text_panel, 6)
        container_layout.addWidget(image_panel, 4)

        scroll_area.setWidget(container)
        return scroll_area

    def setup_text_content(self):
        """
        Configura el contenido de texto para la página basado en el contenido JSON.
        """
        # Título de la página
        header = QFrame()
        header.setObjectName("heroHeader")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Usar el método format_title para procesar el título
        formatted_title = format_title(self.page_content.get("title", "Título de la Página"))
        title = QLabel(formatted_title)
        title.setObjectName("heroTitle")
        title.setTextFormat(Qt.RichText) # Permite interpretar el HTML
        header_layout.addWidget(title)

        if "subtitle" in self.page_content:
            subtitle = self.page_content["subtitle"]
            subtitle_highlight = QLabel(subtitle)
            subtitle_highlight.setObjectName("heroHighlight")
            subtitle_highlight.setTextFormat(Qt.RichText)
            subtitle_highlight.setWordWrap(True)  # Habilitar ajuste de texto
            header_layout.addWidget(subtitle_highlight)

        self.text_layout.addWidget(header)
        
        # Descripción de la página
        intro_card = QFrame()
        intro_layout = QVBoxLayout(intro_card)
        
        description = QLabel(self.page_content.get("description", ""))
        description.setObjectName("heroDescription")
        description.setWordWrap(True)
        description.setTextFormat(Qt.RichText) # Permite interpretar el HTML en la descripción
        intro_layout.addWidget(description)
        
        self.text_layout.addWidget(intro_card)
        
        # Características/funcionalidades
        features = QFrame()
        features.setObjectName("featureContainer")
        features_layout = QVBoxLayout(features)
        features_layout.setSpacing(16)
        
        # Usar component_factory para crear elementos de característica
        for feature_data in self.page_content.get("features", []):
            feature = create_info_item(
                feature_data.get("icon", "⭐"), 
                feature_data.get("title", "Característica"), 
                feature_data.get("description", None)
            )
            features_layout.addWidget(feature)
    
        self.text_layout.addWidget(features)
        self.text_layout.addStretch()

    def setup_educational_content(self, layout, button_callback=None, external_url=None, button_icon=None):
        """
        Método para configurar contenido educativo adicional usando EducationalContentManager
        """
        # Si no hay callback específico, usar el método predeterminado
        if not button_callback:
            button_callback = self.start_first_operation
            
        # Usar EducationalContentManager para crear todo el contenido
        start_button = EducationalContentManager.setup_educational_content(
            self,
            self.page_content,
            layout,
            button_callback,
            external_url,
            button_icon
        )
        
        # Si necesitas acceder al botón después, puedes guardarlo como atributo
        self.start_button = start_button

    def get_image_path(self):
        """Obtiene la ruta de la imagen del contenido JSON si existe"""
        if self.page_content and "image" in self.page_content:
            return self.page_content.get("image", {}).get("path", "assets/images/intro/deco.png")
        return "assets/images/intro/default.png"

    def get_image_width(self):
        """Obtiene el ancho de la imagen del contenido JSON si existe"""
        if self.page_content and "image" in self.page_content:
            return self.page_content.get("image", {}).get("width", 200)
        return 200

    def get_image_height(self):
        """Obtiene la altura de la imagen del contenido JSON si existe"""
        if self.page_content and "image" in self.page_content:
            return self.page_content.get("image", {}).get("height", 200)
        return 200

    def get_image_caption(self):
        """Obtiene la descripción de la imagen del contenido JSON si existe"""
        if self.page_content and "image" in self.page_content:
            return self.page_content.get("image", {}).get("caption", None)
        return None

    # Métodos para la funcionalidad de operaciones matemáticas
    def show_dropdown_menu(self):
        if not self.operations:
            return
            
        menu = QMenu(self)
        menu.setObjectName("operationsMenu")
        
        spacer = QWidgetAction(menu)
        spacer_widget = QWidget()
        spacer_widget.setFixedHeight(10)
        spacer_widget.setStyleSheet("background-color: transparent;")
        spacer.setDefaultWidget(spacer_widget)
        menu.addAction(spacer)
        
        for label, (op_key, _) in self.operations.items():
            action = QAction(label, self)
            action.triggered.connect(lambda _, k=label: self.prepare_operation(k))
            menu.addAction(action)
        
        position = self.toggle_button.mapToGlobal(QPoint(0, self.toggle_button.height() + 5))
        menu.exec_(position)

    def prepare_operation(self, operation_key):
        self.toggle_button.show()
        
        op_key, widget_class = self.operations[operation_key]
        self.current_operation = op_key
        
        # Actualizar título de operación
        object_name = self.get_object_name()
        if not object_name:
            # Reducir el título si es muy largo
            if len(operation_key) > 45:
                operation_key = operation_key[:37] + "..."
            operation_title = highlight_last_word(operation_key)
        else:
            # Acortar el nombre del objeto si es muy largo
            if len(object_name) > 20:
                object_name = object_name[:17] + "..."
            operation_title = f"{operation_key} de <span style='color:#ff8103;'>{object_name}</span>"
        
        self.operation_title_label.setText(operation_title)
        # Ajustar el label para una línea preferentemente
        self.operation_title_label.setMinimumWidth(400)  # Ancho mínimo para mejor legibilidad
        self.operation_title_label.setWordWrap(True)  # Habilitar ajuste de texto
        self.operation_title_container.show()
        
        if operation_key not in self.operation_widgets:
            try:
                widget = widget_class(self.manager, self.controller, op_key)
            except TypeError:
                widget = widget_class(self.manager, self.controller)

            # Configurar título en el widget si es necesario
            if hasattr(widget, 'set_operation_title'):
                widget.set_operation_title(operation_title)

            if hasattr(widget, 'calculate_button'):
                widget.calculate_button.clicked.connect(self.execute_current_operation)
            if hasattr(widget, 'cancel_button'):
                widget.cancel_button.clicked.connect(self.reset_interface)

            self.operation_widgets[operation_key] = widget
            self.stacked_widget.addWidget(widget)

        widget = self.operation_widgets[operation_key]
        self.stacked_widget.setCurrentWidget(widget)

    def get_object_name(self):
        """Obtiene el nombre del objeto desde el título de la página"""
        page_title = self.page_content.get("title", "Objeto")
        if "{" in page_title and "}" in page_title:
            return page_title.split("{")[1].replace("}", "")
        return None

    def reset_interface(self):
        """Restablece la interfaz a su estado inicial"""
        self.toggle_button.hide()

        if self.current_operation:
            widget = self.operation_widgets.get(self.current_operation)
            if widget and hasattr(widget, 'cleanup'):
                widget.cleanup()
                
            if self.manager:
                self.manager.clear()
                
        self.current_operation = None
        self.operation_title_container.hide()
        self.stacked_widget.setCurrentIndex(0)

    def start_first_operation(self):
        """Inicia la primera operación disponible"""
        if self.operations:
            first_label = next(iter(self.operations))  # Obtiene la primera operación
            self.prepare_operation(first_label)  # Navega a la operación
        else:
            self.show_message_dialog(
                "🔴 ERROR", 
                "#f44336", 
                "No hay operaciones configuradas para esta página."
            )
            
    def show_message_dialog(self, title: str, title_color: str, message: str, image_name: str = "error.png"):
        """Muestra un diálogo de mensaje"""
        dialog = MessageDialog(title, title_color, message, image_name, parent=self)
        dialog.exec()

    def execute_current_operation(self):
        """Método para ser implementado por las subclases"""
        pass

    def show_result(self, result, message):
        """Método para ser implementado por las subclases"""
        pass
